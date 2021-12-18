import json
import uuid
from datetime import datetime
from .. import db
from . import controllers
from ..models import *
from flask import request, redirect, url_for
from flask import jsonify
from flask_login import current_user, logout_user, login_required
from sqlalchemy import asc
from ..i18 import lang

URL_PREFIX = "/color"


@controllers.route('{}/add!add_color'.format(URL_PREFIX), methods=['POST'])
@login_required
def add_color():
    info_data = json.loads(request.get_data())
    lang_type = info_data["langType"]

    try:
        name_color = Color.query.filter_by(NAME=info_data.get("NAME")).all()
        en_name_color = Color.query.filter_by(EN_NAME=info_data.get("EN_NAME")).all()

        if len(name_color) != 0:
            return jsonify({'code': 0, 'msg': lang[lang_type]["inner_zh_ch_repeat_reset"], 'data': {'code': 1}})
        elif len(en_name_color) != 0:
            return jsonify({'code': 0, 'msg': lang[lang_type]["inner_en_us_repeat_reset"], 'data': {'code': 1}})
        else:
            color = Color(ID=uuid.uuid1(), CREATE_DATETIME=datetime.now(), NAME=info_data.get("NAME"),
                          EN_NAME=info_data.get("EN_NAME"), DESCRIPTION=info_data.get("DESCRIPTION", ""))
            db.session.add(color)
            db.session.commit()

            colors = Color.query.order_by(asc(Color.EN_NAME)).all()
            colors_list = []
            for color in colors:
                colors_list.append(color.to_json())

            return jsonify({'code': 0, 'msg': lang[lang_type]["inner_add_success"],
                            'data': {"colors": colors_list, 'code': 0}})
    except:
        return jsonify({'code': 0, 'msg': lang[lang_type]["inner_network_abnormal"], 'data': {'code': 1}})
