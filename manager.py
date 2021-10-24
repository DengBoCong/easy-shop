#!/usr/bin/env python
from app import create_app, db
from app import setting
from app.models import *
from flask import g
from flask import render_template
from flask_migrate import Migrate
from flask_migrate import MigrateCommand
from flask_script import Manager
from flask_script import Shell

app = create_app(setting.FLASK_CONFIG or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error/404.html'), 404


@app.errorhandler(403)
def page_not_found(e):
    return render_template('error/403.html'), 403


@app.errorhandler(401)
def page_not_found(e):
    return render_template("user/app/templates/login.html"), 401


with app.app_context():
    g.contextPath = ''


def make_shell_context():
    return dict(app=app, db=db, User=User)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def myprint():
    print('hello world')


if __name__ == '__main__':
    manager.run()
