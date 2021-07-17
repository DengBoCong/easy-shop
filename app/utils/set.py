import uuid
from .. import db
from ..models import *
from flask import request
from datetime import datetime
from flask_login import current_user


def set_system_log(PATH, MESSAGE, ACTION, LEVEL):
    log = SystemLog(ID=uuid.uuid1(), PATH=PATH, LEVEL=LEVEL,
                    USER_NAME=current_user.NAME, USER_ID=current_user.ID, MESSAGE=MESSAGE, IP=request.remote_addr,
                    ACTION=ACTION, AGENT=request.headers.get("User-Agent"))
    db.session.add(log)
    db.session.commit()


def set_data_log(DATA, MESSAGE, ACTION, LEVEL):
    log = DataLog(ID=uuid.uuid1(), CREATE_DATETIME=datetime.now(), LEVEL=LEVEL, USER_NAME=current_user.NAME,
                  DESCRIPTION=MESSAGE, ACTION=ACTION, DATA=DATA)
    db.session.add(log)
    db.session.commit()
