import uuid
from . import controllers
from .. import db
from ..models import User
from datetime import datetime, timedelta
from ..setting import COOKIE_DURATION_DAYS
from flask import request
from flask import jsonify
from flask_login import login_user, logout_user, login_required, current_user
from ..i18 import lang

URL_PREFIX = "/login"


@controllers.route('{}/user!verification_login'.format(URL_PREFIX), methods=['POST'])
def do_login():
    # 检查用户名是否存在
    user = User.query.filter_by(EMAIL=request.form['account']).first()
    lang_type = request.form['langType']
    if user is not None:
        if user.check_password(request.form['password'].encode('utf-8')):
            login_user(user, remember=True, duration=timedelta(days=COOKIE_DURATION_DAYS))

            return jsonify({'code': 0, 'msg': lang[lang_type]["inner_login_success"], 'data': {'code': 0}})
    return jsonify({'code': 0, 'msg': lang[lang_type]["inner_login_fail"], 'data': {'code': 1}})
