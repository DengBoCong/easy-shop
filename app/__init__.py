from config import config
from app import setting
from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_caching import Cache

loginManager = LoginManager()
loginManager.session_protection = "strong"
loginManager.login_view = "views.not_login"
loginManager.login_message = "请重新登录"

bootstrap = Bootstrap()
mail = Mail()
db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_object(config[config_name])
    config[config_name].init_app(app=app)
    app.secret_key = setting.SECRET_KEY  # 设置表单交互密钥
    app.jinja_env.variable_start_string = "[["
    app.jinja_env.variable_end_string = "]]"
    # cache = Cache(config={'CACHE_TYPE': 'filesystem', 'CACHE_DIR': ''})
    cache = Cache(config={'CACHE_TYPE': 'simple'})

    mail.init_app(app)
    bootstrap.init_app(app)
    db.init_app(app)
    loginManager.init_app(app)
    cache.init_app(app)

    from .controllers import controllers
    from .views import views
    app.register_blueprint(controllers)
    app.register_blueprint(views)

    return app
