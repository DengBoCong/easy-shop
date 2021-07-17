import uuid
from app import db
from flask_login import UserMixin, AnonymousUserMixin
from datetime import datetime


class Attachment(db.Model, UserMixin):
    __tablename__ = 'VERB_ATTACHMENT'

    ID = db.Column(db.String(50), primary_key=True, nullable=False, comment="ID")
    CREATE_DATETIME = db.Column(db.DateTime, index=True, default=datetime.now(), nullable=False, comment="创建时间")
    UPDATE_DATETIME = db.Column(db.DateTime, nullable=False, comment="更新时间")
    USER_ID = db.Column(db.String(50), nullable=False, default="", comment="创建用户id")
    DATA_ID = db.Column(db.String(50), nullable=False, default="", comment="所属数据id")
    NAME = db.Column(db.String(50), nullable=False, default="", comment="附件名称")
    PATH = db.Column(db.String(100), nullable=False, default="", comment="附件路径")
    VERB_NOTICE_ID = db.Column(db.String(50), db.ForeignKey('VERB_NOTICE.ID', ondelete='SET NULL'),
                               comment="verbNotice")

    def to_json(self):
        return {
            'ID': self.ID,
            'CREATE_DATETIME': self.CREATE_DATETIME.strftime('%Y-%m-%d %H:%M:%S'),
            'UPDATE_DATETIME': self.UPDATE_DATETIME.strftime('%Y-%m-%d %H:%M:%S'),
            'USER_ID': self.USER_ID,
            'DATA_ID': self.DATA_ID,
            'NAME': self.NAME,
            'PATH': self.PATH,
        }

    def __repr__(self):
        return '<VerbAttachment name:%r>\n' % self.NAME
