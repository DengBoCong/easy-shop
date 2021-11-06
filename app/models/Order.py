import uuid
from app import db
from flask_login import UserMixin, AnonymousUserMixin
from datetime import datetime


class Order(db.Model, UserMixin):
    __tablename__ = 'SHOP_ORDER'

    ID = db.Column(db.String(50), primary_key=True, nullable=False, comment="ID")
    CREATE_DATETIME = db.Column(db.DateTime, index=True, default=datetime.now(), nullable=False, comment="创建时间")
    NUM = db.Column(db.String(100), nullable=False, default="", comment="订单编号")
    TOTAL_AMOUNT = db.Column(db.DECIMAL(20, 3), nullable=False, default=0.000, comment="总额")
    STATUS = db.Column(db.String(30), nullable=False, default="", comment="订单状态")
    TRACK_NUM = db.Column(db.String(100), nullable=False, default="", comment="追踪编号")
    USER_ID = db.Column(db.String(50), db.ForeignKey('SHOP_USER.ID', ondelete='SET NULL'), comment="USER ID")

    orderGoods = db.relationship('OrderGood', backref='order', lazy='dynamic')

    def __repr__(self):
        return '<Order %r>\n' % self.NUM

    def to_json(self):
        return {
            'ID': self.ID,
            'CREATE_DATETIME': self.CREATE_DATETIME.strftime('%Y-%m-%d %H:%M:%S'),
            'NUM': self.NUM,
            'TOTAL_AMOUNT': self.TOTAL_AMOUNT,
            'STATUS': self.STATUS,
            'TRACK_NUM': self.TRACK_NUM,
            'USER_ID': self.USER_ID
        }
