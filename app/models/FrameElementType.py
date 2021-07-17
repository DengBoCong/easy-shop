import uuid
from app import db
from flask_login import UserMixin, AnonymousUserMixin
from datetime import datetime


class FrameElementType(db.Model, UserMixin):
    __tablename__ = 'VERB_FRAME_ELEMENT_TYPE'

    ID = db.Column(db.String(50), primary_key=True, nullable=False, comment="ID")
    CREATE_DATETIME = db.Column(db.DateTime, default=datetime.now(), nullable=False, comment="创建时间")
    TYPE = db.Column(db.Enum('Core Frame Elements', 'Non-core Frame Elements', 'Construction Marker'),
                     nullable=False, comment="类别")
    NAME = db.Column(db.String(50), nullable=False, default="", comment="名称")

    elements = db.relationship('FrameElement', backref='type', lazy='dynamic')

    def __repr__(self):
        return '<FrameElementType name:%r>\n' % self.TAG

    def to_json(self):
        return {
            'ID': self.ID,
            'CREATE_DATETIME': self.CREATE_DATETIME.strftime('%Y-%m-%d %H:%M:%S'),
            'TYPE': self.TYPE,
            'NAME': self.NAME
        }
