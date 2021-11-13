import uuid
from app import db
from flask_login import UserMixin, AnonymousUserMixin
from datetime import datetime


class ShoppingGood(db.Model, UserMixin):
    __tablename__ = 'SHOP_SHOPPING_GOOD'

    ID = db.Column(db.String(50), primary_key=True, nullable=False, comment="ID")
    CREATE_DATETIME = db.Column(db.DateTime, index=True, default=datetime.now(), nullable=False, comment="创建时间")
    USER_ID = db.Column(db.String(50), db.ForeignKey('SHOP_USER.ID', ondelete='SET NULL'), comment="USER ID")
    GOOD_ID = db.Column(db.String(50), db.ForeignKey('SHOP_GOOD.ID', ondelete='SET NULL'), comment="GOOD ID")
    SIZE = db.Column(db.String(20), nullable=False, default="", comment="尺码")
    NUM = db.Column(db.Integer, nullable=False, default=0, comment="数量")

    def __repr__(self):
        return '<ShoppingGood %r>\n' % self.ID

    def to_json(self):
        return {
            'ID': self.ID,
            'CREATE_DATETIME': self.CREATE_DATETIME.strftime('%Y-%m-%d %H:%M:%S'),
            'USER_ID': self.USER_ID,
            'GOOD_ID': self.GOOD_ID,
            'SIZE': self.SIZE,
            'NUM': self.NUM
        }
