import uuid
from app import db
from flask_login import UserMixin, AnonymousUserMixin
from datetime import datetime


class GoodImg(db.Model, UserMixin):
    __tablename__ = 'SHOP_GOOD_IMG'

    ID = db.Column(db.String(50), primary_key=True, nullable=False, comment="ID")
    CREATE_DATETIME = db.Column(db.DateTime, index=True, default=datetime.now(), nullable=False, comment="创建时间")
    GOOD_ID = db.Column(db.String(50), db.ForeignKey('SHOP_GOOD.ID', ondelete='SET NULL'), comment="货物ID")
    URL = db.Column(db.String(255), nullable=False, default="", comment="地址")

    def __repr__(self):
        return '<GoodImg %r>\n' % self.PRICE

    def to_json(self):
        return {
            'ID': self.ID,
            'CREATE_DATETIME': self.CREATE_DATETIME.strftime('%Y-%m-%d %H:%M:%S'),
            'GOOD_ID': self.GOOD_ID,
            'URL': self.URL,
        }
