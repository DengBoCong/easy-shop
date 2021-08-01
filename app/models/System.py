import uuid
from app import db
from flask_login import UserMixin, AnonymousUserMixin
from datetime import datetime


class System(db.Model, UserMixin):
    __tablename__ = 'SHOP_SYSTEM'

    ID = db.Column(db.String(50), primary_key=True, nullable=False, comment="ID")
    CREATE_DATETIME = db.Column(db.DateTime, default=datetime.now(), nullable=False, comment="创建时间")
    UPDATE_DATETIME = db.Column(db.DateTime, nullable=False, comment="更新时间")
    SITE_NAME = db.Column(db.String(64), nullable=False, default="中文动词语义网", comment="网站名称")
    ALLOW_LOGIN = db.Column(db.Boolean, nullable=False, default=True, comment="是否允许登录")
    COPY_RIGHT_INFO = db.Column(db.String(100), nullable=False, default="", comment="版权信息")
    IF_EMAIL = db.Column(db.Boolean, nullable=False, default=False, comment="是否开启邮件通知")
    VERSION = db.Column(db.String(10), nullable=False, default="v0.0.0", comment="系统版本号")
    TITLE = db.Column(db.String(30), nullable=False, default="欢迎使用管理系统", comment="通知标题")
    DESCRIPTION = db.Column(db.String(300), nullable=False, default="", comment="通知内容")
    DOMAIN_NAME = db.Column(db.String(100), nullable=False, default="", comment="网站域名")

    def to_json(self):
        return {
            'ID': self.ID,
            'CREATE_DATETIME': self.CREATE_DATETIME.strftime('%Y-%m-%d %H:%M:%S'),
            'UPDATE_DATETIME': self.UPDATE_DATETIME.strftime('%Y-%m-%d %H:%M:%S'),
            'SITE_NAME': self.SITE_NAME,
            'ALLOW_LOGIN': self.ALLOW_LOGIN,
            'COPY_RIGHT_INFO': self.COPY_RIGHT_INFO,
            'IF_EMAIL': self.IF_EMAIL,
            'VERSION': self.VERSION,
            'TITLE': self.TITLE,
            'DESCRIPTION': self.DESCRIPTION,
            'DOMAIN_NAME': self.DOMAIN_NAME,
        }

    def __repr__(self):
        return '<VerbSystem name:%r>\n' % self.SITE_NAME
