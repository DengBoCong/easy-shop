import uuid
from . import controllers
from .. import db
from ..models import *
from datetime import datetime
from flask import request
from flask import jsonify
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy.orm import load_only

URL_PREFIX = "/init"


@controllers.route('{}/init_user'.format(URL_PREFIX), methods=['GET'])
def init_user():
    user = User()
    user.ID = uuid.uuid1()
    user.UPDATE_DATETIME = datetime.now()
    user.LAST_DATETIME = datetime.now()
    user.EMAIL = "1210212670@qq.com"
    user.password = "123456789"
    user.NAME = "超级管理员"

    # system = System()
    # system.ALLOW_LOGIN = True
    # system.COPY_RIGHT_INFO = "© Copyright 2020-2021 DengBoCong. All Rights Reserved. 赣ICP备20002291号"
    # system.SITE_NAME = "中文动词语义网"
    db.session.add(user)
    # db.session.add(system)
    db.session.commit()


@controllers.route('{}/init_public_user'.format(URL_PREFIX), methods=['GET'])
def init_public_user():
    user = User()
    user.ID = uuid.uuid1()
    user.LAST_DATETIME = datetime.now()
    user.CREATE_DATETIME = datetime.now()
    user.UPDATE_DATETIME = datetime.now()
    user.EMAIL = "210212670@qq.com"
    user.password = "123456789"
    user.NAME = "普通用户"

    privilege = Privilege.query.filter_by(TARGET="/login").all()
    role = Role()
    role.ID = uuid.uuid1()
    role.UPDATE_DATETIME = datetime.now()
    role.NAME = "普通用户"
    role.DESCRIPTION = "普通用户"
    role.ICON_CLS = "layui-icon-senior"
    role.TYPE = 1
    role.privilege = privilege

    user.roles = role
    db.session.add(role)

    db.session.add(user)
    db.session.commit()


@controllers.route('{}/init_privilege'.format(URL_PREFIX), methods=['GET'])
def init_privilege():
    p = Privilege()
    p.ID = uuid.uuid1()
    p.UPDATE_DATETIME = datetime.now()
    p.NAME = "主页"
    p.TYPE = "menu"

    p1 = Privilege()
    p1.ID = uuid.uuid1()
    p1.UPDATE_DATETIME = datetime.now()
    p1.NAME = "控制台"
    p1.TARGET = "/index"
    p1.parent = p

    p2 = Privilege()
    p2.ID = uuid.uuid1()
    p2.UPDATE_DATETIME = datetime.now()
    p2.NAME = "登录"
    p2.TARGET = "/login"
    p2.parent = p

    db.session.add_all([p, p1, p2])
    db.session.commit()


@controllers.route('{}/init_role'.format(URL_PREFIX), methods=['GET'])
def init_role():
    # privilege = Privilege.query.options(load_only('TARGET')).all()
    # privilege = Privilege.query.with_entities(Privilege.TARGET).all()
    privilege = Privilege.query.all()
    # db.session.query(Article.read_num).all()
    # def has_pre():
    #     for pri in privilege:
    #         if pri.TARGET == '/index':
    #             return True
    #     return False
    #
    # print(privilege)
    # print(has_pre())

    role = Role()
    role.ID = uuid.uuid1()
    role.NAME = "超级管理员"
    role.CREATE_DATETIME = datetime.now()
    role.UPDATE_DATETIME = datetime.now()
    role.DESCRIPTION = "拥有全部权限，不允许修改"
    role.ICON_CLS = "layui-icon-senior"
    role.TYPE = 1
    role.privilege = privilege
    db.session.add(role)
    db.session.commit()


@controllers.route('{}/init_system'.format(URL_PREFIX), methods=['GET'])
def init_system():
    system = System()
    system.ID = uuid.uuid1()
    system.CREATE_DATETIME = datetime.now()
    system.UPDATE_DATETIME = datetime.now()
    system.SITE_NAME = "中文动词语义网"
    system.COPY_RIGHT_INFO = "© Copyright 2020-2021 DengBoCong. All Rights Reserved. 赣ICP备20002291号"
    system.ALLOW_LOGIN = True
    system.VERSION = "v1.0.0"
    db.session.add(system)
    db.session.commit()


@controllers.route('{}/init_home_page'.format(URL_PREFIX), methods=['GET'])
def init_home_page():
    home = HomePage(ID=uuid.uuid1(), CREATE_DATETIME=datetime.now(), UPDATE_DATETIME=datetime.now(), TYPE="HOME",
                    CONTENT="HOME")
    PUBLICATIONS = HomePage(ID=uuid.uuid1(), CREATE_DATETIME=datetime.now(), UPDATE_DATETIME=datetime.now(),
                            TYPE="PUBLICATIONS", CONTENT="PUBLICATIONS")
    CONTRIBUTORS = HomePage(ID=uuid.uuid1(), CREATE_DATETIME=datetime.now(), UPDATE_DATETIME=datetime.now(),
                            TYPE="CONTRIBUTORS", CONTENT="CONTRIBUTORS")
    db.session.add(home)
    db.session.add(PUBLICATIONS)
    db.session.add(CONTRIBUTORS)
    db.session.commit()

