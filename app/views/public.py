import re
import json
from . import views
from flask import jsonify
from flask import render_template, request
from flask_login import login_required, logout_user
from datetime import datetime
from ..i18 import lang


@views.route('/<lang_type>/login', methods=['GET', 'POST'])
def login(lang_type):
    """ 登入页"""
    if lang_type not in ["zh_cn", "en_us"]:
        return render_template("404.html", lang=lang[lang_type])
    return render_template("login.html", lang=lang[lang_type])
