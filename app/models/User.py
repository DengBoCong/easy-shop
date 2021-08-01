import uuid
from app import db, loginManager
from flask_login import UserMixin, AnonymousUserMixin, confirm_login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from ..setting import DEFAULT_PASSWORD


@loginManager.user_loader
def load_user(user_id):
    return User.query.filter(User.ID == user_id).first()


# @loginManager.needs_refresh_handler
# def refresh():
#     # do stuff
#     confirm_login()


class User(db.Model, UserMixin):
    __tablename__ = 'SHOP_USER'

    ID = db.Column(db.String(50), primary_key=True, nullable=False, comment="ID")
    CREATE_DATETIME = db.Column(db.DateTime, index=True, default=datetime.now(), nullable=False, comment="创建时间")
    LAST_DATETIME = db.Column(db.DateTime, index=True, nullable=False, comment="最后登录时间")
    UPDATE_DATETIME = db.Column(db.DateTime, nullable=False, comment="更新时间")
    EMAIL = db.Column(db.String(60), index=True, nullable=False, default="", unique=True, comment="邮箱账号")
    ACCOUNT = db.Column(db.String(60), index=True, nullable=False, default="", unique=True, comment="登录账号")
    _PWD = db.Column(db.String(100), nullable=False, default=generate_password_hash(DEFAULT_PASSWORD), comment="密码")
    NAME = db.Column(db.String(100), nullable=False, default="未署名", comment="名称")
    PHONE = db.Column(db.String(20), nullable=False, default="00000000000", comment="电话号码")
    IF_LOGIN = db.Column(db.Boolean, nullable=False, default=True, comment="是否允许登录")
    SPARE_CHAT = db.Column(db.String(50), nullable=False, default="", comment="备用联系方式")
    DESCRIPTION = db.Column(db.String(200), nullable=False, default="", comment="备注")
    PARENT_ID = db.Column(db.String(50), nullable=False, default="", comment="上级ID")
    AREA_ID = db.Column(db.String(50), nullable=False, default="", comment="片区ID")
    RANK = db.Column(db.Enum('ADMIN', 'AGENT', 'USER'), nullable=False, comment="账号类型")

    @property
    def password(self):
        return self._PWD

    @property
    def is_active(self):
        return self.IF_LOGIN

    @password.setter
    def password(self, value):
        self._PWD = generate_password_hash(value)

    def check_password(self, user_pwd):
        return check_password_hash(self._PWD, user_pwd)

    def get_id(self):
        return self.ID

    def __repr__(self):
        return '<User %r>\n' % self.ACCOUNT

    def to_json(self):
        return {
            'ID': self.ID,
            'CREATE_DATETIME': self.CREATE_DATETIME.strftime('%Y-%m-%d %H:%M:%S'),
            'UPDATE_DATETIME': self.UPDATE_DATETIME.strftime('%Y-%m-%d %H:%M:%S'),
            'LAST_DATETIME': self.LAST_DATETIME.strftime('%Y-%m-%d %H:%M:%S'),
            'EMAIL': self.EMAIL,
            'ACCOUNT': self.ACCOUNT,
            'NAME': self.NAME,
            'PHONE': self.PHONE,
            'IF_LOGIN': self.IF_LOGIN,
            'SPARE_CHAT': self.SPARE_CHAT,
            'DESCRIPTION': self.DESCRIPTION,
            'PARENT_ID': self.PARENT_ID,
            'AREA_ID': self.AREA_ID,
            'RANK': self.RANK,
        }
