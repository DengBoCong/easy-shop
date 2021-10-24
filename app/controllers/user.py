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
            return jsonify({'code': 1, 'msg': lang[lang_type]["inner_account_repeat_reset"], 'data': {}})
        elif info_data.get("NAME") != "NULL-None" and len(name_user) != 0:
            return jsonify({'code': 1, 'msg': lang[lang_type]["inner_name_repeat_reset"], 'data': {}})
        else:
            user = User(ID=uuid.uuid1(), CREATE_DATETIME=datetime.now(), EMAIL=info_data.get("ACCOUNT"),
                        NAME=info_data.get("NAME", "NULL-None"), PHONE=info_data.get("PHONE", "00000000000"),
                        IF_LOGIN=bool(info_data.get("IF_LOGIN", 1)), ROLE=info_data.get("ROLE"),
                        DESCRIPTION=info_data.get("DESCRIPTION", ""), AREA=info_data.get("AREA"),
                        PARENT_ID=info_data.get("PARENT_ID"))
            db.session.add(user)
            db.session.commit()
            return jsonify({'code': 0, 'msg': lang[lang_type]["inner_add_success"], 'data': {}})
    except:
        return jsonify({'code': 1, 'msg': lang[lang_type]["inner_network_abnormal"], 'data': {}})
