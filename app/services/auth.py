from app import db
from functools import wraps
from flask import abort, render_template
from flask_login import current_user


def permission_can(privileges, permission):
    """
    检测用户是否有特定权限
    :param privileges: 用户ROLE_ID
    :param permission: 权限目标地址
    :return:
    """
    for privilege in privileges:
        if privilege.TARGET == permission:
            return True
    return False


def permission_required(permission):
    """
    权限认证装饰器
    :param permission:
    :return:
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                privileges = current_user.roles.privilege
            except:
                abort(401)
            try:
                if not privileges or not permission_can(privileges, permission):
                    abort(403)
                return f(*args, **kwargs)
            except:
                abort(403)

        return decorated_function

    return decorator
