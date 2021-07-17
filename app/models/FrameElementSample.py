import uuid
from app import db
from flask_login import UserMixin, AnonymousUserMixin
from datetime import datetime


class FrameElementSample(db.Model, UserMixin):
    __tablename__ = 'VERB_FRAME_ELEMENT_SAMPLE'

    ID = db.Column(db.String(50), primary_key=True, nullable=False, comment="ID")
    CREATE_DATETIME = db.Column(db.DateTime, default=datetime.now(), nullable=False, comment="创建时间")
    LEMMA = db.Column(db.String(255), nullable=False, default="", comment="Lemma")
    SAMPLE = db.Column(db.String(255), nullable=False, default="", comment="Sample")
    FRAME_ID = db.Column(db.String(50), nullable=False, default="", comment="FrameId")
    ELEMENT_ID = db.Column(db.String(50), db.ForeignKey('VERB_FRAME_ELEMENT.ID', ondelete='SET NULL'),
                           comment="Element")

    def __repr__(self):
        return '<FrameElementSample id:%r>\n' % self.ID

    def to_json(self):
        return {
            'ID': self.ID,
            'CREATE_DATETIME': self.CREATE_DATETIME.strftime('%Y-%m-%d %H:%M:%S'),
            'LEMMA': self.LEMMA,
            'SAMPLE': self.SAMPLE,
            'FRAME_ID': self.FRAME_ID,
            'ELEMENT_ID': self.ELEMENT_ID,
        }
