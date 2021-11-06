import uuid
from app import db
from flask_login import UserMixin, AnonymousUserMixin
from datetime import datetime


class OrderGood(db.Model, UserMixin):
    __tablename__ = 'SHOP_ORDER_GOOD'

    ID = db.Column(db.String(50), primary_key=True, nullable=False, comment="ID")
    CREATE_DATETIME = db.Column(db.DateTime, index=True, default=datetime.now(), nullable=False, comment="创建时间")
    ORDER_ID = db.Column(db.String(50), db.ForeignKey('SHOP_ORDER.ID', ondelete='SET NULL'), comment="ORDER ID")
    GOOD_ID = db.Column(db.String(50), db.ForeignKey('SHOP_GOOD.ID', ondelete='SET NULL'), comment="GOOD ID")
    NUM = db.Column(db.Integer, nullable=False, default=0, comment="数量")
    TITLE = db.Column(db.String(150), nullable=False, default="", comment="保留展示描述")
    PRICE = db.Column(db.DECIMAL(20, 3), nullable=False, default=0.000, comment="单个价格")
    EMAIL = db.Column(db.String(60), index=True, nullable=False, default="", unique=True, comment="货物联系邮箱账号")

    def __repr__(self):
        return '<OrderGood %r>\n' % self.ID

    def to_json(self):
        return {
            'ID': self.ID,
            'CREATE_DATETIME': self.CREATE_DATETIME.strftime('%Y-%m-%d %H:%M:%S'),
            'ORDER_ID': self.ORDER_ID,
            'GOOD_ID': self.GOOD_ID,
            'NUM': self.NUM,
            'TITLE': self.TITLE,
            'PRICE': self.PRICE,
            'EMAIL': self.EMAIL
        }
