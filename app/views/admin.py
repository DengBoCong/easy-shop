from . import views
from flask import jsonify
from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user
from datetime import datetime
from ..services.auth import permission_required
from ..utils.set import set_addition
from ..i18 import lang


@views.route('/<lang_type>/editProducts', methods=['GET', 'POST'])
@login_required
def edit_single_product(lang_type):
    """ 编辑产品"""
    lang_type, sub_page = lang_type.split("-")

    if lang_type not in ["zh_cn", "en_us"]:
        return render_template("404.html", lang_type=lang_type, route="editProducts")
    return render_template("admin/editProducts.html", lang=lang[lang_type],
                           lang_type=lang_type, route="editProducts",
                           addition=set_addition(add="-" + sub_page, location=sub_page))


@views.route('/<lang_type>/publishedProduct', methods=['GET', 'POST'])
@login_required
def published_product(lang_type):
    """ 已发布产品"""
    if lang_type not in ["zh_cn", "en_us"]:
        return render_template("404.html", lang_type=lang_type, route="publishedProduct")
    return render_template("admin/publishedProduct.html", lang=lang[lang_type],
                           lang_type=lang_type, route="publishedProduct",
                           addition=set_addition(location="publishedProduct"))


@views.route('/<lang_type>/customerAccountInfo', methods=['GET', 'POST'])
@login_required
def customer_account_info(lang_type):
    """ 客户信息"""
    if lang_type not in ["zh_cn", "en_us"]:
        return render_template("404.html", lang_type=lang_type, route="customerAccountInfo")
    return render_template("admin/customerAccountInfo.html", lang=lang[lang_type],
                           lang_type=lang_type, route="customerAccountInfo",
                           addition=set_addition(location="customerAccountInfo"))


@views.route('/<lang_type>/addUser', methods=['GET', 'POST'])
@login_required
def add_user(lang_type):
    """ 添加账户"""
    if lang_type not in ["zh_cn", "en_us"]:
        return render_template("404.html", lang_type=lang_type, route="addUser")
    return render_template("admin/addUser.html", lang=lang[lang_type],
                           lang_type=lang_type, route="addUser",
                           addition=set_addition(location="addUser"))
