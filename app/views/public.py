import re
import json
from . import views
from flask import jsonify
from flask import render_template, request
from flask_login import login_required, logout_user
from datetime import datetime
from ..i18 import lang
from ..utils import set_addition


@views.route('/<lang_type>/login', methods=['GET', 'POST'])
def login(lang_type):
    """ 登入页"""
    if lang_type not in ["zh_cn", "en_us"]:
        return render_template("404.html", lang_type=lang_type, route="login")
    return render_template("login.html", lang=lang[lang_type],
                           lang_type=lang_type, route="login", addition=set_addition(location="login"))


@views.route('/<lang_type>/index', methods=['GET', 'POST'])
def index(lang_type):
    """ 首页"""
    if lang_type not in ["zh_cn", "en_us"]:
        return render_template("404.html", lang_type=lang_type, route="index")
    return render_template("index.html", lang=lang[lang_type],
                           lang_type=lang_type, route="index", addition=set_addition())


@views.route('/<lang_type>/aboutUs', methods=['GET', 'POST'])
def about_us(lang_type):
    """ 关于我们页"""
    if lang_type not in ["zh_cn", "en_us"]:
        return render_template("404.html", lang=lang[lang_type], lang_type=lang_type, route="aboutUs")
    return render_template("public/aboutUs.html", lang=lang[lang_type],
                           lang_type=lang_type, route="aboutUs", addition=set_addition(location="aboutUs"))


@views.route('/<lang_type>/contactUs', methods=['GET', 'POST'])
def contact_us(lang_type):
    """ 联系我们页"""
    if lang_type not in ["zh_cn", "en_us"]:
        return render_template("404.html", lang=lang[lang_type], lang_type=lang_type, route="contactUs")
    return render_template("public/contactUs.html", lang=lang[lang_type],
                           lang_type=lang_type, route="contactUs", addition=set_addition(location="contactUs"))


@views.route('/<lang_type>/commonSample', methods=['GET', 'POST'])
def sample(lang_type):
    """ 样品页"""
    info_data = request.args.to_dict()
    lang_type, sub_page = lang_type.split("-")

    addition = set_addition(add="-" + sub_page, categories="sample", page=info_data.get("page", 1),
                            products=info_data.get("products", ""), sort=info_data.get("sort", ""),
                            colors=info_data.get("colors", ""), location=sub_page)

    if lang_type not in ["zh_cn", "en_us"]:
        return render_template("404.html", lang_type=lang_type, route="commonSample")
    return render_template("public/sample.html", lang=lang[lang_type],
                           lang_type=lang_type, route="commonSample", addition=addition)


@views.route('/<lang_type>/designDiagrams', methods=['GET', 'POST'])
def design_diagrams(lang_type):
    """ 设计图页"""
    info_data = request.args.to_dict()
    lang_type, sub_page = lang_type.split("-")

    addition = set_addition(add="-" + sub_page, categories="design", page=info_data.get("page", 1),
                            products=info_data.get("products", ""), sort=info_data.get("sort", ""),
                            colors=info_data.get("colors", ""), location=sub_page)

    if lang_type not in ["zh_cn", "en_us"]:
        return render_template("404.html", lang_type=lang_type, route="designDiagrams")
    return render_template("public/designDiagrams.html", lang=lang[lang_type],
                           lang_type=lang_type, route="designDiagrams", addition=addition)


@views.route('/<lang_type>/referenceDiagrams', methods=['GET', 'POST'])
def reference_diagrams(lang_type):
    """ 参考图页"""
    info_data = request.args.to_dict()
    lang_type, sub_page = lang_type.split("-")

    addition = set_addition(add="-" + sub_page, categories="reference", page=info_data.get("page", 1),
                            products=info_data.get("products", ""), sort=info_data.get("sort", ""),
                            colors=info_data.get("colors", ""), location=sub_page)

    if lang_type not in ["zh_cn", "en_us"]:
        return render_template("404.html", lang_type=lang_type, route="referenceDiagrams")
    return render_template("public/referenceDiagrams.html", lang=lang[lang_type],
                           lang_type=lang_type, route="referenceDiagrams", addition=addition)
