import uuid
from app import db
from flask_login import UserMixin, AnonymousUserMixin
from datetime import datetime


class Config(db.Model, UserMixin):
    __tablename__ = 'VERB_CONFIG'

    ID = db.Column(db.String(50), primary_key=True, nullable=False, comment="ID")
    CREATE_DATETIME = db.Column(db.DateTime, index=True, default=datetime.now(), nullable=False, comment="创建时间")
    UPDATE_DATETIME = db.Column(db.DateTime, nullable=False, comment="更新时间")
    NAME = db.Column(db.String(100), nullable=False, default="", comment="配置名称")
    KEY = db.Column(db.String(50), nullable=False, default="", comment="配置键")
    VALUE = db.Column(db.Text, nullable=False, default="", comment="配置值")

    def to_json(self):
        return {
            'ID': self.ID,
            'CREATE_DATETIME': self.CREATE_DATETIME.strftime('%Y-%m-%d %H:%M:%S'),
            'UPDATE_DATETIME': self.UPDATE_DATETIME.strftime('%Y-%m-%d %H:%M:%S'),
            'NAME': self.NAME,
            'KEY': self.KEY,
            'VALUE': self.VALUE,
        }

    def __repr__(self):
        return '<VerbConfig name:%r>\n' % self.NAME
