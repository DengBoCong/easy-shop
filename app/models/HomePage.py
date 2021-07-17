import uuid
from app import db
from flask_login import UserMixin, AnonymousUserMixin
from datetime import datetime


class HomePage(db.Model, UserMixin):
    __tablename__ = 'VERB_HOME_PAGE'

    ID = db.Column(db.String(50), primary_key=True, nullable=False, comment="ID")
    CREATE_DATETIME = db.Column(db.DateTime, index=True, default=datetime.now(), nullable=False, comment="创建时间")
    UPDATE_DATETIME = db.Column(db.DateTime, nullable=False, comment="更新时间")
    TYPE = db.Column(db.Enum('HOME', 'PUBLICATIONS', 'CONTRIBUTORS'), nullable=False, comment="类别")
    CONTENT = db.Column(db.Text, nullable=False, default="", comment="内容")

    def to_json(self):
        return {
            'ID': self.ID,
            'CREATE_DATETIME': self.CREATE_DATETIME.strftime('%Y-%m-%d %H:%M:%S'),
            'UPDATE_DATETIME': self.UPDATE_DATETIME.strftime('%Y-%m-%d %H:%M:%S'),
            'TYPE': self.TYPE,
            'CONTENT': self.CONTENT,
        }

    def __repr__(self):
        return '<VerbHomePage type:%r>\n' % self.TYPE
