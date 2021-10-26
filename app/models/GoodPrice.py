import uuid
from app import db
from flask_login import UserMixin, AnonymousUserMixin
from datetime import datetime


class GoodPrice(db.Model, UserMixin):
    __tablename__ = 'SHOP_GOOD_PRICE'

    ID = db.Column(db.String(50), primary_key=True, nullable=False, comment="ID")
    CREATE_DATETIME = db.Column(db.DateTime, index=True, default=datetime.now(), nullable=False, comment="创建时间")
    GOOD_ID = db.Column(db.String(50), db.ForeignKey('SHOP_GOOD.ID', ondelete='SET NULL'), comment="货物ID")
    START_NUM = db.Column(db.Integer, nullable=False, default=0, comment="起始数量")
    END_NUM = db.Column(db.Integer, nullable=False, default=0, comment="终止数量")
    PRICE = db.Column(db.DECIMAL(20, 3), nullable=False, default=0.000, comment="价格")

    def __repr__(self):
        return '<GoodPrice %r>\n' % self.NAME

    def to_json(self):
        return {
            'ID': self.ID,
            'CREATE_DATETIME': self.CREATE_DATETIME.strftime('%Y-%m-%d %H:%M:%S'),
            'GOOD_ID': self.GOOD_ID,
            'START_NUM': self.START_NUM,
            'END_NUM': self.END_NUM,
            'PRICE': self.PRICE,
        }
