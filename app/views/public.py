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
        return render_template("404.html", lang=lang[lang_type], lang_type=lang_type, route="login")
    return render_template("login.html", lang=lang[lang_type], lang_type=lang_type, route="login")


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


@views.route('/<lang_type>/men', methods=['GET', 'POST'])
def men(lang_type):
    """ 男装页"""
    if lang_type not in ["zh_cn", "en_us"]:
        return render_template("404.html", lang=lang[lang_type], lang_type=lang_type, route="men")
    return render_template("public/men.html", lang=lang[lang_type], lang_type=lang_type, route="men")


@views.route('/<lang_type>/women', methods=['GET', 'POST'])
def women(lang_type):
    """ 女装页"""
    if lang_type not in ["zh_cn", "en_us"]:
        return render_template("404.html", lang=lang[lang_type], lang_type=lang_type, route="women")
    return render_template("public/women.html", lang=lang[lang_type], lang_type=lang_type, route="women")


@views.route('/<lang_type>/kids', methods=['GET', 'POST'])
def kids(lang_type):
    """ 童装页"""
    if lang_type not in ["zh_cn", "en_us"]:
        return render_template("404.html", lang=lang[lang_type], lang_type=lang_type, route="kids")
    return render_template("public/kids.html", lang=lang[lang_type], lang_type=lang_type, route="kids")


@views.route('/<lang_type>/others', methods=['GET', 'POST'])
def others(lang_type):
    """ 其他页"""
    if lang_type not in ["zh_cn", "en_us"]:
        return render_template("404.html", lang=lang[lang_type], lang_type=lang_type, route="others")
    return render_template("public/others.html", lang=lang[lang_type], lang_type=lang_type, route="others")


@views.route('/<lang_type>/commonSample/<sub_page>', methods=['GET', 'POST'])
def sample(lang_type, sub_page):
    """ 样品页"""
    if lang_type not in ["zh_cn", "en_us"]:
        return render_template("404.html", lang=lang[lang_type], lang_type=lang_type, route=sub_page)
    return render_template("public/sample.html", lang=lang[lang_type], lang_type=lang_type, route=sub_page)


@views.route('/<lang_type>/designDiagrams/<sub_page>', methods=['GET', 'POST'])
def design_diagrams(lang_type, sub_page):
    """ 设计图页"""
    if lang_type not in ["zh_cn", "en_us"]:
        return render_template("404.html", lang=lang[lang_type], lang_type=lang_type, route=sub_page)
    return render_template("public/designDiagrams.html", lang=lang[lang_type], lang_type=lang_type, route=sub_page)


@views.route('/<lang_type>/referenceDiagrams/<sub_page>', methods=['GET', 'POST'])
def reference_diagrams(lang_type, sub_page):
    """ 参考图页"""
    if lang_type not in ["zh_cn", "en_us"]:
        return render_template("404.html", lang=lang[lang_type], lang_type=lang_type, route=sub_page)
    return render_template("public/referenceDiagrams.html", lang=lang[lang_type], lang_type=lang_type, route=sub_page)
