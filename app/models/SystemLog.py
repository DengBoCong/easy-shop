import uuid
from app import db
from flask_login import UserMixin, AnonymousUserMixin
from datetime import datetime


class SystemLog(db.Model, UserMixin):
    __tablename__ = 'VERB_SYSTEM_LOG'

    ID = db.Column(db.String(50), primary_key=True, nullable=False, comment="ID")
    CREATE_DATETIME = db.Column(db.DateTime, index=True, default=datetime.now(), nullable=False, comment="创建时间")
    LEVEL = db.Column(db.Enum("INFO", "DEBUG", "WARNING", "ERROR"), nullable=False, default="INFO", comment="日志级别")
    PATH = db.Column(db.String(100), nullable=False, default="", comment="请求路径")
    GET = db.Column(db.Text, nullable=False, default="", comment="get参数")
    POST = db.Column(db.Text, nullable=False, default="", comment="post参数")
    USER_NAME = db.Column(db.String(100), nullable=False, default="", comment="用户名称")
    USER_ID = db.Column(db.String(50), nullable=False, default="", comment="用户ID")
    MESSAGE = db.Column(db.String(100), nullable=False, default="", comment="描述")
    ACTION = db.Column(db.String(200), nullable=False, default="", comment="动作")
    IP = db.Column(db.String(100), nullable=False, default="", comment="操作IP")
    AGENT = db.Column(db.String(200), nullable=False, default="", comment="用户代理")

    def to_json(self):
        return {
            'ID': self.ID,
            'CREATE_DATETIME': self.CREATE_DATETIME.strftime('%Y-%m-%d %H:%M:%S'),
            'LEVEL': self.LEVEL,
            'PATH': self.PATH,
            'GET': self.GET,
            'POST': self.POST,
            'USER_NAME': self.USER_NAME,
            'USER_ID': self.USER_ID,
            'MESSAGE': self.MESSAGE,
            'ACTION': self.ACTION,
            'IP': self.IP,
            'AGENT': self.AGENT,
        }

    def __repr__(self):
        return '<VerbSystemLog userName:%r>\n' % self.USER_NAME
