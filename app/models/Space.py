import uuid
from app import db
from flask_login import UserMixin, AnonymousUserMixin
from datetime import datetime

# 角色资源关联表
space_user_table = db.Table(
    'VERB_SPACE_USER', db.metadata,
    db.Column('SPACE_ID', db.String(50), db.ForeignKey('VERB_SPACE.ID', ondelete='CASCADE')),
    db.Column('USER_ID', db.String(50), db.ForeignKey('VERB_USER.ID', ondelete='CASCADE')),
    db.Column('CREATE_DATETIME', db.DateTime, default=datetime.now(), nullable=False, comment="创建时间"),
    db.Column('PRIVILEGE', db.SmallInteger, default=0, nullable=False, comment="空间成员操作权限 0 浏览者 1 编辑者 2 管理员"),
)


class Space(db.Model, UserMixin):
    __tablename__ = 'VERB_SPACE'

    ID = db.Column(db.String(50), primary_key=True, nullable=False, comment="ID")
    CREATE_DATETIME = db.Column(db.DateTime, default=datetime.now(), nullable=False, comment="创建时间")
    UPDATE_DATETIME = db.Column(db.DateTime, nullable=False, comment="更新时间")
    NAME = db.Column(db.String(50), nullable=False, default="", comment="空间名称")
    DESCRIPTION = db.Column(db.String(200), nullable=False, default="", comment="空间描述")
    TAGS = db.Column(db.String(255), nullable=False, default="", comment="空间标签，用英文逗号隔开")
    VISIT_LEVEL = db.Column(db.Enum('private', 'public'), nullable=False,
                            default="public", comment="访问级别：private,public")
    IF_EXPORT = db.Column(db.Boolean, nullable=False, default=True, comment="空间下数据是否允许导出")

    users = db.relationship('User', secondary=space_user_table,
                            backref=db.backref('spaces', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return '<Space name:%r description:%r>\n' % (self.NAME, self.DESCRIPTION)

    def to_json(self):
        return {
            'ID': self.ID,
            'CREATE_DATETIME': self.CREATE_DATETIME.strftime('%Y-%m-%d %H:%M:%S'),
            'UPDATE_DATETIME': self.UPDATE_DATETIME.strftime('%Y-%m-%d %H:%M:%S'),
            'NAME': self.NAME,
            'DESCRIPTION': self.DESCRIPTION,
            'TAGS': self.TAGS,
            'VISIT_LEVEL': self.VISIT_LEVEL,
            'IF_EXPORT': self.IF_EXPORT,
        }
