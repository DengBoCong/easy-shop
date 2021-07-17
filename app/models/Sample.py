import uuid
from app import db
from flask_login import UserMixin, AnonymousUserMixin
from datetime import datetime


class Sample(db.Model, UserMixin):
    __tablename__ = 'VERB_SAMPLE'

    ID = db.Column(db.String(50), primary_key=True, nullable=False, comment="ID")
    CREATE_DATETIME = db.Column(db.DateTime, default=datetime.now(), nullable=False, comment="创建时间")
    UPDATE_DATETIME = db.Column(db.DateTime, nullable=False, comment="更新时间")
    CONTENT = db.Column(db.Text, nullable=False, default="", comment="标注句子")
    VERB_PATTERN_ID = db.Column(db.String(50), db.ForeignKey('VERB_VERB_PATTERN.ID', ondelete='SET NULL'),
                                comment="verbPattern")

    def __repr__(self):
        return '<Sample id:%r>\n' % self.ID

    def to_json(self):
        return {
            'ID': self.ID,
            'CREATE_DATETIME': self.CREATE_DATETIME.strftime('%Y-%m-%d %H:%M:%S'),
            'UPDATE_DATETIME': self.UPDATE_DATETIME.strftime('%Y-%m-%d %H:%M:%S'),
            'CONTENT': self.CONTENT,
            'VERB_PATTERN_ID': self.VERB_PATTERN_ID,
        }
