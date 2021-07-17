import uuid
from app import db
from flask_login import UserMixin, AnonymousUserMixin
from datetime import datetime


class DataLog(db.Model, UserMixin):
    __tablename__ = 'VERB_DATA_LOG'

    ID = db.Column(db.String(50), primary_key=True, nullable=False, comment="ID")
    CREATE_DATETIME = db.Column(db.DateTime, index=True, default=datetime.now(), nullable=False, comment="创建时间")
    LEVEL = db.Column(db.Enum("INFO", "DEBUG", "WARNING", "ERROR"), nullable=False, default="INFO", comment="日志级别")
    USER_NAME = db.Column(db.String(100), nullable=False, default="", comment="用户名称")
    DESCRIPTION = db.Column(db.String(100), nullable=False, default="", comment="备注")
    ACTION = db.Column(db.String(200), nullable=False, default="", comment="动作")
    DATA = db.Column(db.String(255), nullable=False, default="", comment="数据")

    def to_json(self):
        return {
            'ID': self.ID,
            'CREATE_DATETIME': self.CREATE_DATETIME.strftime('%Y-%m-%d %H:%M:%S'),
            'LEVEL': self.LEVEL,
            'USER_NAME': self.USER_NAME,
            'DESCRIPTION': self.DESCRIPTION,
            'ACTION': self.ACTION,
            'DATA': self.DATA,
        }

    def __repr__(self):
        return '<VerbDataLog userName:%r>\n' % self.USER_NAME
