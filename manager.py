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
from app.utils.get import get_system_info

app = create_app(setting.FLASK_CONFIG or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


@app.errorhandler(404)
def page_not_found(e):
    info = get_system_info()
    return render_template('error/404.html', message=info), 404


@app.errorhandler(403)
def page_not_found(e):
    info = get_system_info()
    return render_template('error/403.html', message=info), 403


@app.errorhandler(401)
def page_not_found(e):
    info = get_system_info()
    return render_template("user/login.html", message=info), 401


with app.app_context():
    g.contextPath = ''


def make_shell_context():
    return dict(app=app, db=db, Attachment=Attachment, Config=Config, Contact=Contact, DataLog=DataLog,
                Email=Email, Frame=Frame, FrameElement=FrameElement, FrameElementType=FrameElementType,
                HomePage=HomePage, Link=Link, Notice=Notice, OnLine=OnLine, Privilege=Privilege, Role=Role,
                Sample=Sample, Space=Space, System=System, SystemLog=SystemLog, User=User, Verb=Verb,
                VerbPattern=VerbPattern)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def myprint():
    print('hello world')


if __name__ == '__main__':
    manager.run()
