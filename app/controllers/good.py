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

URL_PREFIX = "/good"


@controllers.route('{}/get!get_all_good_category'.format(URL_PREFIX), methods=['GET'])
@login_required
def get_all_good_category():
    info_data = request.args.to_dict()
    lang_type = info_data["langType"]
    try:
        good_categories = GoodCategory.query.order_by(asc(GoodCategory.EN_NAME)).all()
        good_categories_list = []
        for good_category in good_categories:
            good_categories_list.append(good_category.to_json())
        return jsonify({'code': 0, 'msg': '', 'data': good_categories_list})
    except:
        return jsonify({'code': 1, 'msg': lang[lang_type]["inner_network_abnormal"], 'data': [{}]})


@controllers.route('{}/add!add_good_category'.format(URL_PREFIX), methods=['POST'])
@login_required
def add_good_category():
    info_data = json.loads(request.get_data())
    lang_type = info_data["langType"]

    try:
        name_good_category = GoodCategory.query.filter_by(NAME=info_data.get("NAME")).all()
        en_name_good_category = GoodCategory.query.filter_by(EN_NAME=info_data.get("EN_NAME")).all()

        if len(name_good_category) != 0:
            return jsonify({'code': 1, 'msg': lang[lang_type]["inner_zh_ch_repeat_reset"], 'data': {}})
        elif len(en_name_good_category) != 0:
            return jsonify({'code': 1, 'msg': lang[lang_type]["inner_en_us_repeat_reset"], 'data': {}})
        else:
            good_category = GoodCategory(ID=uuid.uuid1(), CREATE_DATETIME=datetime.now(), NAME=info_data.get("NAME"),
                                         EN_NAME=info_data.get("EN_NAME"), DESCRIPTION=info_data.get("DESCRIPTION", ""))
            db.session.add(good_category)
            db.session.commit()

            good_categories = GoodCategory.query.order_by(asc(GoodCategory.EN_NAME)).all()
            good_categories_list = []
            for good_category in good_categories:
                good_categories_list.append(good_category.to_json())

            return jsonify({'code': 0, 'msg': lang[lang_type]["inner_add_success"],
                            'data': {"goodCategories": good_categories_list}})
    except:
        return jsonify({'code': 1, 'msg': lang[lang_type]["inner_network_abnormal"], 'data': {}})
