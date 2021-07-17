import uuid
from app import db
from flask_login import UserMixin, AnonymousUserMixin
from datetime import datetime
from flask import jsonify


class Privilege(db.Model, UserMixin):
    __tablename__ = 'VERB_PRIVILEGE'

    ID = db.Column(db.String(50), primary_key=True, nullable=False, comment="ID")
    CREATE_DATETIME = db.Column(db.DateTime, default=datetime.now(), nullable=False, comment="创建时间")
    UPDATE_DATETIME = db.Column(db.DateTime, nullable=False, comment="更新时间")
    NAME = db.Column(db.String(30), nullable=False, comment="命名")
    TARGET = db.Column(db.String(200), nullable=False, default="", comment="权限目标地址")
    ACTION = db.Column(db.String(100), nullable=False, default="", comment="动作")
    DESCRIPTION = db.Column(db.String(200), nullable=False, default="", comment="描述")
    ICON_CLS = db.Column(db.String(100), nullable=False, default="", comment="资源icon")
    SORT = db.Column(db.Integer, nullable=False, default=0, comment="排序")

    def get_id(self):
        return str(self.ID)

    def to_json(self):
        return {
            'ID': self.ID,
            'CREATE_DATETIME': self.CREATE_DATETIME.strftime('%Y-%m-%d %H:%M:%S'),
            'UPDATE_DATETIME': self.UPDATE_DATETIME.strftime('%Y-%m-%d %H:%M:%S'),
            'NAME': self.NAME,
            'TARGET': self.TARGET,
            'ACTION': self.ACTION,
            'DESCRIPTION': self.DESCRIPTION,
            'ICON_CLS': self.ICON_CLS,
            'SORT': self.SORT,
        }

    def __repr__(self):
        return '<Privilege name:%r target:%r>\n' % (self.NAME, self.TARGET)
