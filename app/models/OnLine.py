import uuid
from app import db
from datetime import datetime


class OnLine(db.Model):
    __tablename__ = 'VERB_ONLINE'

    ID = db.Column(db.String(36), primary_key=True, nullable=False, comment="ID")
    CREATE_DATETIME = db.Column(db.DateTime, index=True, default=datetime.now(), nullable=False, comment="创建时间")
    LOGIN_NAME = db.Column(db.String(100), nullable=False, default="", comment="登录名")
    IP = db.Column(db.String(100), nullable=False, default="", comment="登录IP")
    TYPE = db.Column(db.String(200), nullable=False, default="", comment="请求代理类型")
    ACCESS_TOKEN = db.Column(db.String(50), nullable=False, index=True, default="", comment="用户登录验证token")
    IF_ONLINE = db.Column(db.Boolean, nullable=False, default=True, comment="是否在线")

    def get_id(self):
        return str(self.ID)

    def __repr__(self):
        return '<Online loginName:%r>\n' % self.LOGIN_NAME

    def to_json(self):
        return {
            'ID': self.ID,
            'CREATE_DATETIME': self.CREATE_DATETIME.strftime('%Y-%m-%d %H:%M:%S'),
            'LOGIN_NAME': self.LOGIN_NAME,
            'IP': self.IP,
            'TYPE': self.TYPE,
            'ACCESS_TOKEN': self.ACCESS_TOKEN,
            'IF_ONLINE': self.IF_ONLINE
        }
