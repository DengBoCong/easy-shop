import uuid
from . import controllers
from .. import db
from ..models import User, OnLine, SystemLog
from datetime import datetime, timedelta
from ..setting import COOKIE_DURATION_DAYS
from flask import request
from flask import jsonify
from flask_login import login_user, logout_user, login_required, current_user

URL_PREFIX = "/login"


@controllers.route('{}/verb_user!verification_login'.format(URL_PREFIX), methods=['POST'])
def do_login():
    # 检查用户名是否存在
    user = User.query.filter_by(EMAIL=request.form['email']).first()
    if user is not None:
        if user.check_password(request.form['password'].encode('utf-8')):
            online = OnLine(ID=uuid.uuid1(), IP=request.remote_addr, ACCESS_TOKEN=uuid.uuid1(),
                            LOGIN_NAME=user.NAME, TYPE=request.headers.get("User-Agent"))

            log = SystemLog(ID=uuid.uuid1(), PATH="/api/login/verb_user!verification_login",
                            USER_NAME=user.NAME, USER_ID=user.ID, MESSAGE="登录", IP=request.remote_addr,
                            ACTION="login", AGENT=request.headers.get("User-Agent"))

            User.query.filter_by(EMAIL=request.form['email']).update({"LAST_IP": request.remote_addr,
                                                                             "LAST_DATETIME": datetime.now()})
            db.session.add(online)
            db.session.add(log)
            db.session.commit()

            login_user(user, remember=True if request.form['remember'] == "on" else False,
                       duration=timedelta(days=COOKIE_DURATION_DAYS))
            # is_safe_url

            return jsonify({'code': 0, 'msg': '登录成功', 'data': {'access_token': online.ACCESS_TOKEN}})
    return jsonify({'code': 1, 'msg': '账号或密码错误', 'data': {}})


@controllers.route('{}/verb_user!verification_logout'.format(URL_PREFIX), methods=['GET'])
@login_required
def do_logout():
    log = SystemLog(ID=uuid.uuid1(), PATH="/api/login/verb_user!verification_logout", LEVEL="INFO",
                    USER_NAME=current_user.NAME, USER_ID=current_user.ID, MESSAGE="退出了系统",
                    ACTION="login", IP=request.remote_addr, AGENT=request.headers.get("User-Agent"))

    logout_user()
    online = OnLine.query.filter_by(ACCESS_TOKEN=request.args.get('access_token')).first()
    online.IF_ONLINE = False

    db.session.add(log)
    db.session.commit()
    return jsonify({'code': 0, 'msg': '退出登录', 'data': {}})
