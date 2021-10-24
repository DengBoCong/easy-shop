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
    EMAIL = db.Column(db.String(60), index=True, nullable=False, default="", unique=True, comment="邮箱账号")
    _PWD = db.Column(db.String(100), nullable=False, default=generate_password_hash(DEFAULT_PASSWORD), comment="密码")
    NAME = db.Column(db.String(100), nullable=False, default="未署名", comment="名称")
    PHONE = db.Column(db.String(30), nullable=False, default="00000000000", comment="联系方式")
    IF_LOGIN = db.Column(db.Boolean, nullable=False, default=True, comment="是否允许登录")
    ROLE = db.Column(db.Enum('ADMIN', 'AGENT', 'USER'), nullable=False, comment="账号类型")
    DESCRIPTION = db.Column(db.String(255), nullable=False, default="", comment="备注")
    AREA = db.Column(db.String(255), nullable=False, default="", comment="片区")
    PARENT_ID = db.Column(db.String(50), db.ForeignKey('SHOP_USER.ID'))

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
        return '<User %r>\n' % self.EMAIL

    def to_json(self):
        return {
            'ID': self.ID,
            'CREATE_DATETIME': self.CREATE_DATETIME.strftime('%Y-%m-%d %H:%M:%S'),
            'EMAIL': self.EMAIL,
            'NAME': self.NAME,
            'PHONE': self.PHONE,
            'IF_LOGIN': self.IF_LOGIN,
            'ROLE': self.ROLE,
            'DESCRIPTION': self.DESCRIPTION,
            'AREA': self.AREA,
            'PARENT_ID': self.PARENT_ID
        }
