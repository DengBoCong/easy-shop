import uuid
from app import db
from flask_login import UserMixin, AnonymousUserMixin
from datetime import datetime


class Notice(db.Model, UserMixin):
    __tablename__ = 'VERB_NOTICE'

    ID = db.Column(db.String(50), primary_key=True, nullable=False, comment="ID")
    CREATE_DATETIME = db.Column(db.DateTime, index=True, default=datetime.now(), nullable=False, comment="创建时间")
    UPDATE_DATETIME = db.Column(db.DateTime, nullable=False, comment="更新时间")
    TITLE = db.Column(db.String(100), nullable=False, default="", comment="标题")
    SUB_TITLE = db.Column(db.String(100), nullable=False, default="", comment="子标题")
    IF_TOP = db.Column(db.Boolean, nullable=False, default=True, comment="是否置顶")
    DESCRIPTION = db.Column(db.String(200), nullable=False, default="", comment="备注")
    CONTENT = db.Column(db.Text, nullable=False, default="", comment="内容")

    attachments = db.relationship('Attachment', backref='notice', lazy='dynamic')

    def to_json(self):
        return {
            'ID': self.ID,
            'CREATE_DATETIME': self.CREATE_DATETIME.strftime('%Y-%m-%d %H:%M:%S'),
            'UPDATE_DATETIME': self.UPDATE_DATETIME.strftime('%Y-%m-%d %H:%M:%S'),
            'TITLE': self.TITLE,
            'SUB_TITLE': self.SUB_TITLE,
            'IF_TOP': self.IF_TOP,
            'DESCRIPTION': self.DESCRIPTION,
            'CONTENT': self.CONTENT,
        }

    def __repr__(self):
        return '<VerbNotice title:%r>\n' % self.TITLE
