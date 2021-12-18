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

URL_PREFIX = "/system"


@controllers.route('{}/update!update_info'.format(URL_PREFIX), methods=['POST'])
@login_required
def system_update_info():
    info_data = json.loads(request.get_data())
    lang_type = info_data["langType"]
    contact_list = info_data.get("CONTACT_US", [])
    about_list = info_data.get("ABOUT_US", [])
    index_men = info_data.get("INDEX_MEN", None)
    index_women = info_data.get("INDEX_WOMEN", None)
    index_new = info_data.get("INDEX_NEW", None)

    try:
        system_info = {}
        if contact_list:
            system_info["CONTACT_US"] = ",".join(contact_list)

        if about_list:
            system_info["ABOUT_US"] = ",".join(about_list)

        if index_men:
            system_info["INDEX_MEN"] = index_men

        if index_women:
            system_info["INDEX_WOMEN"] = index_women

        if index_new:
            system_info["INDEX_NEW"] = index_new

        system = System.query.filter_by(ID="0").update(system_info)
        if system == 1:
            db.session.commit()

            return jsonify({'code': 0, 'msg': lang[lang_type]["common_update_success"], 'data': {'code': 0}})
        else:
            return jsonify({'code': 0, 'msg': lang[lang_type]["common_update_fail"], 'data': {'code': 1}})

    except:
        return jsonify({'code': 0, 'msg': lang[lang_type]["inner_network_abnormal"], 'data': {'code': 1}})
