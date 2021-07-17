import uuid
from app import db
from flask_login import UserMixin, AnonymousUserMixin
from datetime import datetime


class Verb(db.Model, UserMixin):
    __tablename__ = 'VERB_VERB'

    ID = db.Column(db.String(50), primary_key=True, nullable=False, comment="ID")
    CREATE_DATETIME = db.Column(db.DateTime, default=datetime.now(), nullable=False, comment="创建时间")
    UPDATE_DATETIME = db.Column(db.DateTime, nullable=False, comment="更新时间")
    NAME = db.Column(db.String(30), nullable=False, default="", comment="名称")
    PIN_YIN = db.Column(db.String(30), nullable=False, default="", comment="拼音")
    FREQUENCY = db.Column(db.Integer, nullable=False, default=0, comment="频率")
    IF_FINISH = db.Column(db.Enum("0", "1", "2"), nullable=False, default="0", comment="是否完成标注")
    USER_ID = db.Column(db.String(50), db.ForeignKey('VERB_USER.ID', ondelete='SET NULL'), comment="用户ID")
    TEMP_FRAME_ID = db.Column(db.String(50), nullable=False, default="", comment="参考Frame")

    FRAMES_ID = db.Column(db.String(50), db.ForeignKey('VERB_FRAME.ID', ondelete='SET NULL'),
                          comment="Frame")

    patterns = db.relationship('VerbPattern', backref='ownerVerb', lazy='dynamic')

    def __repr__(self):
        return '<Verb name:%r>\n' % self.NAME

    def to_json(self):
        return {
            'ID': self.ID,
            'CREATE_DATETIME': self.CREATE_DATETIME.strftime('%Y-%m-%d %H:%M:%S'),
            'UPDATE_DATETIME': self.UPDATE_DATETIME.strftime('%Y-%m-%d %H:%M:%S'),
            'NAME': self.NAME,
            'PIN_YIN': self.PIN_YIN,
            'FREQUENCY': self.FREQUENCY,
            'FRAMES_ID': self.FRAMES_ID,
            'IF_FINISH': self.IF_FINISH,
            'USER_ID': self.USER_ID,
            'TEMP_FRAME_ID': self.TEMP_FRAME_ID
        }
