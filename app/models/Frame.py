import uuid
from app import db
from flask_login import UserMixin, AnonymousUserMixin
from datetime import datetime


class Frame(db.Model, UserMixin):
    __tablename__ = 'VERB_FRAME'

    ID = db.Column(db.String(50), primary_key=True, nullable=False, comment="ID")
    CREATE_DATETIME = db.Column(db.DateTime, default=datetime.now(), nullable=False, comment="创建时间")
    UPDATE_DATETIME = db.Column(db.DateTime, nullable=False, comment="更新时间")
    NAME = db.Column(db.String(50), nullable=False, default="", comment="名称")
    DEF = db.Column(db.String(255), nullable=False, default="", comment="Def")
    FRAME_TYPE = db.Column(db.Enum('Archi', 'Primary', 'Basic'), nullable=False, comment="类别")
    PATTERN = db.Column(db.String(255), nullable=False, default="", comment="PATTERN")
    IMAGE_URL = db.Column(db.String(255), nullable=False, default="", comment="图片地址")
    SAMPLE = db.Column(db.Text, nullable=False, default="", comment="SAMPLE")
    PARENT_ID = db.Column(db.String(50), db.ForeignKey('VERB_FRAME.ID'))

    child = db.relationship('Frame', back_populates='parent')
    parent = db.relationship('Frame', back_populates='child', remote_side=[ID])

    verbs = db.relationship('Verb', backref='frame', lazy='dynamic')

    def __repr__(self):
        return '<Frame name:%r>\n' % self.NAME

    def to_json(self):
        return {
            'ID': self.ID,
            'CREATE_DATETIME': self.CREATE_DATETIME.strftime('%Y-%m-%d %H:%M:%S'),
            'UPDATE_DATETIME': self.UPDATE_DATETIME.strftime('%Y-%m-%d %H:%M:%S'),
            'NAME': self.NAME,
            'DEF': self.DEF,
            'FRAME_TYPE': self.FRAME_TYPE,
            'PATTERN': self.PATTERN,
            'SAMPLE': self.SAMPLE,
            'PARENT_ID': self.PARENT_ID,
            'IMAGE_URL': self.IMAGE_URL,
        }
