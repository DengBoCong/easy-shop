import uuid
from app import db
from flask_login import UserMixin, AnonymousUserMixin
from datetime import datetime

# 角色资源关联表
role_privilege_table = db.Table(
    'VERB_ROLE_PRIVILEGE', db.metadata,
    db.Column('ROLE_ID', db.String(50), db.ForeignKey('VERB_ROLE.ID', ondelete='CASCADE'), index=True),
    db.Column('PRIVILEGE_ID', db.String(50), db.ForeignKey('VERB_PRIVILEGE.ID', ondelete='CASCADE'), index=True),
    db.Column('CREATE_DATETIME', db.DateTime, default=datetime.now(), nullable=False, comment="创建时间"),
)


class Role(db.Model, UserMixin):
    __tablename__ = 'VERB_ROLE'

    ID = db.Column(db.String(50), primary_key=True, nullable=False, comment="ID")
    CREATE_DATETIME = db.Column(db.DateTime, default=datetime.now(), nullable=False, comment="创建时间")
    UPDATE_DATETIME = db.Column(db.DateTime, nullable=False, comment="更新时间")
    NAME = db.Column(db.String(30), nullable=False, default="", comment="权限角色名称")
    DESCRIPTION = db.Column(db.String(200), nullable=False, default="", comment="角色描述")
    ICON_CLS = db.Column(db.String(100), nullable=False, default="", comment="角色icon")
    TYPE = db.Column(db.SmallInteger, nullable=False, default=0, comment="角色创建类型0 自定义角色 1 系统角色")

    privilege = db.relationship('Privilege', secondary=role_privilege_table,
                                backref=db.backref('roles', lazy='dynamic'))

    users = db.relationship('User', backref='roles', lazy='dynamic')

    def get_id(self):
        return str(self.ID)

    def to_dict(self):
        return dict([(k, getattr(self, k)) for k in self.__dict__.keys() if not k.startswith("_")])

    def __repr__(self):
        return '<Role name:%r description:%r iconCls:%r>\n' % (self.NAME, self.DESCRIPTION, self.ICON_CLS)

    def to_json(self):
        return {
            'ID': self.ID,
            'CREATE_DATETIME': self.CREATE_DATETIME.strftime('%Y-%m-%d %H:%M:%S'),
            'UPDATE_DATETIME': self.UPDATE_DATETIME.strftime('%Y-%m-%d %H:%M:%S'),
            'NAME': self.NAME,
            'DESCRIPTION': self.DESCRIPTION,
            'ICON_CLS': self.ICON_CLS,
            'TYPE': self.TYPE,
        }
