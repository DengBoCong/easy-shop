import uuid
from app import db
from flask_login import UserMixin, AnonymousUserMixin
from datetime import datetime

frame_element_frame_table = db.Table(
    'VERB_FRAME_ELEMENT_FRAME', db.metadata,
    db.Column('FRAME_ELEMENT_ID', db.String(50), db.ForeignKey('VERB_FRAME_ELEMENT.ID',
                                                               ondelete='CASCADE'), index=True),
    db.Column('FRAME_ID', db.String(50), db.ForeignKey('VERB_FRAME.ID', ondelete='CASCADE'), index=True)
)


class FrameElement(db.Model, UserMixin):
    __tablename__ = 'VERB_FRAME_ELEMENT'

    ID = db.Column(db.String(50), primary_key=True, nullable=False, comment="ID")
    CREATE_DATETIME = db.Column(db.DateTime, default=datetime.now(), nullable=False, comment="创建时间")
    DEF = db.Column(db.String(255), nullable=False, default="", comment="Def")
    ELEMENT_TYPE_ID = db.Column(db.String(50), db.ForeignKey('VERB_FRAME_ELEMENT_TYPE.ID', ondelete='SET NULL'),
                                comment="Element Type")

    frames = db.relationship('Frame', secondary=frame_element_frame_table,
                             backref=db.backref('frameElements', lazy='dynamic'))
    elementSamples = db.relationship('FrameElementSample', backref='element', lazy='dynamic')

    def __repr__(self):
        return '<FrameElement def:%r>\n' % self.DEF

    def to_json(self):
        return {
            'ID': self.ID,
            'CREATE_DATETIME': self.CREATE_DATETIME.strftime('%Y-%m-%d %H:%M:%S'),
            'DEF': self.DEF,
            'ELEMENT_TYPE_ID': self.ELEMENT_TYPE_ID,
        }
