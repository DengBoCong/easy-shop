import uuid
import json
from . import controllers
from .. import db
from ..models import Notice, Attachment
from datetime import datetime, timedelta
from flask import request
from flask import jsonify
from flask_login import login_required
from ..setting import PAGE_LIMIT

URL_PREFIX = "/notice"


# ==================通告手册相关=======================
@controllers.route('{}/get!get_all_notice_info'.format(URL_PREFIX), methods=['GET'])
@login_required
def get_all_notice_info():
    info_data = request.args.to_dict()
    page = int(info_data.get("page", 1))
    limit = int(info_data.get("limit", PAGE_LIMIT))
    try:
        notices = Notice.query.all()
        start = (page - 1) * limit
        notice_list = list()
        for notice in notices:
            notice_list.append(notice.to_json())
        return jsonify({'code': 0, 'msg': '退出登录', 'data': notice_list[start:page * limit]})
    except:
        return jsonify({'code': 1, 'msg': '网络异常，加载失败', 'data': {}})


@controllers.route('{}/get!get_notice_info_by_id'.format(URL_PREFIX), methods=['GET'])
@login_required
def get_notice_info_by_id():
    info_data = request.args.to_dict()
    try:
        notices = Notice.query.get(info_data.get("ID"))
        return jsonify({'code': 0, 'msg': '退出登录', 'data': notices.to_json()})
    except:
        return jsonify({'code': 1, 'msg': '网络异常，加载失败', 'data': {}})


@controllers.route('{}/add!add_notice'.format(URL_PREFIX), methods=['POST'])
@login_required
def add_notice():
    try:
        info_data = json.loads(request.get_data())
        name_notice = Notice.query.filter_by(TITLE=info_data.get("TITLE")).all()

        if len(name_notice) != 0:
            return jsonify({'code': 1, 'msg': '标题重复，请重新填写', 'data': {}})
        else:
            notice_id = uuid.uuid1()
            notice = Notice(ID=notice_id, CREATE_DATETIME=datetime.now(), UPDATE_DATETIME=datetime.now(),
                            TITLE=info_data.get("TITLE"), SUB_TITLE=info_data.get("SUB_TITLE"),
                            IF_TOP=int(info_data.get("IF_TOP")), DESCRIPTION=info_data.get("NAME"), CONTENT="")
            db.session.add(notice)
            db.session.commit()
            return jsonify({'code': 0, 'msg': '添加成功', 'data': notice_id})
    except:
        return jsonify({'code': 1, 'msg': '网络异常，更新失败', 'data': {}})


@controllers.route('{}/update!notice_info'.format(URL_PREFIX), methods=['POST'])
@login_required
def update_notice_info():
    info_data = json.loads(request.get_data())

    if info_data.get("IF_TOP", None):
        info_data["IF_TOP"] = int(info_data["IF_TOP"])
    notice = Notice.query.filter_by(ID=info_data.get("ID")).update(info_data)

    if notice == 1:
        db.session.commit()

        return jsonify({'code': 0, 'msg': '更新成功', 'data': {}})
    else:
        return jsonify({'code': 1, 'msg': '信息更新失败', 'data': {}})


@controllers.route('{}/delete!delete_notice'.format(URL_PREFIX), methods=['POST'])
@login_required
def delete_notice():
    info_data = json.loads(request.get_data())

    id_list = []
    for notice in info_data:
        id_list.append(notice.get("ID"))

    if len(id_list) != 0:
        notices = Notice.query.filter(Notice.ID.in_(id_list)).all()
        for data in notices:
            db.session.delete(data)

        return jsonify({'code': 0, 'msg': '', 'data': {}})

    else:
        return jsonify({'code': 1, 'msg': '未选中数据，删除异常', 'data': {}})


# ==================附件相关=======================
@controllers.route('{}/get!get_all_attach_info_by_notice'.format(URL_PREFIX), methods=['GET'])
@login_required
def get_all_attach_info_by_notice():
    info_data = request.args.to_dict()
    try:
        notice_info = Notice.query.get(info_data.get("noticeId"))
        attach_list = list()
        for attach in notice_info.attachments:
            attach_list.append(attach.to_json())
        return jsonify({'code': 0, 'msg': '退出登录', 'data': attach_list})
    except:
        return jsonify({'code': 1, 'msg': '网络异常，加载失败', 'data': {}})


@controllers.route('{}/delete!delete_attach'.format(URL_PREFIX), methods=['GET'])
@login_required
def delete_attach():
    info_data = request.args.to_dict()

    attach = Attachment.query.get(info_data.get("attachId"))

    if attach:
        db.session.delete(attach)
        return jsonify({'code': 0, 'msg': '删除成功', 'data': {}})

    else:
        return jsonify({'code': 1, 'msg': '删除异常', 'data': {}})
