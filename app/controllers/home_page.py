import json
from . import controllers
from .. import db
from ..models import HomePage
from datetime import datetime, timedelta
from flask import request
from flask import jsonify
from flask_login import login_required
from ..utils import set_system_log

URL_PREFIX = "/home_page"


@controllers.route('{}/home_page!get_home_by_type'.format(URL_PREFIX), methods=['POST'])
def get_home_by_type():
    try:
        info_data = json.loads(request.get_data())
        home = HomePage.query.filter_by(TYPE=info_data.get('type')).first()
        return jsonify({'code': 0, 'msg': '退出登录', 'data': home.to_json()})
    except:
        return jsonify({'code': 1, 'msg': '网络异常，加载失败', 'data': {}})


@controllers.route('{}/home_page!update_home_page_by_type'.format(URL_PREFIX), methods=['POST'])
@login_required
def update_home_page_by_type():
    try:
        info_data = json.loads(request.get_data())
        page = HomePage.query.filter_by(TYPE=info_data.get("TYPE")).update(info_data)
        if page == 1:
            db.session.commit()

            set_system_log(PATH="/api/home_page/home_page!update_home_page_by_type", ACTION="home_page",
                           MESSAGE="更新{}编辑页成功".format(info_data.get('TYPE')), LEVEL="INFO")
            return jsonify({'code': 0, 'msg': '更新成功', 'data': {}})
        else:
            set_system_log(PATH="/api/home_page/home_page!update_home_page_by_type", ACTION="home_page",
                           MESSAGE="更新{}编辑页失败，无对应页面信息".format(info_data.get('TYPE')), LEVEL="WARNING")
            return jsonify({'code': 1, 'msg': '更新失败', 'data': {}})
    except:
        set_system_log(PATH="/api/home_page/home_page!update_home_page_by_type", ACTION="home_page",
                       MESSAGE="更新{}编辑页失败，网络异常".format(info_data.get('TYPE')), LEVEL="ERROR")
        return jsonify({'code': 1, 'msg': '网络异常，请检查后重试', 'data': {}})
