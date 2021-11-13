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
from ..utils.get import *


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

    wish_goods = WishGood.query.filter_by(USER_ID=current_user.ID).all()
    goods_list = list()
    for wish_good in wish_goods:
        good_info = wish_good.to_json()
        good_info["GOOD"] = wish_good.good.to_json()
        good_info["GOOD"]["COLOR"] = get_color_op(wish_good.good.COLOR) if \
            lang_type == 'zh_cn' else wish_good.good.COLOR
        good_info["GOOD"]["CATEGORY"] = wish_good.good.category.NAME if \
            lang_type == 'zh_cn' else wish_good.good.category.EN_NAME
        good_info["GOOD"]["PRICE"] = "{}{}".format(
            get_currency_op(good_info["GOOD"]["CURRENCY"]), "%.2f" % good_info["GOOD"]["PRICE"])
        goods_list.append(good_info)
    return render_template("customer/wishlist.html", lang=lang[lang_type],
                           lang_type=lang_type, route="wishlist",
                           addition=set_addition(location="wishlist"),
                           data={"goods": goods_list})


@views.route('/<lang_type>/shoppingBag', methods=['GET', 'POST'])
@login_required
def shopping_bag(lang_type):
    """ 购物袋"""
    if lang_type not in ["zh_cn", "en_us"]:
        return render_template("404.html", lang_type=lang_type, route="shoppingBag")
    return render_template("customer/shoppingBag.html", lang=lang[lang_type],
                           lang_type=lang_type, route="shoppingBag",
                           addition=set_addition(location="shoppingBag"))


@views.route('/<lang_type>/sampleBag', methods=['GET', 'POST'])
@login_required
def sample_bag(lang_type):
    """ 样品袋"""
    if lang_type not in ["zh_cn", "en_us"]:
        return render_template("404.html", lang_type=lang_type, route="sampleBag")
    return render_template("customer/sampleBag.html", lang=lang[lang_type],
                           lang_type=lang_type, route="sampleBag",
                           addition=set_addition(location="sampleBag"))
