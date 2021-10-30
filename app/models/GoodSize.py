import uuid
from app import db
from flask_login import UserMixin, AnonymousUserMixin
from datetime import datetime


class GoodSize(db.Model, UserMixin):
    __tablename__ = 'SHOP_GOOD_SIZE'

    ID = db.Column(db.String(50), primary_key=True, nullable=False, comment="ID")
    CREATE_DATETIME = db.Column(db.DateTime, index=True, default=datetime.now(), nullable=False, comment="创建时间")
    SIZE = db.Column(db.String(30), nullable=False, default="", comment="尺码")
    DESCRIPTION = db.Column(db.String(100), nullable=False, default="", comment="备注")

    def __repr__(self):
        return '<GoodSize %r>\n' % self.SIZE

    def to_json(self):
        return {
            'ID': self.ID,
            'CREATE_DATETIME': self.CREATE_DATETIME.strftime('%Y-%m-%d %H:%M:%S'),
            'SIZE': self.SIZE,
            'DESCRIPTION': self.DESCRIPTION,
        }
