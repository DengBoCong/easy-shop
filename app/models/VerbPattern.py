import uuid
from app import db
from flask_login import UserMixin, AnonymousUserMixin
from datetime import datetime


class VerbPattern(db.Model, UserMixin):
    __tablename__ = 'VERB_VERB_PATTERN'

    ID = db.Column(db.String(50), primary_key=True, nullable=False, comment="ID")
    CREATE_DATETIME = db.Column(db.DateTime, default=datetime.now(), nullable=False, comment="创建时间")
    UPDATE_DATETIME = db.Column(db.DateTime, nullable=False, comment="更新时间")
    CONSTRUCTION = db.Column(db.String(255), nullable=False, default="", comment="CONSTRUCTION")
    PATTERN = db.Column(db.String(255), nullable=False, default="", comment="PATTERN")

    VERB_ID = db.Column(db.String(50), db.ForeignKey('VERB_VERB.ID', ondelete='SET NULL'),
                        comment="verb")

    samples = db.relationship('Sample', backref='verbPattern', lazy='dynamic')

    def __repr__(self):
        return '<VerbPattern name:%r>\n' % self.PATTERN

    def to_json(self):
        return {
            'ID': self.ID,
            'CREATE_DATETIME': self.CREATE_DATETIME.strftime('%Y-%m-%d %H:%M:%S'),
            'UPDATE_DATETIME': self.UPDATE_DATETIME.strftime('%Y-%m-%d %H:%M:%S'),
            'CONSTRUCTION': self.CONSTRUCTION,
            'PATTERN': self.PATTERN,
            'VERB_ID': self.VERB_ID,
        }
