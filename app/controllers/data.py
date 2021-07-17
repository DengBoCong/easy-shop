import re
import json
import uuid
from . import controllers
from .. import db
from ..models import *
from datetime import datetime
from flask import request
from flask import jsonify
from flask_login import login_required
from sqlalchemy import or_, and_
from ..setting import ROOT_NODE_ID, PAGE_LIMIT
from ..utils import *

URL_PREFIX = "/data"


# ==============================Frame相关================================

@controllers.route('{}/get!get_all_frame'.format(URL_PREFIX), methods=['GET'])
@login_required
def get_all_frame():
    info_data = request.args.to_dict()
    try:
        frames = Frame.query.get(ROOT_NODE_ID)
        frame, _ = get_frame_tree(frames=frames, spread_id=info_data.get("spreadId", ""))

        return jsonify({'code': 0, 'msg': '', 'data': [frame]})
    except:
        return jsonify({'code': 1, 'msg': '网络异常，加载失败', 'data': [{}]})


@controllers.route('{}/get!get_all_frame_for_select'.format(URL_PREFIX), methods=['GET'])
@login_required
def get_all_frame_for_select():
    try:
        frames = Frame.query.get(ROOT_NODE_ID)
        # frame_all = get_frame_with_third(frames)
        frame_not_verb = get_frame_not_third_where_not_verb(frames)
        # {"all": frame_all, "noVerb":frame_not_verb}
        return jsonify({'code': 0, 'msg': '', 'data': frame_not_verb})
    except:
        return jsonify({'code': 1, 'msg': '网络异常，加载失败', 'data': [{}]})


@controllers.route('{}/get!get_all_frame_where_not_third'.format(URL_PREFIX), methods=['GET'])
@login_required
def get_all_frame_where_not_third():
    try:
        frames = Frame.query.get(ROOT_NODE_ID)
        frame = get_frame_not_third(frames)

        return jsonify({'code': 0, 'msg': '', 'data': frame})
    except:
        return jsonify({'code': 1, 'msg': '网络异常，加载失败', 'data': [{}]})


@controllers.route('{}/add!add_frame'.format(URL_PREFIX), methods=['POST'])
@login_required
def add_frame():
    info_data = json.loads(request.get_data())
    try:
        name_frame = Frame.query.filter_by(NAME=info_data.get("NAME")).all()

        if len(name_frame) != 0:
            frames = Frame.query.get(ROOT_NODE_ID)
            frame_data, _ = get_frame_tree(frames=frames, spread_id=info_data.get("PARENT_ID"))

            return jsonify({'code': 0, 'msg': '名称重复，请重新填写',
                            'data': {'frame': [frame_data], 'newId': 'null'}})
        elif info_data.get("IF_THIRD") == 1:
            frames = Frame.query.get(ROOT_NODE_ID)
            frame_data, _ = get_frame_tree(frames=frames, spread_id=info_data.get("PARENT_ID"))
            return jsonify({'code': 0, 'msg': 'Frame最多三级',
                            'data': {'frame': [frame_data], 'newId': 'null'}})
        elif info_data.get("HAS_VERB") == 1:
            frames = Frame.query.get(ROOT_NODE_ID)
            frame_data, _ = get_frame_tree(frames=frames, spread_id=info_data.get("PARENT_ID"))
            return jsonify({'code': 0, 'msg': '该Frame存在子Verb，不允许添加Frame',
                            'data': {'frame': [frame_data], 'newId': 'null'}})
        else:
            new_id = uuid.uuid1()
            frame = Frame(ID=new_id, CREATE_DATETIME=datetime.now(), UPDATE_DATETIME=datetime.now(),
                          NAME="未命名", FRAME_TYPE="Archi", PARENT_ID=info_data.get("PARENT_ID"))
            db.session.add(frame)
            db.session.commit()

            frames = Frame.query.get(ROOT_NODE_ID)
            frame_data, _ = get_frame_tree(frames=frames, spread_id=info_data.get("PARENT_ID"))

            set_data_log(DATA="未命名", MESSAGE="初始化添加成功", ACTION="Frame", LEVEL="INFO")
            return jsonify({'code': 0, 'msg': '添加成功', 'data': {'frame': [frame_data], 'newId': new_id}})
    except:
        frames = Frame.query.get(ROOT_NODE_ID)
        frame_data, _ = get_frame_tree(frames=frames, spread_id=info_data.get("PARENT_ID"))

        set_data_log(DATA="未命名", MESSAGE="初始化添加失败", ACTION="Frame", LEVEL="ERROR")
        return jsonify({'code': 1, 'msg': '网络异常，添加失败，请重新刷新', 'data': {'frame': [frame_data], 'newId': 'null'}})


@controllers.route('{}/delete!delete_frame'.format(URL_PREFIX), methods=['POST'])
@login_required
def delete_frame_by_id():
    info_data = json.loads(request.get_data())
    frame = Frame.query.get(info_data.get("ID"))

    if frame is not None:
        delete_frame_and_sub(frame.child)
        for verb in frame.verbs:
            db.session.delete(verb)
        frame_samples = FrameElementSample.query.filter_by(FRAME_ID=frame.ID).all()
        for sample in frame_samples:
            db.session.delete(sample)
        db.session.delete(frame)

        # frames = Frame.query.get(ROOT_NODE_ID)
        # frame_data = get_frame_tree(frames)

        set_data_log(DATA=frame.NAME, MESSAGE="删除成功", ACTION="Frame", LEVEL="INFO")
        return jsonify({'code': 0, 'msg': '删除成功', 'data': {}}) # [frame_data]
    else:
        # frames = Frame.query.get(ROOT_NODE_ID)
        # frame_data = get_frame_tree(frames)

        set_data_log(DATA=frame.NAME, MESSAGE="删除异常", ACTION="Frame", LEVEL="ERROR")
        return jsonify({'code': 1, 'msg': '删除异常', 'data': {}})


def delete_frame_and_sub(frame):
    if len(frame) == 0:
        return

    for sub_frame in frame:
        for verb in sub_frame.verbs:
            db.session.delete(verb)
        frame_samples = FrameElementSample.query.filter_by(FRAME_ID=sub_frame.ID).all()
        for sample in frame_samples:
            db.session.delete(sample)
        delete_frame_and_sub(sub_frame.child)
        db.session.delete(sub_frame)


@controllers.route('{}/update!frame_basic_info'.format(URL_PREFIX), methods=['POST'])
@login_required
def update_frame_basic_info():
    info_data = json.loads(request.get_data())
    temp_frame = Frame.query.get(info_data.get("ID"))
    if info_data.get("ONLINE_PARENT_ID", None) and info_data.get("ONLINE_PARENT_ID") != "null":
        info_data["PARENT_ID"] = info_data.get("ONLINE_PARENT_ID")
    if info_data.get("ONLINE_PARENT_ID", None):
        del info_data["ONLINE_PARENT_ID"]
    if info_data["PARENT_ID"] != temp_frame.PARENT_ID and info_data["PARENT_ID"] != info_data.get("ID"):
        #  and info_data.get("PARENT_ID") != ROOT_NODE_ID
        parent_frame = Frame.query.get(info_data["PARENT_ID"])
        parent_count, child_count = 0, 1
        if info_data["PARENT_ID"] != ROOT_NODE_ID and parent_frame.parent:
            parent_count = 1
            if parent_frame.parent.parent:
                parent_count = 2
                if parent_frame.parent.parent.parent:
                    parent_count = 3
        if temp_frame.child:
            child_count = 2
            for child in temp_frame.child:
                if child.child:
                    child_count = 3
                    break
        if parent_count + child_count > 3:
            return jsonify({'code': 1, 'msg': '迁移Frame总级联层数超出三层，请重新选择', 'data': {}})

    if info_data.get("NAME") != temp_frame.NAME:
        name_frame = Frame.query.filter_by(NAME=info_data.get("NAME")).all()
        if len(name_frame) != 0:
            return jsonify({'code': 1, 'msg': '名称重复，请重新填写', 'data': {}})

    del info_data["file"]
    frame = Frame.query.filter_by(ID=info_data.get("ID")).update(info_data)

    if frame == 1:
        db.session.commit()

        set_data_log(DATA=info_data.get("ID"), MESSAGE="更新成功", ACTION="Frame", LEVEL="INFO")
        return jsonify({'code': 0, 'msg': '更新成功', 'data': {}})
    else:
        set_data_log(DATA=info_data.get("ID"), MESSAGE="信息更新失败", ACTION="Frame", LEVEL="ERROR")
        return jsonify({'code': 1, 'msg': '信息更新失败', 'data': {}})


# ==============================Element相关================================
@controllers.route('{}/get!get_all_element_type'.format(URL_PREFIX), methods=['GET'])
@login_required
def get_all_element_type():
    info_data = request.args.to_dict()
    page = int(info_data.get("page", 1))
    limit = int(info_data.get("limit", PAGE_LIMIT))
    try:
        frame_element_types = FrameElementType.query.order_by(FrameElementType.NAME.asc()).all()
        frame_element_type_list = []
        start = (page - 1) * limit
        for frame_element_type in frame_element_types:
            frame_element_type_json = frame_element_type.to_json()
            frame_element_type_list.append(frame_element_type_json)
        count = len(frame_element_type_list)
    except:
        return jsonify({'code': 1, 'msg': '网络异常，加载失败', 'count': '0', 'data': [{}]})

    return jsonify({'code': 0, 'msg': '', 'count': count, 'data': frame_element_type_list[start:page * limit]})


@controllers.route('{}/get!element_type_filter_by_param'.format(URL_PREFIX), methods=['GET'])
@login_required
def element_type_filter_by_param():
    info_data = request.args.to_dict()
    try:
        frame_element_types = FrameElementType.query.filter(
            and_(FrameElementType.NAME.like("%" + info_data.get("NAME", "") + "%"),
                 FrameElementType.TYPE.like("%" + info_data.get("TYPE", "") + "%"))).all()

        element_type_list = []
        for element_type in frame_element_types:
            element_type_json = element_type.to_json()
            element_type_list.append(element_type_json)
        count = len(element_type_list)
    except:
        return jsonify({'code': 1, 'msg': '网络异常，加载失败', 'count': '0', 'data': [{}]})

    return jsonify({'code': 0, 'msg': '', 'count': count, 'data': element_type_list})


@controllers.route('{}/get!element_type_filter_by_type'.format(URL_PREFIX), methods=['GET'])
def element_type_filter_by_type():
    info_data = request.args.to_dict()
    try:
        frame_element_types = FrameElementType.query.filter_by(TYPE=info_data.get("TYPE")).all()

        element_type_list = []
        for element_type in frame_element_types:
            element_type_json = element_type.to_json()
            element_type_list.append(element_type_json)
        count = len(element_type_list)
    except:
        return jsonify({'code': 1, 'msg': '网络异常，加载失败', 'count': '0', 'data': [{}]})

    return jsonify({'code': 0, 'msg': '', 'count': count, 'data': element_type_list})


@controllers.route('{}/get!element_type_all_with_filter_by_type'.format(URL_PREFIX), methods=['GET'])
@login_required
def element_type_all_with_filter_by_type():
    info_data = request.args.to_dict()
    try:
        frame_element_types = FrameElementType.query.all()

        element_type_list = []
        element_type_list_sub = []
        for element_type in frame_element_types:
            element_type_json = element_type.to_json()
            element_type_list.append(element_type_json)
            if element_type.TYPE == info_data.get("TYPE"):
                element_type_list_sub.append(element_type_json)
        count = len(element_type_list)
    except:
        return jsonify({'code': 1, 'msg': '网络异常，加载失败', 'count': '0', 'data': [{}]})

    return jsonify(
        {'code': 0, 'msg': '', 'count': count,
         'data': {'allType': element_type_list, 'subType': element_type_list_sub}})


@controllers.route('{}/get!element_type_filter_by_id'.format(URL_PREFIX), methods=['GET'])
@login_required
def element_type_filter_by_id():
    info_data = request.args.to_dict()
    try:
        frame_element_type = FrameElementType.query.get(info_data.get("ID"))
        if not frame_element_type:
            return jsonify({'code': 1, 'msg': '未找到相关ElementType信息', 'data': [{}]})
        frame_elements = []
        for element in frame_element_type.elements:
            element_json = element.to_json()
            frame_elements.append(element_json)
        count = len(frame_elements)
    except:
        return jsonify({'code': 1, 'msg': '网络异常，加载失败', 'data': [{}]})

    return jsonify({'code': 0, 'msg': '', 'count': count, 'data': frame_elements})


@controllers.route('{}/get!element_filter_by_id'.format(URL_PREFIX), methods=['GET'])
@login_required
def element_filter_by_id():
    info_data = request.args.to_dict()
    try:
        frame_element = FrameElement.query.get(info_data.get("ID"))
        frame_element_sample = FrameElementSample.query.get(info_data.get("sampleId"))
        if not frame_element:
            return jsonify({'code': 1, 'msg': '未找到相关Element信息', 'data': [{}]})
        frame_element_info = frame_element.to_json()
        frame_element_info["LEMMA"] = frame_element_sample.LEMMA
        frame_element_info["SAMPLE"] = frame_element_sample.SAMPLE
    except:
        return jsonify({'code': 1, 'msg': '网络异常，加载失败', 'data': [{}]})

    return jsonify({'code': 0, 'msg': '', 'data': frame_element_info})


@controllers.route('{}/add!add_element_type'.format(URL_PREFIX), methods=['POST'])
@login_required
def add_element_type():
    try:
        info_data = json.loads(request.get_data())
        name_element_type = FrameElementType.query.filter_by(NAME=info_data.get("NAME")).all()

        if len(name_element_type) != 0:
            return jsonify({'code': 1, 'msg': '名称重复，请重新填写', 'data': {}})
        else:
            element_type = FrameElementType(ID=uuid.uuid1(), CREATE_DATETIME=datetime.now(), TYPE=info_data.get("TYPE"),
                                            NAME=info_data.get("NAME"))
            db.session.add(element_type)
            db.session.commit()

            set_data_log(DATA=info_data.get("NAME"), MESSAGE="添加成功", ACTION="ElementType", LEVEL="INFO")
            return jsonify({'code': 0, 'msg': '添加成功', 'data': {}})
    except:
        set_data_log(DATA=info_data.get("NAME"), MESSAGE="添加失败", ACTION="ElementType", LEVEL="ERROR")
        return jsonify({'code': 1, 'msg': '网络异常，添加失败', 'data': {}})


@controllers.route('{}/add!add_frame_element'.format(URL_PREFIX), methods=['POST'])
@login_required
def add_frame_element():
    info_data = json.loads(request.get_data())
    try:
        frame = Frame.query.get(info_data.get("FRAME_ID"))
        if frame.frameElements.filter_by(ELEMENT_TYPE_ID=info_data.get("ELEMENT_TYPE_ID")).scalar() is not None:
            return jsonify({'code': 1, 'msg': '该元素已存在当前Frame中，请勿重复添加', 'data': {}})

        frame_element_id = uuid.uuid1()
        frame_element = FrameElement(ID=frame_element_id, CREATE_DATETIME=datetime.now(), DEF=info_data.get("DEF"),
                                     ELEMENT_TYPE_ID=info_data.get("ELEMENT_TYPE_ID"))
        frame_element_sample = FrameElementSample(ID=uuid.uuid1(), CREATE_DATETIME=datetime.now(),
                                                  LEMMA=info_data.get("LEMMA"),
                                                  SAMPLE=info_data.get("SAMPLE"), FRAME_ID=info_data.get("FRAME_ID"),
                                                  ELEMENT_ID=frame_element_id)

        frame_element.frames.append(frame)
        db.session.add(frame_element_sample)
        db.session.add(frame_element)
        db.session.commit()

        set_data_log(DATA="", MESSAGE="添加成功", ACTION="Element", LEVEL="INFO")
        return jsonify({'code': 0, 'msg': '添加成功', 'data': {}})
    except:
        set_data_log(DATA="", MESSAGE="添加失败", ACTION="Element", LEVEL="ERROR")
        return jsonify({'code': 1, 'msg': '网络异常，添加失败', 'data': {}})


@controllers.route('{}/add!contact_frame_element'.format(URL_PREFIX), methods=['POST'])
@login_required
def contact_frame_element():
    try:
        info_data = json.loads(request.get_data())
        frame = Frame.query.get(info_data.get("FRAME_ID"))
        frame_element = FrameElement.query.get(info_data.get("ELEMENT_ID"))
        if frame.frameElements.filter_by(ELEMENT_TYPE_ID=frame_element.ELEMENT_TYPE_ID).scalar() is not None:
            return jsonify({'code': 1, 'msg': '该元素已存在当前Frame中，请勿重复添加', 'data': {}})

        element_sample = FrameElementSample(ID=uuid.uuid1(), CREATE_DATETIME=datetime.now(),
                                            LEMMA=info_data.get("LEMMA"),
                                            SAMPLE=info_data.get("SAMPLE"), FRAME_ID=info_data.get("FRAME_ID"),
                                            ELEMENT_ID=info_data.get("ELEMENT_ID"))
        frame_element.frames.append(frame)
        db.session.add(frame_element)
        db.session.add(element_sample)
        db.session.commit()

        set_data_log(DATA=info_data.get("FRAME_ID"), MESSAGE="Frame关联Element", ACTION="Element", LEVEL="INFO")
        return jsonify({'code': 0, 'msg': '添加成功', 'data': {}})
    except:
        set_data_log(DATA=info_data.get("FRAME_ID"), MESSAGE="Frame关联Element失败", ACTION="Element", LEVEL="ERROR")
        return jsonify({'code': 1, 'msg': '网络异常，添加失败', 'data': {}})


@controllers.route('{}/delete!delete_frame_element'.format(URL_PREFIX), methods=['POST'])
@login_required
def delete_frame_element():
    """
    删除Frame和Element关联
    :return:
    """
    info_data = json.loads(request.get_data())
    frame = Frame.query.get(info_data.get("FRAME_ID"))

    if info_data.get("ID_LIST") and frame.frameElements:
        sample_id_list, element_id_list = list(), list()
        for value in info_data.get("ID_LIST"):
            value = value.split("*")
            if len(value) == 2:
                element_id_list.append(value[0])
                sample_id_list.append(value[1])

        for element in frame.frameElements:
            if element.ID in element_id_list:
                frame.frameElements.remove(element)

        if len(sample_id_list) != 0:
            element_samples = FrameElementSample.query.filter(FrameElementSample.ID.in_(sample_id_list)).all()
            for data in element_samples:
                db.session.delete(data)

        db.session.commit()

        set_data_log(DATA=info_data.get("FRAME_ID"), MESSAGE="成功删除关联", ACTION="Element", LEVEL="INFO")
        return jsonify({'code': 0, 'msg': '成功删除关联', 'data': {}})
    else:
        set_data_log(DATA=info_data.get("FRAME_ID"), MESSAGE="删除关联异常", ACTION="Element", LEVEL="ERROR")
        return jsonify({'code': 1, 'msg': '未选中数据，删除异常', 'data': {}})


@controllers.route('{}/delete!delete_element_by_id'.format(URL_PREFIX), methods=['POST'])
@login_required
def delete_element_by_id():
    info_data = json.loads(request.get_data())

    id_list = []
    for element_type in info_data:
        id_list.append(element_type.get("ID"))

    if len(id_list) != 0:
        elements = FrameElement.query.filter(FrameElement.ID.in_(id_list)).all()
        for element in elements:
            if element.elementSamples:
                for element_sample in element.elementSamples:
                    db.session.delete(element_sample)
            element.frames.clear()
            db.session.delete(element)
            set_data_log(DATA=element.DEF, MESSAGE="删除成功", ACTION="ElementType", LEVEL="INFO")

        return jsonify({'code': 0, 'msg': '', 'data': {}})
    else:
        set_data_log(DATA="", MESSAGE="删除异常", ACTION="ElementType", LEVEL="ERROR")
        return jsonify({'code': 1, 'msg': '未选中数据，删除异常', 'data': {}})


@controllers.route('{}/delete!delete_element_type'.format(URL_PREFIX), methods=['POST'])
@login_required
def delete_element_type():
    info_data = json.loads(request.get_data())

    id_list = []
    for element_type in info_data:
        id_list.append(element_type.get("ID"))

    if len(id_list) != 0:
        element_types = FrameElementType.query.filter(FrameElementType.ID.in_(id_list)).all()
        for data in element_types:
            db.session.delete(data)
            set_data_log(DATA=data.NAME, MESSAGE="删除成功", ACTION="ElementType", LEVEL="INFO")

        return jsonify({'code': 0, 'msg': '', 'data': {}})
    else:
        set_data_log(DATA="", MESSAGE="删除异常", ACTION="ElementType", LEVEL="ERROR")
        return jsonify({'code': 1, 'msg': '未选中数据，删除异常', 'data': {}})


@controllers.route('{}/update!element_type_info'.format(URL_PREFIX), methods=['POST'])
@login_required
def update_element_type_info():
    info_data = json.loads(request.get_data())

    element_type = FrameElementType.query.filter_by(ID=info_data.get("ID")).update(info_data)

    if element_type == 1:
        db.session.commit()

        set_data_log(DATA=info_data.get("ID"), MESSAGE="更新成功", ACTION="ElementType", LEVEL="INFO")
        return jsonify({'code': 0, 'msg': '更新成功', 'data': {}})
    else:
        set_data_log(DATA=info_data.get("ID"), MESSAGE="信息更新失败", ACTION="ElementType", LEVEL="ERROR")
        return jsonify({'code': 1, 'msg': '信息更新失败', 'data': {}})


@controllers.route('{}/update!element_info'.format(URL_PREFIX), methods=['POST'])
@login_required
def update_element_info():
    """
    更新Element信息
    :return:
    """
    info_data = json.loads(request.get_data())
    element_sample_info = {"LEMMA": info_data.get("LEMMA"), "SAMPLE": info_data.get("SAMPLE")}
    sample_id = info_data.get("SAMPLE_ID")
    del info_data["LEMMA"]
    del info_data["SAMPLE"]
    del info_data["SAMPLE_ID"]
    FrameElementSample.query.filter_by(ID=sample_id).update(element_sample_info)
    element = FrameElement.query.filter_by(ID=info_data.get("ID")).update(info_data)

    if element == 1:
        db.session.commit()

        set_data_log(DATA=info_data.get("ID"), MESSAGE="更新成功", ACTION="Element", LEVEL="INFO")
        return jsonify({'code': 0, 'msg': '更新成功', 'data': {}})
    else:
        set_data_log(DATA=info_data.get("ID"), MESSAGE="信息更新失败", ACTION="Element", LEVEL="ERROR")
        return jsonify({'code': 1, 'msg': '信息更新失败', 'data': {}})


# ==============================Verb相关================================
@controllers.route('{}/get!get_all_frame_with_verb'.format(URL_PREFIX), methods=['GET'])
def get_all_frame_with_verb():
    info_data = request.args.to_dict()
    try:
        frames = Frame.query.get(ROOT_NODE_ID)
        frame, _ = get_frame_tree(frames, if_with_verb=True, spread_id=info_data.get("spreadId", ""))

        return jsonify({'code': 0, 'msg': '', 'data': [frame]})
    except:
        return jsonify({'code': 1, 'msg': '网络异常，加载失败', 'data': [{}]})


@controllers.route('{}/add!add_verb'.format(URL_PREFIX), methods=['POST'])
@login_required
def add_verb():
    info_data = json.loads(request.get_data())
    try:
        frame = Frame.query.get(info_data.get("FRAME_ID"))
        if frame.verbs.filter_by(NAME=info_data.get("NAME")).scalar() is not None:
            return jsonify({'code': 1, 'msg': '该Verb已存在当前Frame中，请勿重复添加', 'data': {}})

        verb = Verb(ID=uuid.uuid1(), CREATE_DATETIME=datetime.now(), UPDATE_DATETIME=datetime.now(),
                    NAME=info_data.get("NAME"), PIN_YIN=info_data.get("PIN_YIN"),
                    FREQUENCY=info_data.get("FREQUENCY"), FRAMES_ID=info_data.get("FRAME_ID"))

        db.session.add(verb)
        db.session.commit()

        set_data_log(DATA=info_data.get("NAME"), MESSAGE="添加成功", ACTION="Verb", LEVEL="INFO")
        return jsonify({'code': 0, 'msg': '添加成功', 'data': {}})
    except:
        set_data_log(DATA=info_data.get("NAME"), MESSAGE="添加失败", ACTION="Verb", LEVEL="ERROR")
        return jsonify({'code': 1, 'msg': '网络异常，添加失败', 'data': {}})


@controllers.route('{}/update!verb_basic_info'.format(URL_PREFIX), methods=['POST'])
@login_required
def update_verb_basic_info():
    info_data = json.loads(request.get_data())
    verb = Verb.query.filter_by(ID=info_data.get("ID")).update(info_data)

    if verb == 1:
        db.session.commit()
        set_data_log(DATA=info_data.get("ID"), MESSAGE="更新成功", ACTION="Verb", LEVEL="INFO")
        return jsonify({'code': 0, 'msg': '更新成功', 'data': {}})
    else:
        set_data_log(DATA=info_data.get("ID"), MESSAGE="信息更新失败", ACTION="Verb", LEVEL="ERROR")
        return jsonify({'code': 1, 'msg': '信息更新失败', 'data': {}})


@controllers.route('{}/delete!delete_verb_by_id'.format(URL_PREFIX), methods=['POST'])
@login_required
def delete_verb_by_id():
    info_data = json.loads(request.get_data())
    try:
        verb = Verb.query.get(info_data.get("ID"))
        for pattern in verb.patterns:
            for sample in pattern.samples:
                db.session.delete(sample)
            db.session.delete(pattern)

        db.session.delete(verb)

        set_data_log(DATA=verb.NAME, MESSAGE="删除成功", ACTION="Verb", LEVEL="INFO")
        return jsonify({'code': 0, 'msg': '删除成功', 'data': {}})
    except:
        set_data_log(DATA="", MESSAGE="删除成功", ACTION="Verb", LEVEL="ERROR")
        return jsonify({'code': 1, 'msg': '网络异常，删除失败', 'data': {}})


# ==============================VerbPattern相关================================
@controllers.route('{}/add!add_verb_pattern'.format(URL_PREFIX), methods=['POST'])
@login_required
def add_verb_pattern():
    info_data = json.loads(request.get_data())
    try:
        verb = Verb.query.get(info_data.get("VERB_ID"))
        if verb.patterns.filter_by(PATTERN=info_data.get("PATTERN")).scalar() is not None:
            return jsonify({'code': 1, 'msg': '该Pattern已存在当前Verb中，请勿重复添加', 'data': {}})

        verb_pattern = VerbPattern(ID=uuid.uuid1(), CREATE_DATETIME=datetime.now(), UPDATE_DATETIME=datetime.now(),
                                   CONSTRUCTION=info_data.get("CONSTRUCTION"), PATTERN=info_data.get("PATTERN"),
                                   VERB_ID=info_data.get("VERB_ID"))

        db.session.add(verb_pattern)
        db.session.commit()

        set_data_log(DATA=info_data.get("PATTERN"), MESSAGE="添加成功", ACTION="VerbPattern", LEVEL="INFO")
        return jsonify({'code': 0, 'msg': '添加成功', 'data': {}})
    except:
        set_data_log(DATA=info_data.get("PATTERN"), MESSAGE="添加失败", ACTION="VerbPattern", LEVEL="ERROR")
        return jsonify({'code': 1, 'msg': '网络异常，添加失败', 'data': {}})


@controllers.route('{}/delete!delete_verb_pattern_by_id'.format(URL_PREFIX), methods=['POST'])
@login_required
def delete_verb_pattern_by_id():
    info_data = json.loads(request.get_data())
    try:
        ver_pattern = VerbPattern.query.get(info_data.get("ID"))
        for data in ver_pattern.samples:
            db.session.delete(data)

        db.session.delete(ver_pattern)

        set_data_log(DATA=ver_pattern.PATTERN, MESSAGE="删除成功", ACTION="VerbPattern", LEVEL="INFO")
        return jsonify({'code': 0, 'msg': '删除成功', 'data': {}})
    except:
        set_data_log(DATA="", MESSAGE="删除成功", ACTION="VerbPattern", LEVEL="ERROR")
        return jsonify({'code': 1, 'msg': '网络异常，删除失败', 'data': {}})


@controllers.route('{}/update!verb_pattern_info'.format(URL_PREFIX), methods=['POST'])
@login_required
def update_verb_pattern_info():
    info_data = json.loads(request.get_data())
    verb_pattern = VerbPattern.query.filter_by(ID=info_data.get("ID")).update(info_data)

    if verb_pattern == 1:
        db.session.commit()
        set_data_log(DATA=info_data.get("ID"), MESSAGE="更新成功", ACTION="VerbPattern", LEVEL="INFO")
        return jsonify({'code': 0, 'msg': '更新成功', 'data': {}})
    else:
        set_data_log(DATA=info_data.get("ID"), MESSAGE="信息更新失败", ACTION="VerbPattern", LEVEL="ERROR")
        return jsonify({'code': 1, 'msg': '信息更新失败', 'data': {}})


@controllers.route('{}/add!add_verb_pattern_sample'.format(URL_PREFIX), methods=['POST'])
@login_required
def add_verb_pattern_sample():
    try:
        info_data = json.loads(request.get_data())
        whole_re = re.compile(r'<[p]+.*?>(.*?)</[p]*?>', re.S)
        match_re = re.compile(r'[/](.*?)[]]', re.S)
        temp_list = re.findall(whole_re, info_data.get("CONTENT"))
        if not temp_list:
            temp_list.append(info_data.get("CONTENT"))

        verb = Verb.query.get(info_data.get("verbId"))
        pattern_dict = dict()
        if verb.patterns:
            for pattern in verb.patterns:
                pattern_dict[pattern.PATTERN] = pattern.ID

        sample_list = list()
        for temp in temp_list:
            element_list = re.findall(match_re, temp)
            pattern_str = "[" + "]-[".join(element_list) + "]"
            if not pattern_dict.get(pattern_str, None):
                pattern_id = uuid.uuid1()
                pattern_temp = VerbPattern(ID=pattern_id, CREATE_DATETIME=datetime.now(),
                                           UPDATE_DATETIME=datetime.now(),
                                           CONSTRUCTION="None", PATTERN=pattern_str, VERB_ID=info_data.get("verbId"))
                db.session.add(pattern_temp)
                pattern_dict[pattern_str] = pattern_id
                sample_list.append(
                    {"ID": uuid.uuid1(), "CREATE_DATETIME": datetime.now(), "UPDATE_DATETIME": datetime.now(),
                     "CONTENT": temp, "VERB_PATTERN_ID": pattern_id})
            else:
                sample_list.append(
                    {"ID": uuid.uuid1(), "CREATE_DATETIME": datetime.now(), "UPDATE_DATETIME": datetime.now(),
                     "CONTENT": temp, "VERB_PATTERN_ID": pattern_dict.get(pattern_str)})

        db.session.execute(Sample.__table__.insert(), sample_list)
        db.session.commit()

        set_data_log(DATA=info_data.get("VERB_PATTERN_ID"), MESSAGE="添加成功", ACTION="VerbPattern", LEVEL="INFO")
        return jsonify({'code': 0, 'msg': '添加成功', 'data': {}})
    except:
        set_data_log(DATA="", MESSAGE="添加失败", ACTION="VerbPattern", LEVEL="ERROR")
        return jsonify({'code': 1, 'msg': '网络异常，添加失败', 'data': {}})


@controllers.route('{}/delete!delete_verb_pattern_sample'.format(URL_PREFIX), methods=['POST'])
@login_required
def delete_verb_pattern_sample():
    info_data = json.loads(request.get_data())

    if len(info_data) != 0:
        samples = Sample.query.filter(Sample.ID.in_(info_data)).all()
        for data in samples:
            db.session.delete(data)
            set_data_log(DATA=data.ID, MESSAGE="删除成功", ACTION="Sample", LEVEL="INFO")
        return jsonify({'code': 0, 'msg': '删除成功', 'data': {}})

    else:
        set_data_log(DATA="", MESSAGE="删除异常", ACTION="Sample", LEVEL="ERROR")
        return jsonify({'code': 1, 'msg': '未选中数据，删除异常', 'data': {}})


@controllers.route('{}/update!verb_pattern_sample'.format(URL_PREFIX), methods=['POST'])
@login_required
def update_verb_pattern_sample():
    info_data = json.loads(request.get_data())
    match_re = re.compile(r'[/](.*?)[]]', re.S)
    element_list = re.findall(match_re, info_data.get("CONTENT"))
    pattern_str = "[" + "]-[".join(element_list) + "]"
    sample_temp = Sample.query.get(info_data.get("ID"))
    pattern_id = None
    if sample_temp.verbPattern.PATTERN != pattern_str:
        verb = Verb.query.get(info_data.get("VERB_ID"))
        if verb.patterns:
            for pattern in verb.patterns:
                if pattern.PATTERN == pattern_str:
                    pattern_id = pattern.ID
                    break
        if not pattern_id:
            pattern_id = uuid.uuid1()
            new_pattern = VerbPattern(ID=pattern_id, CREATE_DATETIME=datetime.now(), UPDATE_DATETIME=datetime.now(),
                                      CONSTRUCTION="", PATTERN=pattern_str, VERB_ID=info_data.get("VERB_ID"))
            db.session.add(new_pattern)

    del info_data["VERB_ID"]
    if pattern_id:
        info_data["VERB_PATTERN_ID"] = pattern_id
    sample = Sample.query.filter_by(ID=info_data.get("ID")).update(info_data)

    if sample == 1:
        db.session.commit()
        set_data_log(DATA=info_data.get("ID"), MESSAGE="更新成功", ACTION="Sample", LEVEL="INFO")
        return jsonify({'code': 0, 'msg': '更新成功', 'data': {}})
    else:
        set_data_log(DATA=info_data.get("ID"), MESSAGE="信息更新失败", ACTION="Sample", LEVEL="ERROR")
        return jsonify({'code': 1, 'msg': '信息更新失败', 'data': {}})
