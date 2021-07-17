import uuid
import json
from . import controllers
from .. import db
from ..models import *
from datetime import datetime
from flask import request
from flask import jsonify
from flask_login import login_user, logout_user, login_required, current_user
from ..setting import PAGE_LIMIT

URL_PREFIX = "/system"


@controllers.route('{}/system_out'.format(URL_PREFIX), methods=['GET'])
def system_info():
    return jsonify({'code': 0, 'msg': '成功退出', 'data': {}})


# ==============================快捷方式相关================================

@controllers.route('{}/get!link_list'.format(URL_PREFIX), methods=['GET'])
@login_required
def link_list():
    info_data = request.args.to_dict()
    page = int(info_data.get("page", 1))
    limit = int(info_data.get("limit", PAGE_LIMIT))
    try:
        links = Link.query.all()
        start = (page - 1) * limit
        links_list = []
        for link in links:
            user_json = link.to_json()
            links_list.append(user_json)
        count = len(links_list)
    except:
        return jsonify({'code': 1, 'msg': '网络异常，加载失败', 'count': '0', 'data': [{}]})

    return jsonify({'code': 0, 'msg': '', 'count': count, 'data': links_list[start:page * limit]})


@controllers.route('{}/get!link_list_filter_by_param'.format(URL_PREFIX), methods=['GET'])
@login_required
def link_list_filter_by_param():
    info_data = request.args.to_dict()
    try:
        links = Link.query.filter(Link.NAME.like("%" + info_data.get("NAME", "") + "%")).all()

        links_list = []
        for link in links:
            user_json = link.to_json()
            links_list.append(user_json)
        count = len(links_list)
    except:
        return jsonify({'code': 1, 'msg': '网络异常，加载失败', 'count': '0', 'data': [{}]})

    return jsonify({'code': 0, 'msg': '', 'count': count, 'data': links_list})


@controllers.route('{}/add!add_link'.format(URL_PREFIX), methods=['POST'])
@login_required
def add_link():
    try:
        info_data = json.loads(request.get_data())
        name_link = Link.query.filter_by(NAME=info_data.get("NAME")).all()

        if len(name_link) != 0:
            return jsonify({'code': 1, 'msg': '名称重复，请重新填写', 'data': {}})
        else:
            link = Link(ID=uuid.uuid1(), CREATE_DATETIME=datetime.now(), UPDATE_DATETIME=datetime.now(),
                        NAME=info_data.get("NAME"), URL=info_data.get("URL"), SORT=info_data.get("SORT"),
                        ICON_CLS=info_data.get("ICON_CLS"))
            db.session.add(link)
            db.session.commit()
            return jsonify({'code': 0, 'msg': '添加成功', 'data': {}})
    except:
        return jsonify({'code': 1, 'msg': '网络异常，更新失败', 'data': {}})


@controllers.route('{}/delete!delete_link'.format(URL_PREFIX), methods=['POST'])
@login_required
def delete_link():
    info_data = json.loads(request.get_data())

    id_list = []
    for link in info_data:
        id_list.append(link.get("ID"))

    if len(id_list) != 0:
        links = Link.query.filter(Link.ID.in_(id_list)).all()
        for data in links:
            db.session.delete(data)

        return jsonify({'code': 0, 'msg': '', 'data': {}})

    else:
        return jsonify({'code': 1, 'msg': '未选中数据，删除异常', 'data': {}})


@controllers.route('{}/update!link_info'.format(URL_PREFIX), methods=['POST'])
@login_required
def update_link_info():
    info_data = json.loads(request.get_data())

    link = Link.query.filter_by(ID=info_data.get("ID")).update(info_data)

    if link == 1:
        db.session.commit()

        return jsonify({'code': 0, 'msg': '更新成功', 'data': {}})
    else:
        return jsonify({'code': 1, 'msg': '信息更新失败', 'data': {}})


# ==============================系统联系人相关相关================================
@controllers.route('{}/get!user_contacts'.format(URL_PREFIX), methods=['GET'])
@login_required
def get_user_contacts():
    info_data = request.args.to_dict()
    page = int(info_data.get("page", 1))
    limit = int(info_data.get("limit", PAGE_LIMIT))
    try:
        contacts = User.query.filter_by(IF_CONTACT=True).all()
        start = (page - 1) * limit
        contacts_list = []
        for contact in contacts:
            contact_json = contact.to_json()
            contacts_list.append(contact_json)
        count = len(contacts_list)
    except:
        return jsonify({'code': 1, 'msg': '网络异常，加载失败', 'count': '0', 'data': [{}]})

    return jsonify({'code': 0, 'msg': '', 'count': count, 'data': contacts_list[start:page * limit]})


@controllers.route('{}/set!user_contacts'.format(URL_PREFIX), methods=['POST'])
@login_required
def set_user_contacts():
    info_data = json.loads(request.get_data())
    try:
        user = User.query.filter_by(ID=info_data.get("ID")).first()
        if user is not None:
            if user.IF_CONTACT:
                return jsonify({'code': 1, 'msg': '用户已是系统联系人，请重新选择', 'data': [{}]})
            user.IF_CONTACT = True
            db.session.commit()
        else:
            return jsonify({'code': 1, 'msg': '用户不存在或已被移除，请重新选择', 'data': [{}]})
    except:
        return jsonify({'code': 1, 'msg': '网络异常，加载失败', 'data': [{}]})

    return jsonify({'code': 0, 'msg': '设置成功', 'data': {}})


@controllers.route('{}/delete!delete_contact'.format(URL_PREFIX), methods=['POST'])
@login_required
def delete_contact():
    info_data = json.loads(request.get_data())

    id_list = []
    for contact in info_data:
        id_list.append(contact.get("ID"))

    if len(id_list) != 0:
        users = User.query.filter(User.ID.in_(id_list)).all()
        for data in users:
            data.IF_CONTACT = False

        db.session.commit()
        return jsonify({'code': 0, 'msg': '', 'data': {}})

    else:
        return jsonify({'code': 1, 'msg': '未选中数据，删除异常', 'data': {}})


# ==============================系统设置================================
@controllers.route('{}/set!system_info'.format(URL_PREFIX), methods=['POST'])
@login_required
def set_system_info():
    info_data = json.loads(request.get_data())
    info_data['ALLOW_LOGIN'] = True if info_data['ALLOW_LOGIN'] == '1' else False
    info_data['IF_EMAIL'] = True if info_data['IF_EMAIL'] == '1' else False

    system = System.query.filter_by(SITE_NAME=info_data.get("SITE_NAME")).update(info_data)

    if system == 1:
        db.session.commit()

        return jsonify({'code': 0, 'msg': '更新成功', 'data': {}})
    else:
        return jsonify({'code': 1, 'msg': '信息更新失败', 'data': {}})
