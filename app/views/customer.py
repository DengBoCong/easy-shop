import re
import json
from . import views
from flask import jsonify
from flask import render_template, request
from flask_login import login_required, logout_user, current_user
from sqlalchemy import asc, desc, and_, or_
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

    shopping_goods = ShoppingGood.query.filter_by(USER_ID=current_user.ID).all()
    goods_list = list()
    amount, shipping = 0.0, 0.0
    for shopping_good in shopping_goods:
        good_info = shopping_good.to_json()
        good_info["GOOD"] = shopping_good.good.to_json()
        good_info["GOOD"]["COLOR"] = get_color_op(shopping_good.good.COLOR) if \
            lang_type == 'zh_cn' else shopping_good.good.COLOR
        good_info["GOOD"]["CATEGORY"] = shopping_good.good.category.NAME if \
            lang_type == 'zh_cn' else shopping_good.good.category.EN_NAME
        good_info["GOOD"]["PRICE"] = "{}{} {}".format(
            get_currency_op(good_info["GOOD"]["CURRENCY"]),
            "%.2f" % good_info["GOOD"]["PRICE"],
            get_currency_lang_op(good_info["GOOD"]["CURRENCY"])
        )

        amount += float(shopping_good.good.PRICE) * shopping_good.NUM
        goods_list.append(good_info)

    total_amount = amount if len(goods_list) == 0 else "{}{} {}".format(
        get_currency_op(goods_list[0]["GOOD"]["CURRENCY"]),
        "%.2f" % amount,
        get_currency_lang_op(goods_list[0]["GOOD"]["CURRENCY"])
    )

    shipping_cost = shipping if len(goods_list) == 0 else "{}{} {}".format(
        get_currency_op(goods_list[0]["GOOD"]["CURRENCY"]),
        "%.2f" % shipping,
        get_currency_lang_op(goods_list[0]["GOOD"]["CURRENCY"])
    )

    trending_goods = Good.query.filter(
        Good.AREA_ID.like("%" + current_user.AREA_ID + "%")
    ).order_by(desc(Good.NUM)).all()
    trending_goods_list = list()
    for trending_good in trending_goods:
        trending_good_info = trending_good.to_json()
        trending_good_info["TYPE"] = trending_good_info["TYPE"].lower()
        trending_good_info["COLOR"] = get_color_op(
            trending_good_info["COLOR"]) if lang_type == 'zh_cn' else trending_good_info["COLOR"]
        trending_good_info[
            "CATEGORY"] = trending_good.category.NAME if lang_type == 'zh_cn' else trending_good.category.EN_NAME

        trending_goods_list.append(trending_good_info)

    return render_template("customer/shoppingBag.html", lang=lang[lang_type],
                           lang_type=lang_type, route="shoppingBag",
                           addition=set_addition(location="shoppingBag"),
                           data={"goods": goods_list, "totalAmount": total_amount,
                                 "shippingCost": shipping_cost, "trendingGoods": trending_goods_list})


@views.route('/<lang_type>/sampleBag', methods=['GET', 'POST'])
@login_required
def sample_bag(lang_type):
    """ 样品袋"""
    if lang_type not in ["zh_cn", "en_us"]:
        return render_template("404.html", lang_type=lang_type, route="sampleBag")

    sample_goods = SampleGood.query.filter_by(USER_ID=current_user.ID).all()
    goods_list = list()
    amount, shipping = 0.0, 0.0
    for sample_good in sample_goods:
        good_info = sample_good.to_json()
        good_info["GOOD"] = sample_good.good.to_json()
        good_info["GOOD"]["COLOR"] = get_color_op(sample_good.good.COLOR) if \
            lang_type == 'zh_cn' else sample_good.good.COLOR
        good_info["GOOD"]["CATEGORY"] = sample_good.good.category.NAME if \
            lang_type == 'zh_cn' else sample_good.good.category.EN_NAME
        good_info["GOOD"]["PRICE"] = "{}{} {}".format(
            get_currency_op(good_info["GOOD"]["CURRENCY"]),
            "%.2f" % good_info["GOOD"]["PRICE"],
            get_currency_lang_op(good_info["GOOD"]["CURRENCY"])
        )

        amount += float(sample_good.good.PRICE) * sample_good.NUM
        goods_list.append(good_info)

    total_amount = amount if len(goods_list) == 0 else "{}{} {}".format(
        get_currency_op(goods_list[0]["GOOD"]["CURRENCY"]),
        "%.2f" % amount,
        get_currency_lang_op(goods_list[0]["GOOD"]["CURRENCY"])
    )

    shipping_cost = shipping if len(goods_list) == 0 else "{}{} {}".format(
        get_currency_op(goods_list[0]["GOOD"]["CURRENCY"]),
        "%.2f" % shipping,
        get_currency_lang_op(goods_list[0]["GOOD"]["CURRENCY"])
    )

    trending_goods = Good.query.filter(
        Good.AREA_ID.like("%" + current_user.AREA_ID + "%")
    ).order_by(desc(Good.NUM)).all()
    trending_goods_list = list()
    for trending_good in trending_goods:
        trending_good_info = trending_good.to_json()
        trending_good_info["TYPE"] = trending_good_info["TYPE"].lower()
        trending_good_info["COLOR"] = get_color_op(
            trending_good_info["COLOR"]) if lang_type == 'zh_cn' else trending_good_info["COLOR"]
        trending_good_info[
            "CATEGORY"] = trending_good.category.NAME if lang_type == 'zh_cn' else trending_good.category.EN_NAME

        trending_goods_list.append(trending_good_info)

    return render_template("customer/sampleBag.html", lang=lang[lang_type],
                           lang_type=lang_type, route="sampleBag",
                           addition=set_addition(location="sampleBag"),
                           data={"goods": goods_list, "totalAmount": total_amount,
                                 "shippingCost": shipping_cost, "trendingGoods": trending_goods_list}
                           )
