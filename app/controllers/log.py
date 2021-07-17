import uuid
from . import controllers
from .. import db
from ..models import *
from datetime import datetime
from flask import request
from flask import jsonify
from flask_login import login_required
from sqlalchemy import or_, and_
from ..utils import set_system_log
from ..setting import PAGE_LIMIT

URL_PREFIX = "/log"


# ==================system log相关=======================

@controllers.route('{}/get!get_all_system_log'.format(URL_PREFIX), methods=['GET'])
@login_required
def get_all_system_log():
    info_data = request.args.to_dict()
    page = int(info_data.get("page", 1))
    limit = int(info_data.get("limit", PAGE_LIMIT))
    try:
        system_logs = SystemLog.query.order_by(SystemLog.CREATE_DATETIME.desc()).all()
        start = (page - 1) * limit
        log_list = []
        for log in system_logs:
            log_json = log.to_json()
            log_list.append(log_json)
        count = len(log_list)

        set_system_log(PATH="/api/log/get!get_all_system_log", ACTION="log",
                       MESSAGE="操作日志加载成功", LEVEL="INFO")
        return jsonify({'code': 0, 'msg': '', 'count': count, 'data': log_list[start:page * limit]})
    except:
        set_system_log(PATH="/api/log/get!get_all_system_log", ACTION="log",
                       MESSAGE="网络异常，操作日志加载失败", LEVEL="ERROR")
        return jsonify({'code': 1, 'msg': '网络异常，加载失败', 'count': '0', 'data': [{}]})


@controllers.route('{}/get!system_log_list_filter_by_param'.format(URL_PREFIX), methods=['GET'])
@login_required
def system_log_list_filter_by_param():
    info_data = request.args.to_dict()
    try:
        system_logs = SystemLog.query.filter(
            and_(SystemLog.LEVEL.like("%" + info_data.get("LEVEL", "") + "%"),
                 SystemLog.USER_NAME.like("%" + info_data.get("USER_NAME", "") + "%"),
                 SystemLog.MESSAGE.like("%" + info_data.get("MESSAGE", "") + "%"))
        ).all()

        logs_list = []
        for log in system_logs:
            log_json = log.to_json()
            logs_list.append(log_json)
        count = len(logs_list)

        set_system_log(PATH="/api/log/get!system_log_list_filter_by_param", ACTION="log",
                       MESSAGE="操作日志查询成功", LEVEL="INFO")
        return jsonify({'code': 0, 'msg': '', 'count': count, 'data': logs_list})
    except:
        set_system_log(PATH="/api/log/get!system_log_list_filter_by_param", ACTION="log",
                       MESSAGE="网络异常，操作日志加载失败", LEVEL="ERROR")
        return jsonify({'code': 1, 'msg': '网络异常，加载失败', 'count': '0', 'data': [{}]})


# ==================data log相关=======================

@controllers.route('{}/get!get_all_data_log'.format(URL_PREFIX), methods=['GET'])
@login_required
def get_all_data_log():
    info_data = request.args.to_dict()
    page = int(info_data.get("page", 1))
    limit = int(info_data.get("limit", PAGE_LIMIT))
    try:
        data_logs = DataLog.query.order_by(DataLog.CREATE_DATETIME.desc()).all()
        start = (page - 1) * limit
        log_list = []
        for log in data_logs:
            log_json = log.to_json()
            log_list.append(log_json)
        count = len(log_list)

        set_system_log(PATH="/api/log/get!get_all_data_log", ACTION="log",
                       MESSAGE="数据日志加载成功", LEVEL="INFO")
        return jsonify({'code': 0, 'msg': '', 'count': count, 'data': log_list[start:page * limit]})
    except:
        set_system_log(PATH="/api/log/get!get_all_data_log", ACTION="log",
                       MESSAGE="网络异常，数据日志加载失败", LEVEL="ERROR")
        return jsonify({'code': 1, 'msg': '网络异常，加载失败', 'count': '0', 'data': [{}]})


@controllers.route('{}/get!data_log_list_filter_by_param'.format(URL_PREFIX), methods=['GET'])
@login_required
def data_log_list_filter_by_param():
    info_data = request.args.to_dict()
    try:
        data_logs = DataLog.query.filter(
            and_(DataLog.LEVEL.like("%" + info_data.get("LEVEL", "") + "%"),
                 DataLog.USER_NAME.like("%" + info_data.get("USER_NAME", "") + "%"),
                 DataLog.DESCRIPTION.like("%" + info_data.get("DESCRIPTION", "") + "%"))
        ).all()

        logs_list = []
        for log in data_logs:
            log_json = log.to_json()
            logs_list.append(log_json)
        count = len(logs_list)

        set_system_log(PATH="/api/log/get!data_log_list_filter_by_param", ACTION="log",
                       MESSAGE="数据日志查询成功", LEVEL="INFO")
        return jsonify({'code': 0, 'msg': '', 'count': count, 'data': logs_list})
    except:
        set_system_log(PATH="/api/log/get!data_log_list_filter_by_param", ACTION="log",
                       MESSAGE="网络异常，数据日志加载失败", LEVEL="ERROR")
        return jsonify({'code': 1, 'msg': '网络异常，加载失败', 'count': '0', 'data': [{}]})
