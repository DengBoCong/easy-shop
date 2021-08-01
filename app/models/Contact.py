import uuid
from app import db
from flask_login import UserMixin, AnonymousUserMixin
from datetime import datetime


class Contact(db.Model, UserMixin):
    __tablename__ = 'SHOP_CONTACT'

    ID = db.Column(db.String(50), primary_key=True, nullable=False, comment="ID")
    CREATE_DATETIME = db.Column(db.DateTime, index=True, default=datetime.now(), nullable=False, comment="创建时间")
    UPDATE_DATETIME = db.Column(db.DateTime, nullable=False, comment="更新时间")
    NAME = db.Column(db.String(50), nullable=False, default="", comment="附件名称")
    PHONE = db.Column(db.String(20), nullable=False, default="", comment="手机号")
    EMAIL = db.Column(db.String(60), index=True, nullable=False, default="", comment="邮箱账号")
    WE_CHAT = db.Column(db.String(30), nullable=False, default="", comment="微信号")
    QQ = db.Column(db.String(20), nullable=False, default="", comment="QQ号")

    def to_json(self):
        return {
            'ID': self.ID,
            'CREATE_DATETIME': self.CREATE_DATETIME.strftime('%Y-%m-%d %H:%M:%S'),
            'UPDATE_DATETIME': self.UPDATE_DATETIME.strftime('%Y-%m-%d %H:%M:%S'),
            'NAME': self.NAME,
            'PHONE': self.PHONE,
            'EMAIL': self.EMAIL,
            'WE_CHAT': self.WE_CHAT,
            'QQ': self.QQ,
        }

    def __repr__(self):
        return '<VerbContact name:%r>\n' % self.NAME
