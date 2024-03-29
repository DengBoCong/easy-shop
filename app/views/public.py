import re
import json
from . import views
from flask import jsonify
from flask import render_template, request, redirect, url_for
from flask_login import login_required, logout_user, current_user
from sqlalchemy import asc, desc, and_, or_
from datetime import datetime
from ..i18 import lang
from ..utils import set_addition
from ..models import *
from ..utils.get import *
from ..setting import PAGE_LIMIT


@views.route('/accessDeny', methods=['GET', 'POST'])
def access_deny():
    """ 无权限"""
    return render_template("error/accessDeny.html")


@views.route('/notLogin', methods=['GET', 'POST'])
def not_login():
    """ 登陆失效或未登录"""
    return render_template("error/notLogin.html")


@views.route('/<lang_type>/login', methods=['GET', 'POST'])
def login(lang_type):
    """ 登入页"""
    if lang_type not in ["zh_cn", "en_us"]:
        return render_template("404.html", lang_type=lang_type, route="login")
    return render_template("login.html", lang=lang[lang_type],
                           lang_type=lang_type, route="login", addition=set_addition(location="login"))


@views.route('/<lang_type>/logout', methods=['GET', 'POST'])
def do_logout(lang_type):
    logout_user()
    if lang_type not in ["zh_cn", "en_us"]:
        return render_template("404.html", lang_type=lang_type, route="login")
    return render_template("login.html", lang=lang[lang_type],
                           lang_type=lang_type, route="login", addition=set_addition(location="login"))


@views.route('/<lang_type>/index', methods=['GET', 'POST'])
def index(lang_type):
    """ 首页"""
    if lang_type not in ["zh_cn", "en_us"]:
        return render_template("404.html", lang_type=lang_type, route="index")

    system = System.query.get("0")

    return render_template("index.html", lang=lang[lang_type],
                           lang_type=lang_type, route="index", systemInfo=system,
                           addition=set_addition(), rand=str(random.randint(0, 10000)))


@views.route('/<lang_type>/', methods=['GET', 'POST'])
def index_d(lang_type):
    """ 首页"""
    if lang_type not in ["zh_cn", "en_us"]:
        return render_template("404.html", lang_type=lang_type, route="index")
    return redirect(url_for('views.index', lang_type=lang_type))


@views.route('/', methods=['GET', 'POST'])
def index_g():
    """ 首页"""
    return redirect(url_for('views.index', lang_type="zh_cn"))


@views.route('/<lang_type>/aboutUs', methods=['GET', 'POST'])
def about_us(lang_type):
    """ 关于我们页"""
    if lang_type not in ["zh_cn", "en_us"]:
        return render_template("404.html", lang=lang[lang_type], lang_type=lang_type, route="aboutUs")

    system = System.query.get("0")
    img_list = []
    if system:
        img_list = system.ABOUT_US.split(",")
    if len(img_list) == 1 and img_list[0] == "":
        img_list = []

    return render_template("public/aboutUs.html", lang=lang[lang_type],
                           lang_type=lang_type, route="aboutUs", imgs=img_list,
                           addition=set_addition(location="aboutUs"), rand=str(random.randint(0, 10000)))


@views.route('/<lang_type>/contactUs', methods=['GET', 'POST'])
def contact_us(lang_type):
    """ 联系我们页"""
    if lang_type not in ["zh_cn", "en_us"]:
        return render_template("404.html", lang=lang[lang_type], lang_type=lang_type, route="contactUs")

    system = System.query.get("0")
    img_list = []
    if system:
        img_list = system.CONTACT_US.split(",")
    if len(img_list) == 1 and img_list[0] == "":
        img_list = []

    return render_template("public/contactUs.html", lang=lang[lang_type],
                           lang_type=lang_type, route="contactUs", imgs=img_list,
                           addition=set_addition(location="contactUs"), rand=str(random.randint(0, 10000)))


@views.route('/<lang_type>/commonSample', methods=['GET', 'POST'])
def sample(lang_type):
    """ 样品页"""
    info_data = request.args.to_dict()
    lang_type, sub_page = lang_type.split("-")

    product = info_data.get("products", "")
    color = info_data.get("colors", "")
    sort = info_data.get("sort", "")

    addition = set_addition(add="-" + sub_page, categories="sample", page=info_data.get("page", 1),
                            products=product, sort=sort, colors=color, location=sub_page)

    good_categories = GoodCategory.query.order_by(asc(GoodCategory.EN_NAME)).all()
    good_categories_list = list()
    for good_category in good_categories:
        good_categories_list.append(good_category.to_json())

    area_id = "public"
    if hasattr(current_user, "ROLE"):
        area_id = current_user.AREA_ID if current_user.ROLE == "USER" else ""

    if sort == "latest" or sort == "":
        goods = Good.query.filter(
            Good.AREA_ID.like("%" + area_id + "%"),
            Good.CLASS.like("%SAMPLE%"),
            Good.CATEGORY.like("%" + product + "%"),
            Good.COLOR.like("%" + color + "%"),
            Good.TYPE == sub_page
        ).order_by(desc(Good.CREATE_DATETIME)).all()
    elif sort == "trending":
        goods = Good.query.filter(
            Good.AREA_ID.like("%" + area_id + "%"),
            Good.CLASS.like("%SAMPLE%"),
            Good.CATEGORY.like("%" + product + "%"),
            Good.COLOR.like("%" + color + "%"),
            Good.TYPE == sub_page
        ).order_by(desc(Good.NUM)).all()
    elif sort == "lowHigh":
        goods = Good.query.filter(
            Good.AREA_ID.like("%" + area_id + "%"),
            Good.CLASS.like("%SAMPLE%"),
            Good.CATEGORY.like("%" + product + "%"),
            Good.COLOR.like("%" + color + "%"),
            Good.TYPE == sub_page
        ).order_by(asc(Good.PRICE)).all()
    else:
        goods = Good.query.filter(
            Good.AREA_ID.like("%" + area_id + "%"),
            Good.CLASS.like("%SAMPLE%"),
            Good.CATEGORY.like("%" + product + "%"),
            Good.COLOR.like("%" + color + "%"),
            Good.TYPE == sub_page
        ).order_by(desc(Good.PRICE)).all()

    if lang_type not in ["zh_cn", "en_us"]:
        return render_template("404.html", lang_type=lang_type, route="commonSample")

    goods_list = list()
    page_count, page = len(goods), int(info_data.get("page", 1)) - 1
    for good_index, good in enumerate(goods):
        if not (page * PAGE_LIMIT <= good_index < (page + 1) * PAGE_LIMIT):
            continue
        elif good_index >= (page + 1) * PAGE_LIMIT:
            break

        good_info = good.to_json()
        min_price, max_price = 10000000, 0
        for price in good.goodPrices:
            min_price = price.PRICE if price.PRICE < min_price else min_price
            max_price = price.PRICE if price.PRICE > max_price else max_price
        if min_price != max_price:
            good_info["PRICE"] = "{}{} - {}".format(get_currency_op(good_info["CURRENCY"]), "%.2f" % min_price,
                                                    "%.2f" % max_price)
        else:
            good_info["PRICE"] = "{}{}".format(get_currency_op(good_info["CURRENCY"]), "%.2f" % min_price)
        good_info["COLOR"] = get_color_op(good_info["COLOR"]) if lang_type == 'zh_cn' else good_info["COLOR"]
        good_info["CATEGORY"] = good.category.NAME if lang_type == 'zh_cn' else good.category.EN_NAME
        goods_list.append(good_info)

    colors = Color.query.order_by(asc(Color.EN_NAME)).all()
    colors_list = []
    for color in colors:
        colors_list.append(color.to_json())

    return render_template("public/sample.html", lang=lang[lang_type], lang_type=lang_type, route="commonSample",
                           addition=addition, data={"goods": goods_list, "categories": good_categories_list,
                                                    "pageCount": page_count, "colors": colors_list})


@views.route('/<lang_type>/designDiagrams', methods=['GET', 'POST'])
def design_diagrams(lang_type):
    """ 设计图页"""
    info_data = request.args.to_dict()
    lang_type, sub_page = lang_type.split("-")

    product = info_data.get("products", "")
    color = info_data.get("colors", "")
    sort = info_data.get("sort", "")

    addition = set_addition(add="-" + sub_page, categories="design", page=info_data.get("page", 1),
                            products=product, sort=sort, colors=color, location=sub_page)

    good_categories = GoodCategory.query.order_by(asc(GoodCategory.EN_NAME)).all()
    good_categories_list = list()
    for good_category in good_categories:
        good_categories_list.append(good_category.to_json())

    area_id = "public"
    if hasattr(current_user, "ROLE"):
        area_id = current_user.AREA_ID if current_user.ROLE == "USER" else ""

    if sort == "latest" or sort == "":
        goods = Good.query.filter(
            Good.AREA_ID.like("%" + area_id + "%"),
            Good.CLASS.like("%DESIGN%"),
            Good.CATEGORY.like("%" + product + "%"),
            Good.COLOR.like("%" + color + "%"),
            Good.TYPE == sub_page
        ).order_by(desc(Good.CREATE_DATETIME)).all()
    elif sort == "trending":
        goods = Good.query.filter(
            Good.AREA_ID.like("%" + area_id + "%"),
            Good.CLASS.like("%DESIGN%"),
            Good.CATEGORY.like("%" + product + "%"),
            Good.COLOR.like("%" + color + "%"),
            Good.TYPE == sub_page
        ).order_by(desc(Good.NUM)).all()
    elif sort == "lowHigh":
        goods = Good.query.filter(
            Good.AREA_ID.like("%" + area_id + "%"),
            Good.CLASS.like("%DESIGN%"),
            Good.CATEGORY.like("%" + product + "%"),
            Good.COLOR.like("%" + color + "%"),
            Good.TYPE == sub_page
        ).order_by(asc(Good.PRICE)).all()
    else:
        goods = Good.query.filter(
            Good.AREA_ID.like("%" + area_id + "%"),
            Good.CLASS.like("%DESIGN%"),
            Good.CATEGORY.like("%" + product + "%"),
            Good.COLOR.like("%" + color + "%"),
            Good.TYPE == sub_page
        ).order_by(desc(Good.PRICE)).all()

    if lang_type not in ["zh_cn", "en_us"]:
        return render_template("404.html", lang_type=lang_type, route="designDiagrams")

    goods_list = list()
    page_count, page = len(goods), int(info_data.get("page", 1)) - 1
    for good_index, good in enumerate(goods):
        if not (page * PAGE_LIMIT <= good_index < (page + 1) * PAGE_LIMIT):
            continue
        elif good_index >= (page + 1) * PAGE_LIMIT:
            break

        good_info = good.to_json()
        min_price, max_price = 10000000, 0
        for price in good.goodPrices:
            min_price = price.PRICE if price.PRICE < min_price else min_price
            max_price = price.PRICE if price.PRICE > max_price else max_price
        if min_price != max_price:
            good_info["PRICE"] = "{}{} - {}".format(get_currency_op(good_info["CURRENCY"]), "%.2f" % min_price,
                                                    "%.2f" % max_price)
        else:
            good_info["PRICE"] = "{}{}".format(get_currency_op(good_info["CURRENCY"]), "%.2f" % min_price)
        good_info["COLOR"] = get_color_op(good_info["COLOR"]) if lang_type == 'zh_cn' else good_info["COLOR"]
        good_info["CATEGORY"] = good.category.NAME if lang_type == 'zh_cn' else good.category.EN_NAME
        goods_list.append(good_info)

    colors = Color.query.order_by(asc(Color.EN_NAME)).all()
    colors_list = []
    for color in colors:
        colors_list.append(color.to_json())

    return render_template("public/designDiagrams.html", lang=lang[lang_type], lang_type=lang_type,
                           route="designDiagrams", addition=addition,
                           data={"goods": goods_list, "categories": good_categories_list,
                                 "pageCount": page_count, "colors": colors_list})


@views.route('/<lang_type>/referenceDiagrams', methods=['GET', 'POST'])
def reference_diagrams(lang_type):
    """ 参考图页"""
    info_data = request.args.to_dict()
    lang_type, sub_page = lang_type.split("-")

    product = info_data.get("products", "")
    color = info_data.get("colors", "")
    sort = info_data.get("sort", "")

    addition = set_addition(add="-" + sub_page, categories="reference", page=info_data.get("page", 1),
                            products=product, sort=sort, colors=color, location=sub_page)

    good_categories = GoodCategory.query.order_by(asc(GoodCategory.EN_NAME)).all()
    good_categories_list = list()
    for good_category in good_categories:
        good_categories_list.append(good_category.to_json())

    area_id = "public"
    if hasattr(current_user, "ROLE"):
        area_id = current_user.AREA_ID if current_user.ROLE == "USER" else ""

    if sort == "latest" or sort == "":
        goods = Good.query.filter(
            Good.AREA_ID.like("%" + area_id + "%"),
            Good.CLASS.like("%REFERENCE%"),
            Good.CATEGORY.like("%" + product + "%"),
            Good.COLOR.like("%" + color + "%"),
            Good.TYPE == sub_page
        ).order_by(desc(Good.CREATE_DATETIME)).all()
    elif sort == "trending":
        goods = Good.query.filter(
            Good.AREA_ID.like("%" + area_id + "%"),
            Good.CLASS.like("%REFERENCE%"),
            Good.CATEGORY.like("%" + product + "%"),
            Good.COLOR.like("%" + color + "%"),
            Good.TYPE == sub_page
        ).order_by(desc(Good.NUM)).all()
    elif sort == "lowHigh":
        goods = Good.query.filter(
            Good.AREA_ID.like("%" + area_id + "%"),
            Good.CLASS.like("%REFERENCE%"),
            Good.CATEGORY.like("%" + product + "%"),
            Good.COLOR.like("%" + color + "%"),
            Good.TYPE == sub_page
        ).order_by(asc(Good.PRICE)).all()
    else:
        goods = Good.query.filter(
            Good.AREA_ID.like("%" + area_id + "%"),
            Good.CLASS.like("%REFERENCE%"),
            Good.CATEGORY.like("%" + product + "%"),
            Good.COLOR.like("%" + color + "%"),
            Good.TYPE == sub_page
        ).order_by(desc(Good.PRICE)).all()

    if lang_type not in ["zh_cn", "en_us"]:
        return render_template("404.html", lang_type=lang_type, route="referenceDiagrams")

    goods_list = list()
    page_count, page = len(goods), int(info_data.get("page", 1)) - 1
    for good_index, good in enumerate(goods):
        if not (page * PAGE_LIMIT <= good_index < (page + 1) * PAGE_LIMIT):
            continue
        elif good_index >= (page + 1) * PAGE_LIMIT:
            break

        good_info = good.to_json()
        good_info["PRICE"] = "{}{}".format(get_currency_op(good_info["CURRENCY"]), "%.2f" % good_info["PRICE"])
        good_info["COLOR"] = get_color_op(good_info["COLOR"]) if lang_type == 'zh_cn' else good_info["COLOR"]
        good_info["CATEGORY"] = good.category.NAME if lang_type == 'zh_cn' else good.category.EN_NAME
        goods_list.append(good_info)

    colors = Color.query.order_by(asc(Color.EN_NAME)).all()
    colors_list = []
    for color in colors:
        colors_list.append(color.to_json())

    return render_template("public/referenceDiagrams.html", lang=lang[lang_type], lang_type=lang_type,
                           route="referenceDiagrams", addition=addition,
                           data={"goods": goods_list, "categories": good_categories_list,
                                 "pageCount": page_count, "colors": colors_list})


@views.route('/<lang_type>/singleProduct', methods=['GET', 'POST'])
def single_products(lang_type):
    """ 商品详情"""
    info_data = request.args.to_dict()
    lang_type, sub_page = lang_type.split("-")

    if lang_type not in ["zh_cn", "en_us"]:
        return render_template("404.html", lang_type=lang_type, route="singleProduct")

    good = Good.query.get(info_data.get("goodId"))
    good_info = good.to_json()
    good_info["COLOR"] = get_color_op(good_info["COLOR"]) if lang_type == 'zh_cn' else good_info["COLOR"]
    good_info["CATEGORY_ID"] = good.category.NAME if lang_type == "zh_cn" else good.category.EN_NAME
    good_info["CREATE_DATETIME"] = good.CREATE_DATETIME.strftime('%Y-%m-%d')
    good_info["PRICE"] = get_currency_op(good_info["CURRENCY"]) + str(good_info["PRICE"])

    good_info["SIZE"] = [e for e in good_info["SIZE"].split(",")]
    good_info["SIZE"].sort()

    good_info["IMG"] = [good_info["COVER"]]
    good_img = GoodImg.query.filter_by(GOOD_ID=good_info["ID"]).order_by(asc(GoodImg.CREATE_DATETIME)).all()
    for img in good_img:
        good_info["IMG"].append(img.URL)

    good_prices = GoodPrice.query.filter_by(GOOD_ID=good_info["ID"]).order_by(asc(GoodPrice.START_NUM)).all()
    good_info["PRICES"] = [{
        "RANGE": "{}-{}".format(price.START_NUM, price.END_NUM),
        "PRICE": "%.2f" % price.PRICE + get_currency_op(good_info["CURRENCY"])
    } for price in good_prices]
    # good_info["PRICES"].append({
    #     "RANGE": "{}<".format(good_prices[-1].START_NUM),
    #     "PRICE": "%.2f" % good_prices[-1].PRICE + get_currency_op(good_info["CURRENCY"])
    # })

    related_goods_list, buy_list, shopping_bag_list, wishlist = list(), dict(), list(), list()
    if hasattr(current_user, "ID") and (
            current_user.ROLE == 'AGENT' or current_user.ROLE == 'ADMIN' or current_user.ROLE == 'SUPER'):
        for order_good in good.orderGoods:
            buy_list[order_good.order.user.ID] = order_good.order.user.NAME
        shopping_bag_list = good.shoppingGoods
        wishlist = good.wishGoods
    else:
        related_goods = Good.query.filter(
            Good.AREA_ID.like("%" + good.AREA_ID + "%"),
            Good.CLASS.like("%" + good.CLASS + "%"),
            Good.CATEGORY_ID.like("%" + good.CATEGORY_ID + "%"),
            Good.TYPE.like("%" + sub_page + "%")
        ).order_by(desc(Good.NUM)).all()

        count = 0
        for related_good in related_goods:
            related_good_info = related_good.to_json()
            if related_good.ID == good_info["ID"]:
                continue
            min_price, max_price = 10000000, 0
            for price in related_good.goodPrices:
                min_price = price.PRICE if price.PRICE < min_price else min_price
                max_price = price.PRICE if price.PRICE > max_price else max_price
            if min_price != max_price:
                related_good_info["PRICE"] = "{}{} - {}".format(
                    get_currency_op(related_good_info["CURRENCY"]), "%.2f" % min_price, "%.2f" % max_price)
            else:
                related_good_info["PRICE"] = "{}{}".format(
                    get_currency_op(related_good_info["CURRENCY"]), "%.2f" % min_price)
            related_good_info["COLOR"] = get_color_op(
                related_good_info["COLOR"]) if lang_type == 'zh_cn' else related_good_info["COLOR"]
            related_good_info[
                "CATEGORY"] = related_good.category.NAME if lang_type == 'zh_cn' else related_good.category.EN_NAME
            related_goods_list.append(related_good_info)
            count += 1
            if count == 6:
                break

    return render_template("public/singleProduct.html", lang=lang[lang_type], lang_type=lang_type,
                           route="singleProduct?goodId={}".format(good_info["ID"]),
                           goodInfo=good_info, addition=set_addition(add="-" + sub_page, location=sub_page),
                           data={"productType": good_info["CLASS"], "related_goods": related_goods_list,
                                 "buy_list": buy_list, "shopping_bag_list": shopping_bag_list,
                                 "wishlist": wishlist})
