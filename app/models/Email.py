import uuid
from app import db
from flask_login import UserMixin, AnonymousUserMixin
from datetime import datetime


class Email(db.Model, UserMixin):
    __tablename__ = 'VERB_EMAIL'

    ID = db.Column(db.String(50), primary_key=True, nullable=False, comment="ID")
    CREATE_DATETIME = db.Column(db.DateTime, index=True, default=datetime.now(), nullable=False, comment="创建时间")
    UPDATE_DATETIME = db.Column(db.DateTime, nullable=False, comment="更新时间")
    SENDER_ADDRESS = db.Column(db.String(100), nullable=False, default="", comment="发件人邮件地址")
    SENDER_NAME = db.Column(db.String(100), nullable=False, default="", comment="发件人显示名")
    SENDER_TITLE_PREFIX = db.Column(db.String(100), nullable=False, default="", comment="发送邮件标题前缀")
    HOST = db.Column(db.String(100), nullable=False, default="", comment="服务器主机名")
    PORT = db.Column(db.Integer, nullable=False, default=25, comment="服务器端口")
    USER_NAME = db.Column(db.String(50), nullable=False, default="", comment="用户名")
    PASSWORD = db.Column(db.String(50), nullable=False, default="", comment="密码")
    IF_SSL = db.Column(db.Boolean, nullable=False, default=False, comment="是否使用ssl， 0 默认不使用 1 使用")
    IF_USED = db.Column(db.Boolean, nullable=False, default=False, comment="是否被使用， 0 默认不使用 1 使用")

    def to_json(self):
        return {
            'ID': self.ID,
            'CREATE_DATETIME': self.CREATE_DATETIME.strftime('%Y-%m-%d %H:%M:%S'),
            'UPDATE_DATETIME': self.UPDATE_DATETIME.strftime('%Y-%m-%d %H:%M:%S'),
            'SENDER_ADDRESS': self.SENDER_ADDRESS,
            'SENDER_NAME': self.SENDER_NAME,
            'SENDER_TITLE_PREFIX': self.SENDER_TITLE_PREFIX,
            'HOST': self.HOST,
            'PORT': self.PORT,
            'USER_NAME': self.USER_NAME,
            'IF_SSL': self.IF_SSL,
            'IF_USED': self.IF_USED,
        }

    def __repr__(self):
        return '<VerbEmail userName:%r>\n' % self.USER_NAME
