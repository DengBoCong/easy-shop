import json
import uuid
from datetime import datetime
from .. import db
from . import controllers
from ..models import *
from flask import request, redirect, url_for
from flask import jsonify
from flask_login import current_user, logout_user, login_required
from sqlalchemy import or_, and_
from ..setting import PAGE_LIMIT

URL_PREFIX = "/user"


@controllers.route('{}/update!user_info'.format(URL_PREFIX), methods=['POST'])
@login_required
def update_user_info():
    info_data = json.loads(request.get_data())

    user = User.query.filter_by(EMAIL=info_data.get("EMAIL")).update(info_data)

    if user == 1:
        db.session.commit()

        return jsonify({'code': 0, 'msg': '更新成功', 'data': {}})
    else:
        return jsonify({'code': 1, 'msg': '信息更新失败', 'data': {}})


@controllers.route('{}/update!user_pwd'.format(URL_PREFIX), methods=['POST'])
@login_required
def update_user_pwd():
    info_data = json.loads(request.get_data())
    user = User.query.filter_by(EMAIL=current_user.EMAIL).first()

    if user is not None:
        if user.check_password(info_data.get("oldPassword").encode('utf-8')):
            logout_user()
            online = OnLine.query.filter_by(ACCESS_TOKEN=info_data.get('access_token')).first()
            online.IF_ONLINE = False
            user.password = info_data.get("repassword")
            db.session.commit()
            return jsonify({'code': 0, 'msg': '修改成功，请重新登录', 'data': {}})
        else:
            return jsonify({'code': 1, 'msg': '密码错误，更新失败', 'data': {}})
    else:
        return jsonify({'code': 1, 'msg': '网络异常，请重试', 'data': {}})


@controllers.route('{}/get!user_list'.format(URL_PREFIX), methods=['GET'])
@login_required
def user_list():
    info_data = request.args.to_dict()
    page = int(info_data.get("page", 1))
    limit = int(info_data.get("limit", PAGE_LIMIT))
    try:
        users = User.query.order_by(User.NAME.asc()).all()
        start = (page - 1) * limit
        users_list = []
        for user in users:
            user_json = user.to_json()
            user_json["ROLE_NAME"] = user.roles.NAME if user.roles is not None else "未分配"
            user_json["ROLE_ID"] = user.roles.ID if user.roles is not None else ""
            users_list.append(user_json)
        count = len(users_list)
    except:
        return jsonify({'code': 1, 'msg': '网络异常，加载失败', 'count': '0', 'data': [{}]})

    return jsonify({'code': 0, 'msg': '', 'count': count, 'data': users_list[start:page * limit]})


@controllers.route('{}/get!user_list_filter_by_param'.format(URL_PREFIX), methods=['GET'])
@login_required
def user_list_filter_by_param():
    info_data = request.args.to_dict()
    try:
        users = User.query.filter(and_(User.EMAIL.like("%" + info_data.get("EMAIL", "") + "%"),
                                       User.PHONE.like("%" + info_data.get("PHONE", "") + "%"),
                                       User.NAME.like("%" + info_data.get("NAME", "") + "%"))).all()

        users_list = []
        for user in users:
            user_json = user.to_json()
            user_json["ROLE_NAME"] = user.roles.NAME if user.roles is not None else "未分配"
            user_json["ROLE_ID"] = user.roles.ID if user.roles is not None else ""
            users_list.append(user_json)
        count = len(users_list)
    except:
        return jsonify({'code': 1, 'msg': '网络异常，加载失败', 'count': '0', 'data': [{}]})

    return jsonify({'code': 0, 'msg': '', 'count': count, 'data': users_list})


@controllers.route('{}/add!add_user'.format(URL_PREFIX), methods=['POST'])
@login_required
def add_user():
    info_data = json.loads(request.get_data())
    if info_data.get("file", None):
        del info_data["file"]
    try:
        email_user = User.query.filter_by(EMAIL=info_data.get("EMAIL")).all()
        phone_user = User.query.filter_by(PHONE=info_data.get("PHONE")).all()
        name_user = User.query.filter_by(NAME=info_data.get("NAME")).all()

        if len(email_user) != 0:
            return jsonify({'code': 1, 'msg': '邮箱重复，请重新填写', 'data': {}})
        elif info_data.get("PHONE") != "00000000000" and len(phone_user) != 0:
            return jsonify({'code': 1, 'msg': '手机号重复，请重新填写', 'data': {}})
        elif info_data.get("NAME") != "未署名" and len(name_user) != 0:
            return jsonify({'code': 1, 'msg': '名称重复，请重新填写', 'data': {}})
        else:
            user = User(ID=uuid.uuid1(), EMAIL=info_data.get("EMAIL"), PHONE=info_data.get("PHONE", "00000000000"),
                        NAME=info_data.get("NAME", "未署名"), IF_LOGIN=bool(info_data.get("IF_LOGIN", 0)),
                        PHOTO=info_data.get("PHOTO", "/static/img/default_avatar.jpg"), SEX=info_data.get("SEX", "0"),
                        WE_CHAT=info_data.get("WE_CHAT", ""), QQ=info_data.get("QQ", ""),
                        DESCRIPTION=info_data.get("DESCRIPTION", ""), UPDATE_DATETIME=datetime.now(),
                        ROLE_ID=info_data.get("ROLE_ID", ""), LAST_DATETIME=datetime.now())
            db.session.add(user)
            db.session.commit()
            return jsonify({'code': 0, 'msg': '添加成功', 'data': {}})
    except:
        return jsonify({'code': 1, 'msg': '网络异常，添加失败', 'data': {}})


@controllers.route('{}/delete!delete_user'.format(URL_PREFIX), methods=['POST'])
@login_required
def delete_user():
    info_data = json.loads(request.get_data())

    id_list = []
    for user in info_data:
        id_list.append(user.get("ID"))

    if len(id_list) != 0:
        users = User.query.filter(User.ID.in_(id_list)).all()
        for data in users:
            db.session.delete(data)

        return jsonify({'code': 0, 'msg': '', 'data': {}})

    else:
        return jsonify({'code': 1, 'msg': '未选中数据，删除异常', 'data': {}})
