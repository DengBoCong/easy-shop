import uuid
from app import db
from flask_login import UserMixin, AnonymousUserMixin
from datetime import datetime


class System(db.Model, UserMixin):
    __tablename__ = 'SHOP_SYSTEM'

    ID = db.Column(db.String(50), primary_key=True, nullable=False, comment="ID")
    CREATE_DATETIME = db.Column(db.DateTime, index=True, default=datetime.now(), nullable=False, comment="创建时间")
    INDEX_MEN = db.Column(db.String(255), nullable=False, default="", comment="首页男装")
    INDEX_WOMEN = db.Column(db.String(255), nullable=False, default="", comment="首页女装")
    INDEX_NEW = db.Column(db.String(255), nullable=False, default="", comment="首页新品")
    ABOUT_US = db.Column(db.Text, nullable=False, default="", comment="关于我们")
    CONTACT_US = db.Column(db.Text, nullable=False, default="", comment="联系我们")

    def __repr__(self):
        return '<System %r>\n' % self.ID

    def to_json(self):
        return {
            'ID': self.ID,
            'CREATE_DATETIME': self.CREATE_DATETIME.strftime('%Y-%m-%d %H:%M:%S'),
            'INDEX_MEN': self.INDEX_MEN,
            'INDEX_WOMEN': self.INDEX_WOMEN,
            'INDEX_NEW': self.INDEX_NEW,
            'ABOUT_US': self.ABOUT_US,
            'CONTACT_US': self.CONTACT_US,
        }
