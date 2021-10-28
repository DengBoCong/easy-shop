import uuid
from app import db
from flask_login import UserMixin, AnonymousUserMixin
from datetime import datetime


class GoodCategory(db.Model, UserMixin):
    __tablename__ = 'SHOP_GOOD_CATEGORY'

    ID = db.Column(db.String(50), primary_key=True, nullable=False, comment="ID")
    CREATE_DATETIME = db.Column(db.DateTime, index=True, default=datetime.now(), nullable=False, comment="创建时间")
    NAME = db.Column(db.String(100), nullable=False, default="", comment="名称")
    EN_NAME = db.Column(db.String(100), nullable=False, default="", comment="英文名称")
    DESCRIPTION = db.Column(db.String(255), nullable=False, default="", comment="备注")

    def __repr__(self):
        return '<GoodCategory %r>\n' % self.NAME

    def to_json(self):
        return {
            'ID': self.ID,
            'CREATE_DATETIME': self.CREATE_DATETIME.strftime('%Y-%m-%d %H:%M:%S'),
            'NAME': self.NAME,
            'EN_NAME': self.EN_NAME,
            'DESCRIPTION': self.DESCRIPTION,
        }
