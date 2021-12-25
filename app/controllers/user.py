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
from ..i18 import lang

URL_PREFIX = "/user"


@controllers.route('{}/add!add_user'.format(URL_PREFIX), methods=['POST'])
@login_required
def add_user():
    info_data = json.loads(request.get_data())
    lang_type = info_data["langType"]
    try:
        email_user = User.query.filter_by(EMAIL=info_data.get("EMAIL")).all()
        name_user = User.query.filter_by(NAME=info_data.get("NAME")).all()

        if len(email_user) != 0:
            return jsonify({'code': 0, 'msg': lang[lang_type]["inner_account_repeat_reset"], 'data': {'code': 1}})
        elif info_data.get("NAME") != "NULL-None" and len(name_user) != 0:
            return jsonify({'code': 0, 'msg': lang[lang_type]["inner_name_repeat_reset"], 'data': {'code': 1}})
        else:
            user = User(ID=uuid.uuid1(), CREATE_DATETIME=datetime.now(), EMAIL=info_data.get("EMAIL"),
                        NAME=info_data.get("NAME", ""), PHONE=info_data.get("PHONE", ""),
                        LAST_NAME=info_data.get("LAST_NAME", ""), FIRST_NAME=info_data.get("FIRST_NAME", ""),
                        COMPANY_NAME=info_data.get("COMPANY_NAME", ""), ORDERS=info_data.get("ORDERS", 0),
                        IF_LOGIN=bool(info_data.get("IF_LOGIN", 1)), ROLE=info_data.get("ROLE"),
                        DESCRIPTION=info_data.get("DESCRIPTION", ""), AREA_ID=info_data.get("AREA_ID"),
                        PARENT_ID="root")

            if info_data.get("PWD_", None):
                user.password = info_data["PWD_"]
                del info_data["PWD_"]

            db.session.add(user)
            db.session.commit()
            return jsonify({'code': 0, 'msg': lang[lang_type]["inner_add_success"], 'data': {'code': 0}})
    except:
        return jsonify({'code': 0, 'msg': lang[lang_type]["inner_network_abnormal"], 'data': {'code': 1}})


@controllers.route('{}/update!update_user'.format(URL_PREFIX), methods=['POST'])
@login_required
def update_user():
    info_data = json.loads(request.get_data())
    lang_type = info_data["langType"]
    user_id = info_data["ID"]
    flag = False
    user = User.query.filter_by(ID=user_id).first()

    try:
        del info_data["langType"]

        if info_data.get("_PWD", None) and info_data["_PWD"]:
            flag = True
            if user.check_password(info_data["_PWD"].encode('utf-8')):
                user.password = info_data["NEW_PWD"]
                db.session.commit()
            else:
                return jsonify({'code': 0, 'msg': lang[lang_type]["inner_pwd_fail"],
                                'data': {"userId": user_id, 'code': 1}})

        if "_PWD" in info_data.keys():
            del info_data["_PWD"]
        if "NEW_PWD" in info_data.keys():
            del info_data["NEW_PWD"]

        User.query.filter_by(ID=user_id).update(info_data)
        db.session.commit()

        if flag and user_id == current_user.ID:
            logout_user()
            return jsonify({'code': 0, 'msg': lang[lang_type]["inner_pwd_change"],
                            'data': {"userId": "", 'code': 0}})
        else:
            return jsonify({'code': 0, 'msg': lang[lang_type]["inner_change_success"],
                            'data': {"userId": user_id, 'code': 0}})

    except:
        return jsonify({'code': 0, 'msg': lang[lang_type]["common_update_fail"],
                        'data': {"userId": user_id, 'code': 1}})


@controllers.route('{}/update!update_user_admin'.format(URL_PREFIX), methods=['POST'])
@login_required
def update_user_admin():
    info_data = json.loads(request.get_data())
    lang_type = info_data["langType"]
    user_id = info_data["ID"]
    user = User.query.filter_by(ID=user_id).first()

    try:
        del info_data["langType"]
        if "NEW_PWD" in info_data.keys():
            user.password = info_data["NEW_PWD"]
            db.session.commit()
            del info_data["NEW_PWD"]

        User.query.filter_by(ID=user_id).update(info_data)
        db.session.commit()

        return jsonify({'code': 0, 'msg': lang[lang_type]["inner_change_success"],
                        'data': {"userId": user_id, 'code': 0}})

    except:
        return jsonify({'code': 0, 'msg': lang[lang_type]["common_update_fail"],
                        'data': {"userId": user_id, 'code': 1}})


@controllers.route('{}/delete!delete_user'.format(URL_PREFIX), methods=['POST'])
@login_required
def delete_user_by_id():
    info_data = json.loads(request.get_data())
    lang_type = info_data["langType"]
    user = User.query.get(info_data.get("ID"))

    if user is not None:
        for order in user.orders:
            for order_good in order.orderGoods:
                db.session.delete(order_good)
            db.session.delete(order)
        db.session.delete(user)

        db.session.commit()

        return jsonify({'code': 0, 'msg': lang[lang_type]["inner_delete_success"], 'data': {'code': 0}})
    else:
        return jsonify({'code': 0, 'msg': lang[lang_type]["inner_network_abnormal"], 'data': {'code': 1}})
