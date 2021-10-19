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
        return render_template("404.html", lang_type=lang_type, route="login")
    return render_template("login.html", lang=lang[lang_type], lang_type=lang_type, route="login")


@views.route('/<lang_type>/index', methods=['GET', 'POST'])
def index(lang_type):
    """ 首页"""
    if lang_type not in ["zh_cn", "en_us"]:
        return render_template("404.html", lang_type=lang_type, route="login")
    return render_template("index.html", lang=lang[lang_type], lang_type=lang_type, route="index")


@views.route('/<lang_type>/aboutUs', methods=['GET', 'POST'])
def about_us(lang_type):
    """ 关于我们页"""
    if lang_type not in ["zh_cn", "en_us"]:
        return render_template("404.html", lang=lang[lang_type], lang_type=lang_type, route="aboutUs")
    return render_template("public/aboutUs.html", lang=lang[lang_type], lang_type=lang_type, route="aboutUs")


@views.route('/<lang_type>/contactUs', methods=['GET', 'POST'])
def contact_us(lang_type):
    """ 联系我们页"""
    if lang_type not in ["zh_cn", "en_us"]:
        return render_template("404.html", lang=lang[lang_type], lang_type=lang_type, route="contactUs")
    return render_template("public/contactUs.html", lang=lang[lang_type], lang_type=lang_type, route="contactUs")


@views.route('/<lang_type>/commonSample', methods=['GET', 'POST'])
def sample(lang_type):
    """ 样品页"""
    lang_type, sub_page = lang_type.split("-")
    if lang_type not in ["zh_cn", "en_us"]:
        return render_template("404.html", lang_type=lang_type, route="login")
    return render_template("public/sample.html", lang=lang[lang_type],
                           lang_type=lang_type, route="commonSample")


@views.route('/<lang_type>/designDiagrams', methods=['GET', 'POST'])
def design_diagrams(lang_type, sub_page):
    """ 设计图页"""
    lang_type, sub_page = lang_type.split("-")
    if lang_type not in ["zh_cn", "en_us"]:
        return render_template("404.html", lang_type=lang_type, route="login")
    return render_template("public/designDiagrams.html", lang=lang[lang_type],
                           lang_type=lang_type, route="designDiagrams")


@views.route('/<lang_type>/referenceDiagrams', methods=['GET', 'POST'])
def reference_diagrams(lang_type, sub_page):
    """ 参考图页"""
    lang_type, sub_page = lang_type.split("-")
    if lang_type not in ["zh_cn", "en_us"]:
        return render_template("404.html", lang_type=lang_type, route="login")
    return render_template("public/referenceDiagrams.html", lang=lang[lang_type],
                           lang_type=lang_type, route="referenceDiagrams")
