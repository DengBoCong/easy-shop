import json
import uuid
from . import controllers
from .. import db
from ..models import *
from datetime import datetime
from flask import request
from flask import jsonify
from flask_login import login_required, current_user
from sqlalchemy import or_, and_
from ..setting import USER_NODE_ID, ROOT_NODE_ID
from ..utils import *

URL_PREFIX = "/label"


@controllers.route('{}/get!get_all_frame_for_label'.format(URL_PREFIX), methods=['GET'])
@login_required
def get_all_frame_for_label():
    try:
        frames = Frame.query.filter_by(USER_ID=current_user.ID).all()
        frames_list = get_user_frame_tree(frames=frames, if_with_verb=False)

        return jsonify({'code': 0, 'msg': '', 'data': frames_list})
    except:
        return jsonify({'code': 1, 'msg': '网络异常，加载失败', 'data': [{}]})


# ==============================标注与审核相关================================
@controllers.route('{}/get!get_all_user_frame'.format(URL_PREFIX), methods=['GET'])
@login_required
def get_all_user_frame():
    try:
        frames = Frame.query.get(USER_NODE_ID)
        frame = get_frame_tree_for_review(frames)

        return jsonify({'code': 0, 'msg': '', 'data': [frame]})
    except:
        return jsonify({'code': 1, 'msg': '网络异常，加载失败', 'data': [{}]})


@controllers.route('{}/add!add_user_frame'.format(URL_PREFIX), methods=['POST'])
@login_required
def add_user_frame():
    try:
        info_data = json.loads(request.get_data())
        name_frame = Frame.query.filter_by(NAME=info_data.get("NAME")).all()

        if len(name_frame) != 0:
            frames = Frame.query.filter_by(USER_ID=current_user.ID).all()
            frame_data = get_user_frame_tree(frames=frames)

            return jsonify({'code': 0, 'msg': '名称重复，请重新填写', 'data': frame_data})
        elif info_data.get("IF_THIRD") == 1:
            frames = Frame.query.filter_by(USER_ID=current_user.ID).all()
            frame_data = get_user_frame_tree(frames=frames)
            return jsonify({'code': 0, 'msg': 'Frame最多三级', 'data': frame_data})
        else:
            frame = Frame(ID=uuid.uuid1(), CREATE_DATETIME=datetime.now(), UPDATE_DATETIME=datetime.now(),
                          NAME="未命名", FRAME_TYPE="Archi", PARENT_ID=info_data.get("PARENT_ID"))
            db.session.add(frame)
            db.session.commit()

            frames = Frame.query.filter_by(USER_ID=current_user.ID).all()
            frame_data = get_user_frame_tree(frames=frames)

            set_data_log(DATA="未命名", MESSAGE="初始化添加成功", ACTION="Frame", LEVEL="INFO")
            return jsonify({'code': 0, 'msg': '添加成功', 'data': frame_data})
    except:
        frames = Frame.query.filter_by(USER_ID=current_user.ID).all()
        frame_data = get_user_frame_tree(frames=frames)

        set_data_log(DATA="未命名", MESSAGE="初始化添加失败", ACTION="Frame", LEVEL="ERROR")
        return jsonify({'code': 1, 'msg': '网络异常，添加失败，请重新刷新', 'data': frame_data})


@controllers.route('{}/add!add_user_frame_manage'.format(URL_PREFIX), methods=['POST'])
@login_required
def add_user_frame_manage():
    try:
        info_data = json.loads(request.get_data())
        name_frame = Frame.query.filter_by(NAME=info_data.get("NAME")).all()

        if len(name_frame) != 0:
            frames = Frame.query.get(USER_NODE_ID)
            frame_data, _ = get_frame_tree_for_review(frames, if_with_verb=True, spread_id=info_data.get("PARENT_ID"))

            return jsonify({'code': 0, 'msg': '名称重复，请重新填写', 'data': {'frame': [frame_data], 'newId': 'null'}})
        elif info_data.get("IF_THIRD") == 1:
            frames = Frame.query.get(USER_NODE_ID)
            frame_data, _ = get_frame_tree_for_review(frames, if_with_verb=True, spread_id=info_data.get("PARENT_ID"))
            return jsonify({'code': 0, 'msg': 'Frame最多三级', 'data': {'frame': [frame_data], 'newId': 'null'}})
        else:
            new_id = uuid.uuid1()
            frame = Frame(ID=new_id, CREATE_DATETIME=datetime.now(), UPDATE_DATETIME=datetime.now(),
                          NAME="未命名", FRAME_TYPE="Archi", PARENT_ID=info_data.get("PARENT_ID"))
            db.session.add(frame)
            db.session.commit()

            frames = Frame.query.get(USER_NODE_ID)
            frame_data, _ = get_frame_tree_for_review(frames, if_with_verb=True, spread_id=info_data.get("PARENT_ID"))

            set_data_log(DATA="未命名", MESSAGE="初始化添加成功", ACTION="Frame", LEVEL="INFO")
            return jsonify({'code': 0, 'msg': '添加成功', 'data': {'frame': [frame_data], 'newId': new_id}})
    except:
        frames = Frame.query.get(USER_NODE_ID)
        frame_data = get_frame_tree(frames)

        set_data_log(DATA="未命名", MESSAGE="初始化添加失败", ACTION="Frame", LEVEL="ERROR")
        return jsonify({'code': 1, 'msg': '网络异常，添加失败，请重新刷新', 'data': {'frame': [frame_data], 'newId': 'null'}})


@controllers.route('{}/delete!delete_user_frame'.format(URL_PREFIX), methods=['POST'])
@login_required
def delete_user_frame_by_id():
    info_data = json.loads(request.get_data())
    frame = Frame.query.get(info_data.get("ID"))

    if frame is not None:
        delete_user_frame_and_sub(frame.child)
        db.session.delete(frame)

        frames = Frame.query.filter_by(USER_ID=current_user.ID).all()
        frame_data = get_user_frame_tree(frames=frames)

        set_data_log(DATA=frame.NAME, MESSAGE="删除成功", ACTION="Frame", LEVEL="INFO")
        return jsonify({'code': 0, 'msg': '删除成功', 'data': frame_data})
    else:
        frames = Frame.query.filter_by(USER_ID=current_user.ID).all()
        frame_data = get_user_frame_tree(frames=frames)

        set_data_log(DATA=frame.NAME, MESSAGE="删除异常", ACTION="Frame", LEVEL="ERROR")
        return jsonify({'code': 1, 'msg': '删除异常', 'data': frame_data})


@controllers.route('{}/delete!delete_user_frame_manage'.format(URL_PREFIX), methods=['POST'])
@login_required
def delete_user_frame_by_id_manage():
    info_data = json.loads(request.get_data())
    frame = Frame.query.get(info_data.get("ID"))

    if frame is not None:
        delete_user_frame_and_sub(frame.child)
        for verb in frame.verbs:
            db.session.delete(verb)
        frame_samples = FrameElementSample.query.filter_by(FRAME_ID=frame.ID).all()
        for sample in frame_samples:
            db.session.delete(sample)
        db.session.delete(frame)

        frames = Frame.query.get(USER_NODE_ID)
        frame, _ = get_frame_tree_for_review(frames)

        set_data_log(DATA=frame["title"], MESSAGE="删除成功", ACTION="Frame", LEVEL="INFO")
        return jsonify({'code': 0, 'msg': '删除成功', 'data': [frame]})
    else:
        frames = Frame.query.get(USER_NODE_ID)
        frame, _ = get_frame_tree_for_review(frames)

        set_data_log(DATA=frame.NAME, MESSAGE="删除异常", ACTION="Frame", LEVEL="ERROR")
        return jsonify({'code': 1, 'msg': '删除异常', 'data': [frame]})


def delete_user_frame_and_sub(frame):
    if len(frame) == 0:
        return

    for sub_frame in frame:
        for verb in sub_frame.verbs:
            db.session.delete(verb)
        frame_samples = FrameElementSample.query.filter_by(FRAME_ID=sub_frame.ID).all()
        for sample in frame_samples:
            db.session.delete(sample)
        delete_user_frame_and_sub(sub_frame.child)
        db.session.delete(sub_frame)


@controllers.route('{}/update!user_frame_basic_info'.format(URL_PREFIX), methods=['POST'])
@login_required
def update_user_frame_basic_info():
    info_data = json.loads(request.get_data())
    if info_data.get("PARENT_ID") != USER_NODE_ID:
        parent_frame = Frame.query.get(info_data.get("PARENT_ID"))
        if parent_frame.child:
            return jsonify({'code': 1, 'msg': '该线上的Frame存在子级Frame，不允许添加Verb', 'data': {}})
        else:
            Verb.query.filter(Verb.FRAMES_ID == info_data.get("ID")).update(
                {Verb.FRAMES_ID: info_data.get("PARENT_ID")})

    del info_data["PARENT_ID"]
    frame = Frame.query.filter_by(ID=info_data.get("ID")).update(info_data)
    if frame == 1:
        db.session.commit()
        set_data_log(DATA=info_data.get("NAME"), MESSAGE="更新成功", ACTION="Frame", LEVEL="INFO")
        return jsonify({'code': 0, 'msg': '更新成功', 'data': {}})
    else:
        set_data_log(DATA=info_data.get("ID"), MESSAGE="信息更新失败", ACTION="Frame", LEVEL="ERROR")
        return jsonify({'code': 1, 'msg': '信息更新失败', 'data': {}})


@controllers.route('{}/get!get_all_user_frame_where_not_third'.format(URL_PREFIX), methods=['GET'])
@login_required
def get_all_user_frame_where_not_third():
    try:
        # frames = Frame.query.get(ROOT_NODE_ID)
        user_frames = Frame.query.get(USER_NODE_ID)
        # frame = get_frame_not_third(frames)
        user_frame = get_frame_not_third(user_frames)

        return jsonify({'code': 0, 'msg': '', 'data': user_frame})  # frame + user_frame
    except:
        return jsonify({'code': 1, 'msg': '网络异常，加载失败', 'data': [{}]})


@controllers.route('{}/get!get_all_user_frame_for_select'.format(URL_PREFIX), methods=['GET'])
@login_required
def get_all_user_frame_for_select():
    try:
        frames = Frame.query.get(ROOT_NODE_ID)
        user_frames = Frame.query.get(USER_NODE_ID)
        frame_list = list()
        for frame in frames.child:
            frame_list += get_frame_with_third(frame)
        for frame in user_frames.child:
            frame_list += get_frame_with_third(frame)

        return jsonify({'code': 0, 'msg': '', 'data': frame_list})
    except:
        return jsonify({'code': 1, 'msg': '网络异常，加载失败', 'data': [{}]})


# ==============================标注与审核Verb相关================================
@controllers.route('{}/get!get_all_user_frame_with_verb'.format(URL_PREFIX), methods=['GET'])
@login_required
def get_all_user_frame_with_verb():
    info_data = request.args.to_dict()
    try:
        frames = Frame.query.get(USER_NODE_ID)
        frame, _ = get_frame_tree_for_review(frames, if_with_verb=True, spread_id=info_data.get("spreadId", ""))

        return jsonify({'code': 0, 'msg': '', 'data': [frame]})
    except:
        return jsonify({'code': 1, 'msg': '网络异常，加载失败', 'data': [{}]})


@controllers.route('{}/get!get_all_user_frame_with_verb_for_label'.format(URL_PREFIX), methods=['GET'])
@login_required
def get_all_user_frame_with_verb_for_label():
    info_data = request.args.to_dict()
    try:
        verbs = Verb.query.filter_by(USER_ID=current_user.ID).all()
        frame_dict = dict()
        for verb in verbs:
            temp_frame = Frame.query.get(verb.TEMP_FRAME_ID)
            temp_frame_id = temp_frame.ID
            if not frame_dict.get(temp_frame_id, None):
                frame_dict[temp_frame_id] = {"id": temp_frame_id, "title": temp_frame.NAME,
                                             "children": [], "if_verb": 0, "spread": False}
            spread = False
            if verb.ID == info_data.get("spreadId", ""):
                spread = True
            frame_dict[temp_frame_id]["children"].append({
                "id": verb.ID, "title": "{}{}".format(verb.NAME, "(已提交)" if verb.IF_FINISH == "1" else ""),
                "if_verb": 1, "spread": spread
            })
            frame_dict[temp_frame_id]["spread"] = (spread or frame_dict[temp_frame_id]["spread"])
        frame_list = [value for value in frame_dict.values()]

        return jsonify({'code': 0, 'msg': '', 'data': frame_list})
    except:
        return jsonify({'code': 1, 'msg': '网络异常，加载失败', 'data': [{}]})


@controllers.route('{}/add!add_frame_for_label'.format(URL_PREFIX), methods=['POST'])
@login_required
def add_frame_for_label():
    try:
        info_data = json.loads(request.get_data())
        name_frame = Frame.query.filter_by(NAME=info_data.get("NAME")).all()

        if len(name_frame) != 0:
            frames = Frame.query.filter_by(USER_ID=current_user.ID).all()
            frames_list = get_user_frame_tree(frames=frames)

            return jsonify({'code': 0, 'msg': '名称重复，请重新填写', 'data': frames_list})
        elif info_data.get("IF_THIRD") == 1:
            frames = Frame.query.filter_by(USER_ID=current_user.ID).all()
            frames_list = get_user_frame_tree(frames=frames)
            return jsonify({'code': 0, 'msg': 'Frame最多三级', 'data': frames_list})
        else:
            frame = Frame(ID=uuid.uuid1(), CREATE_DATETIME=datetime.now(), UPDATE_DATETIME=datetime.now(),
                          NAME="未命名", FRAME_TYPE="Archi", PARENT_ID=info_data.get("PARENT_ID"))
            db.session.add(frame)
            db.session.commit()

            frames = Frame.query.filter_by(USER_ID=current_user.ID).all()
            frames_list = get_user_frame_tree(frames=frames)

            set_data_log(DATA="未命名", MESSAGE="初始化添加成功", ACTION="Frame", LEVEL="INFO")
            return jsonify({'code': 0, 'msg': '添加成功', 'data': frames_list})
    except:
        frames = Frame.query.filter_by(USER_ID=current_user.ID).all()
        frames_list = get_user_frame_tree(frames=frames)

        set_data_log(DATA="未命名", MESSAGE="初始化添加失败", ACTION="Frame", LEVEL="ERROR")
        return jsonify({'code': 1, 'msg': '网络异常，添加失败，请重新刷新', 'data': frames_list})


@controllers.route('{}/delete!delete_frame_for_label'.format(URL_PREFIX), methods=['POST'])
@login_required
def delete_frame_for_label_by_id():
    info_data = json.loads(request.get_data())
    frame = Frame.query.get(info_data.get("ID"))

    if frame is not None:
        delete_user_frame_and_sub(frame.child)
        db.session.delete(frame)

        frames = Frame.query.filter_by(USER_ID=current_user.ID).all()
        frames_list = get_user_frame_tree(frames=frames)

        set_data_log(DATA=frame.NAME, MESSAGE="删除成功", ACTION="Frame", LEVEL="INFO")
        return jsonify({'code': 0, 'msg': '删除成功', 'data': frames_list})
    else:
        frames = Frame.query.filter_by(USER_ID=current_user.ID).all()
        frames_list = get_user_frame_tree(frames=frames)

        set_data_log(DATA=frame.NAME, MESSAGE="删除异常", ACTION="Frame", LEVEL="ERROR")
        return jsonify({'code': 1, 'msg': '删除异常', 'data': frames_list})


@controllers.route('{}/get!get_all_frame_select_for_label'.format(URL_PREFIX), methods=['GET'])
@login_required
def get_all_frame_select_for_label():
    try:
        frames = Frame.query.filter_by(USER_ID=current_user.ID).all()
        frames_list = get_user_frame_tree(frames=frames)

        return jsonify({'code': 0, 'msg': '', 'data': frames_list})
    except:
        return jsonify({'code': 1, 'msg': '网络异常，加载失败', 'data': [{}]})


@controllers.route('{}/update!batch_verb_basic_info'.format(URL_PREFIX), methods=['POST'])
@login_required
def update_batch_verb_basic_info():
    info_data = json.loads(request.get_data())
    verbs = Verb.query.filter(Verb.ID.in_(info_data.get("checkedData"))).update(
        {Verb.USER_ID: info_data["USER_ID"], Verb.TEMP_FRAME_ID: info_data["TEMP_FRAME_ID"]}, synchronize_session=False)

    frames = Frame.query.get(USER_NODE_ID)
    frame, _ = get_frame_tree_for_review(frames=frames, if_with_verb=True, spread_id="")
    if verbs != 0:
        db.session.commit()
        return jsonify({'code': 0, 'msg': '更新成功', 'data': [frame]})
    else:
        set_data_log(DATA=info_data.get("ID"), MESSAGE="信息更新失败", ACTION="Verb", LEVEL="ERROR")
        return jsonify({'code': 1, 'msg': '信息更新失败', 'data': [frame]})
