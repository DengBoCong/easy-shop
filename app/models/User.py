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
    __tablename__ = 'VERB_USER'

    ID = db.Column(db.String(50), primary_key=True, nullable=False, comment="ID")
    CREATE_DATETIME = db.Column(db.DateTime, index=True, default=datetime.now(), nullable=False, comment="创建时间")
    LAST_DATETIME = db.Column(db.DateTime, index=True, nullable=False, comment="最后登录时间")
    UPDATE_DATETIME = db.Column(db.DateTime, nullable=False, comment="更新时间")
    EMAIL = db.Column(db.String(60), index=True, nullable=False, default="", unique=True, comment="邮箱账号")
    _PWD = db.Column(db.String(100), nullable=False, default=generate_password_hash(DEFAULT_PASSWORD), comment="密码")
    NAME = db.Column(db.String(100), nullable=False, default="未署名", comment="名称")
    SEX = db.Column(db.String(1), nullable=False, default="0", comment="性别")
    AGE = db.Column(db.Integer, nullable=False, default=0, comment="年龄")
    PHOTO = db.Column(db.String(200), nullable=False, default="/static/img/default_avatar.jpg", comment="头像")
    PHONE = db.Column(db.String(20), nullable=False, default="00000000000", comment="手机号")
    IF_LOGIN = db.Column(db.Boolean, nullable=False, default=True, comment="是否允许登录")
    IF_CONTACT = db.Column(db.Boolean, nullable=False, default=False, comment="是否是系统联系人")
    WE_CHAT = db.Column(db.String(30), nullable=False, default="", comment="微信号")
    QQ = db.Column(db.String(20), nullable=False, default="", comment="QQ号")
    DESCRIPTION = db.Column(db.String(200), nullable=False, default="", comment="备注")
    LAST_IP = db.Column(db.String(15), nullable=False, default="", comment="最后登录ip")

    ROLE_ID = db.Column(db.String(50), db.ForeignKey('VERB_ROLE.ID', ondelete='SET NULL'), comment="角色ID")
    verbs = db.relationship('Verb', backref='user', lazy='dynamic')

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

    def have_permission(self, url):
        permissions = []
        for role in self.roles:
            permissions.extend([resource for resource in role.resources])

        if filter(lambda x: x.URL == url, permissions):
            return True

    def __repr__(self):
        return '<User %r>\n' % self.NAME

    def to_json(self):
        return {
            'ID': self.ID,
            'CREATE_DATETIME': self.CREATE_DATETIME.strftime('%Y-%m-%d %H:%M:%S'),
            'UPDATE_DATETIME': self.UPDATE_DATETIME.strftime('%Y-%m-%d %H:%M:%S'),
            'LAST_DATETIME': self.LAST_DATETIME.strftime('%Y-%m-%d %H:%M:%S'),
            'EMAIL': self.EMAIL,
            'NAME': self.NAME,
            'SEX': self.SEX,
            'AGE': self.AGE,
            'PHOTO': self.PHOTO,
            'PHONE': self.PHONE,
            'IF_LOGIN': self.IF_LOGIN,
            'IF_CONTACT': self.IF_CONTACT,
            'WE_CHAT': self.WE_CHAT,
            'QQ': self.QQ,
            'DESCRIPTION': self.DESCRIPTION,
            'ROLE_ID': self.ROLE_ID,
            'LAST_IP': self.LAST_IP,
        }
