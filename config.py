import os
from datetime import timedelta
from flask import Flask

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # Session相关
    PERMANENT_SESSION_LIFETIME = timedelta(hours=3)

    # 数据库相关
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = False

    # 邮件相关
    FLASKY_MAIL_SENDER = "1210212670@qq.com"

    @classmethod
    def init_app(cls, app: Flask):
        # 设置连接数据库的URL
        app.config["SQLALCHEMY_DATABASE_URI"] = cls.SQLALCHEMY_DATABASE_URI
        # 设置每次请求结束后会自动提交数据库中的改动
        app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = cls.SQLALCHEMY_COMMIT_ON_TEARDOWN
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = cls.SQLALCHEMY_TRACK_MODIFICATIONS
        # 查询时会显示原始SQL语句
        app.config["SQLALCHEMY_ECHO"] = cls.SQLALCHEMY_ECHO


class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = "1210212670@qq.com"  #os.environ.get('')
    MAIL_PASSWORD = "opkewimdfbnbhcgc"  #os.environ.get('')
    SQLALCHEMY_DATABASE_URI = "mysql://root:Andie130857@localhost:3306/easyshop?charset=utf8&autocommit=true"


class TestingConfig(Config):
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'mysql://root:Andie130857@localhost:3306/easyshop?charset=utf8&autocommit=true'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://root:Andie130857@localhost:3306/easyshop?charset=utf8&autocommit=true'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
