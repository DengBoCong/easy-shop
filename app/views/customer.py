import re
import json
from . import views
from flask import jsonify
from flask import render_template, request
from flask_login import login_required, logout_user, current_user
from datetime import datetime
from ..i18 import lang
from ..utils import set_addition
from ..models import *


@views.route('/<lang_type>/accountDetail', methods=['GET', 'POST'])
@login_required
def account_detail(lang_type):
    """ 用户详情"""
    if lang_type not in ["zh_cn", "en_us"]:
        return render_template("404.html", lang_type=lang_type, route="accountDetail")

    # user = User.query.get(current_user.ID)
    # area = {"zh_cn": user.area.NAME, "en_us": user.area.EN_NAME}
    # data={"area": area}

    return render_template("customer/accountDetail.html", lang=lang[lang_type],
                           lang_type=lang_type, route="accountDetail",
                           addition=set_addition(location="login", categories="accountDetail"))


@views.route('/<lang_type>/historyOrders', methods=['GET', 'POST'])
@login_required
def history_orders(lang_type):
    """ 历史订单"""
    if lang_type not in ["zh_cn", "en_us"]:
        return render_template("404.html", lang_type=lang_type, route="historyOrders")
    return render_template("customer/historyOrders.html", lang=lang[lang_type],
                           lang_type=lang_type, route="historyOrders",
                           addition=set_addition(location="login", categories="historyOrders"))


@views.route('/<lang_type>/historySamples', methods=['GET', 'POST'])
@login_required
def history_samples(lang_type):
    """ 历史打样"""
    if lang_type not in ["zh_cn", "en_us"]:
        return render_template("404.html", lang_type=lang_type, route="historySamples")
    return render_template("customer/historySamples.html", lang=lang[lang_type],
                           lang_type=lang_type, route="historySamples",
                           addition=set_addition(location="login", categories="historySamples"))


@views.route('/<lang_type>/wishlist', methods=['GET', 'POST'])
@login_required
def wishlist(lang_type):
    """ 愿望清单"""
    if lang_type not in ["zh_cn", "en_us"]:
        return render_template("404.html", lang_type=lang_type, route="wishlist")
    return render_template("customer/wishlist.html", lang=lang[lang_type],
                           lang_type=lang_type, route="wishlist",
                           addition=set_addition(location="wishlist"))


@views.route('/<lang_type>/shoppingBag', methods=['GET', 'POST'])
@login_required
def shopping_bag(lang_type):
    """ 购物袋"""
    if lang_type not in ["zh_cn", "en_us"]:
        return render_template("404.html", lang_type=lang_type, route="shoppingBag")
    return render_template("customer/shoppingBag.html", lang=lang[lang_type],
                           lang_type=lang_type, route="shoppingBag",
                           addition=set_addition(location="shoppingBag"))
