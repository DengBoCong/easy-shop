import uuid
import json
from .. import db
from . import controllers
from ..models import *
from flask import request, redirect, url_for
from flask import jsonify
from flask_login import current_user, logout_user, login_required
from datetime import datetime
from sqlalchemy import or_, and_
from ..utils.get import get_all_role
from ..utils import set_system_log
from ..setting import PAGE_LIMIT

URL_PREFIX = "/role"


# ==============================角色相关================================

@controllers.route('{}/get!all_role_info'.format(URL_PREFIX), methods=['GET'])
@login_required
def get_all_roles():
    info_data = request.args.to_dict()
    page = int(info_data.get("page", 1))
    limit = int(info_data.get("limit", PAGE_LIMIT))
    try:
        roles = get_all_role()
    except:
        set_system_log(PATH="/api/role/get!all_role_info", ACTION="role",
                       MESSAGE="角色信息加载失败", LEVEL="ERROR")
        return jsonify({'code': 1, 'msg': '角色信息加载失败', 'data': {}})

    roles_list = []
    start = (page - 1) * limit
    for role in roles:
        roles_list.append(role.to_json())
    count = len(roles_list)

    set_system_log(PATH="/api/role/get!all_role_info", ACTION="role",
                   MESSAGE="角色信息加载成功", LEVEL="INFO")
    return jsonify({'code': 0, 'msg': '', 'count': count, 'data': {'roles': roles_list[start:page * limit]}})


@controllers.route('{}/get!role_list_filter_by_param'.format(URL_PREFIX), methods=['GET'])
@login_required
def get_role_list_filter_by_param():
    info_data = request.args.to_dict()
    try:
        roles = Role.query.filter(Role.NAME.like("%" + info_data.get("NAME", "") + "%")).all()

        roles_list = []
        for role in roles:
            role_json = role.to_json()
            roles_list.append(role_json)
        count = len(roles_list)

        set_system_log(PATH="/api/role/get!role_list_filter_by_param", ACTION="role",
                       MESSAGE="角色信息查询成功", LEVEL="INFO")
        return jsonify({'code': 0, 'msg': '', 'count': count, 'data': {'roles': roles_list}})
    except:
        set_system_log(PATH="/api/role/get!role_list_filter_by_param", ACTION="role",
                       MESSAGE="网络异常，角色信息查询失败", LEVEL="ERROR")
        return jsonify({'code': 1, 'msg': '网络异常，加载失败', 'count': '0', 'data': [{}]})


@controllers.route('{}/delete!delete_roles'.format(URL_PREFIX), methods=['POST'])
@login_required
def delete_roles():
    info_data = json.loads(request.get_data())

    id_list = []
    for role in info_data:
        id_list.append(role.get("ID"))

    if len(id_list) != 0:
        roles = Role.query.filter(Role.ID.in_(id_list)).all()
        for data in roles:
            db.session.delete(data)

        set_system_log(PATH="/api/role/delete!delete_roles", ACTION="role",
                       MESSAGE="角色删除成功", LEVEL="INFO")
        return jsonify({'code': 0, 'msg': '', 'data': {}})

    else:
        set_system_log(PATH="/api/role/delete!delete_roles", ACTION="role",
                       MESSAGE="未选中数据，角色删除异常", LEVEL="ERROR")
        return jsonify({'code': 1, 'msg': '未选中数据，删除异常', 'data': {}})


@controllers.route('{}/add!add_role'.format(URL_PREFIX), methods=['POST'])
@login_required
def add_role():
    info_data = json.loads(request.get_data())

    name_role = Role.query.filter_by(NAME=info_data.get("NAME")).all()

    if len(name_role) != 0:
        return jsonify({'code': 1, 'msg': '命名重复，请重新填写', 'data': {}})
    elif len(name_role) == 0:
        role = Role(ID=uuid.uuid1(), CREATE_DATETIME=datetime.now(), UPDATE_DATETIME=datetime.now(),
                    NAME=info_data.get("NAME"), DESCRIPTION=info_data.get("DESCRIPTION"), TYPE=1)

        db.session.add(role)
        db.session.commit()

        set_system_log(PATH="/api/role/add!add_role", ACTION="role",
                       MESSAGE="角色添加成功", LEVEL="INFO")
        return jsonify({'code': 0, 'msg': '添加成功', 'data': {}})
    else:
        set_system_log(PATH="/api/role/add!add_role", ACTION="role",
                       MESSAGE="网络异常，角色添加失败", LEVEL="ERROR")
        return jsonify({'code': 1, 'msg': '网络异常，添加失败', 'data': {}})


@controllers.route('{}/update!role_info'.format(URL_PREFIX), methods=['POST'])
@login_required
def update_role_info():
    info_data = json.loads(request.get_data())

    role = Role.query.filter_by(ID=info_data.get("ID")).update(info_data)

    if role == 1:
        db.session.commit()

        set_system_log(PATH="/api/role/update!role_info", ACTION="role",
                       MESSAGE="角色信息更新成功", LEVEL="INFO")
        return jsonify({'code': 0, 'msg': '更新成功', 'data': {}})
    else:
        set_system_log(PATH="/api/role/update!role_info", ACTION="role",
                       MESSAGE="角色信息更新失败", LEVEL="ERROR")
        return jsonify({'code': 1, 'msg': '信息更新失败', 'data': {}})


@controllers.route('{}/update!role_privilege'.format(URL_PREFIX), methods=['POST'])
@login_required
def update_role_privilege():
    info_data = json.loads(request.get_data())
    privileges = Privilege.query.filter(Privilege.ID.in_(info_data.get("privilege"))).all()
    role = Role.query.get(info_data.get("roleId"))

    if role is not None:
        role.privilege.clear()
        for privilege in privileges:
            role.privilege.append(privilege)
        db.session.commit()

        set_system_log(PATH="/api/role/update!role_privilege", ACTION="role",
                       MESSAGE="角色权限关联更新成功", LEVEL="INFO")
        return jsonify({'code': 0, 'msg': '更新成功', 'data': {}})
    else:
        set_system_log(PATH="/api/role/update!role_privilege", ACTION="role",
                       MESSAGE="角色权限关联更新失败", LEVEL="ERROR")
        return jsonify({'code': 1, 'msg': '角色权限关联更新失败', 'data': {}})


# ==============================权限相关================================

@controllers.route('{}/get!all_privilege_info'.format(URL_PREFIX), methods=['GET'])
@login_required
def get_all_privileges():
    info_data = request.args.to_dict()
    page = int(info_data.get("page", 1))
    limit = int(info_data.get("limit", PAGE_LIMIT))
    try:
        privileges = Privilege.query.order_by(Privilege.TARGET.desc()).all()
    except:
        set_system_log(PATH="/api/role/get!all_privilege_info", ACTION="role",
                       MESSAGE="权限信息加载失败", LEVEL="ERROR")
        return jsonify({'code': 1, 'msg': '权限信息加载失败', 'data': {}})

    privileges_list = []
    start = (page - 1) * limit
    for privilege in privileges:
        privilege_json = privilege.to_json()
        privileges_list.append(privilege_json)

    set_system_log(PATH="/api/role/get!all_privilege_info", ACTION="role",
                   MESSAGE="权限信息加载成功", LEVEL="INFO")
    return jsonify({'code': 0, 'msg': '', 'count': len(privileges_list), 'data': privileges_list[start:page * limit]})


@controllers.route('{}/get!all_privilege_info_with_role_check'.format(URL_PREFIX), methods=['GET'])
@login_required
def get_all_privilege_info_with_role_check():
    info_data = request.args.to_dict()
    try:
        privileges = Privilege.query.all()
        role = Role.query.get(info_data.get("parentRoleID"))
        role_privilege = [temp.ID for temp in role.privilege]
    except:
        set_system_log(PATH="/api/role/get!all_privilege_info_with_role_check", ACTION="role",
                       MESSAGE="权限信息查询失败", LEVEL="ERROR")
        return jsonify({'code': 1, 'msg': '权限信息查询失败', 'data': {}})

    privileges_list = []
    for privilege in privileges:
        privilege_json = privilege.to_json()
        if privilege.ID in role_privilege:
            privilege_json["checked"] = True
        privileges_list.append(privilege_json)

    set_system_log(PATH="/api/role/get!all_privilege_info_with_role_check", ACTION="role",
                   MESSAGE="权限信息查询成功", LEVEL="INFO")
    return jsonify({'code': 0, 'msg': '权限信息查询成功', 'data': privileges_list})


@controllers.route('{}/get!privilege_list_filter_by_param'.format(URL_PREFIX), methods=['GET'])
@login_required
def privilege_list_filter_by_param():
    info_data = request.args.to_dict()
    try:
        privileges = Privilege.query.filter(and_(Privilege.NAME.like("%" + info_data.get("NAME", "") + "%"),
                                                 Privilege.TARGET.like("%" + info_data.get("TARGET", "") + "%"),
                                                 Privilege.ACTION.like("%" + info_data.get("ACTION", "") + "%"))).all()

        privileges_list = []
        for privilege in privileges:
            privilege_json = privilege.to_json()
            privileges_list.append(privilege_json)
        count = len(privileges_list)
    except:
        set_system_log(PATH="/api/role/get!privilege_list_filter_by_param", ACTION="role",
                       MESSAGE="权限信息查询失败", LEVEL="ERROR")
        return jsonify({'code': 1, 'msg': '网络异常，加载失败', 'count': '0', 'data': [{}]})

    set_system_log(PATH="/api/role/get!privilege_list_filter_by_param", ACTION="role",
                   MESSAGE="权限信息查询成功", LEVEL="INFO")
    return jsonify({'code': 0, 'msg': '', 'count': count, 'data': privileges_list})


@controllers.route('{}/delete!delete_privileges'.format(URL_PREFIX), methods=['POST'])
@login_required
def delete_privileges():
    info_data = json.loads(request.get_data())

    id_list = []
    for privilege in info_data:
        id_list.append(privilege.get("ID"))

    if len(id_list) != 0:
        privileges = Privilege.query.filter(Privilege.ID.in_(id_list)).all()
        for data in privileges:
            db.session.delete(data)

        set_system_log(PATH="/api/role/delete!delete_privileges", ACTION="role",
                       MESSAGE="权限信息删除成功", LEVEL="INFO")
        return jsonify({'code': 0, 'msg': '', 'data': {}})

    else:
        set_system_log(PATH="/api/role/delete!delete_privileges", ACTION="role",
                       MESSAGE="未选中数据，权限信息删除异常", LEVEL="ERROR")
        return jsonify({'code': 1, 'msg': '未选中数据，删除异常', 'data': {}})


@controllers.route('{}/add!add_privilege'.format(URL_PREFIX), methods=['POST'])
@login_required
def add_privilege():
    info_data = json.loads(request.get_data())

    name_user = Privilege.query.filter_by(NAME=info_data.get("NAME")).all()
    target_user = Privilege.query.filter_by(TARGET=info_data.get("TARGET")).all()

    if len(name_user) != 0:
        return jsonify({'code': 1, 'msg': '命名重复，请重新填写', 'data': {}})
    elif len(target_user) != 0:
        return jsonify({'code': 1, 'msg': '目标地址重复，请重新填写', 'data': {}})
    elif len(name_user) == 0 and len(target_user) == 0:
        privilege = Privilege(ID=uuid.uuid1(), CREATE_DATETIME=datetime.now(), UPDATE_DATETIME=datetime.now(),
                              NAME=info_data.get("NAME"), TARGET=info_data.get("TARGET"),
                              ACTION=info_data.get("ACTION"), DESCRIPTION=info_data.get("DESCRIPTION"),
                              ICON_CLS=info_data.get("ICON_CLS"), SORT=info_data.get("SORT"))

        db.session.add(privilege)
        db.session.commit()

        set_system_log(PATH="/api/role/add!add_privilege", ACTION="role",
                       MESSAGE="未选中数据，权限信息添加成功", LEVEL="INFO")
        return jsonify({'code': 0, 'msg': '添加成功', 'data': {}})
    else:
        set_system_log(PATH="/api/role/add!add_privilege", ACTION="role",
                       MESSAGE="未选中数据，权限信息添加失败", LEVEL="ERROR")
        return jsonify({'code': 1, 'msg': '网络异常，添加失败', 'data': {}})


@controllers.route('{}/update!privilege_info'.format(URL_PREFIX), methods=['POST'])
@login_required
def update_privilege_info():
    info_data = json.loads(request.get_data())

    privilege = Privilege.query.filter_by(ID=info_data.get("ID")).update(info_data)

    if privilege == 1:
        db.session.commit()

        set_system_log(PATH="/api/role/update!privilege_info", ACTION="role",
                       MESSAGE="权限信息更新成功", LEVEL="INFO")
        return jsonify({'code': 0, 'msg': '更新成功', 'data': {}})
    else:
        set_system_log(PATH="/api/role/update!privilege_info", ACTION="role",
                       MESSAGE="权限信息更新失败", LEVEL="ERROR")
        return jsonify({'code': 1, 'msg': '信息更新失败', 'data': {}})
