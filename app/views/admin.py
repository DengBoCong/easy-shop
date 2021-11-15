from . import views
from flask import jsonify
from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user
from datetime import datetime
from ..models import *
from sqlalchemy import asc, desc, and_, or_
from ..utils.set import set_addition
from ..utils.get import *
from ..i18 import lang
from ..setting import *


@views.route('/<lang_type>/newProducts', methods=['GET', 'POST'])
@login_required
def new_single_product(lang_type):
    """ 添加产品"""
    lang_type, sub_page = lang_type.split("-")

    if lang_type not in ["zh_cn", "en_us"]:
        return render_template("404.html", lang_type=lang_type, route="newProducts")

    info_data = request.args.to_dict()
    product_type = info_data.get("productType", "")
    if product_type not in ["SAMPLE", "DESIGN", "REFERENCE"]:
        return render_template("404.html", lang_type=lang_type, route="newProducts")

    areas = Area.query.order_by(asc(Area.EN_NAME)).all()
    areas_list = []
    for area in areas:
        areas_list.append(area.to_json())

    good_categories = GoodCategory.query.order_by(asc(GoodCategory.EN_NAME)).all()
    good_categories_list = []
    for good_category in good_categories:
        good_categories_list.append(good_category.to_json())

    good_sizes = GoodSize.query.order_by(asc(GoodSize.SIZE)).all()
    good_sizes_list = []
    for good_size in good_sizes:
        good_sizes_list.append(good_size.to_json())

    return render_template("admin/newProducts.html", lang=lang[lang_type],
                           lang_type=lang_type, route="newProducts?productType={}".format(product_type),
                           addition=set_addition(add="-" + sub_page, location=sub_page),
                           data={"areas": areas_list, "goodCategories": good_categories_list,
                                 "goodSizes": good_sizes_list, "productType": product_type})


@views.route('/<lang_type>/editProducts', methods=['GET', 'POST'])
@login_required
def edit_single_product(lang_type):
    """ 编辑产品"""
    lang_type, sub_page = lang_type.split("-")
    info_data = request.args.to_dict()

    if lang_type not in ["zh_cn", "en_us"]:
        return render_template("404.html", lang_type=lang_type, route="editProducts")

    good = Good.query.get(info_data.get("goodId"))
    good_info = good.to_json()

    good_info["SIZE"] = [e for e in good_info["SIZE"].split(",")]

    good_info["IMG"] = [good_info["COVER"]]
    good_img = GoodImg.query.filter_by(GOOD_ID=good_info["ID"]).order_by(asc(GoodImg.CREATE_DATETIME)).all()
    for img in good_img:
        good_info["IMG"].append(img.URL)

    good_prices = GoodPrice.query.filter_by(GOOD_ID=good_info["ID"]).order_by(asc(GoodPrice.START_NUM)).all()
    good_info["PRICES"] = [{
        "START_NUM": price.START_NUM,
        "END_NUM": price.END_NUM,
        "PRICE": "%.2f" % price.PRICE
    } for price in good_prices]
    good_info["TYPE"] = good_info["TYPE"].lower()

    areas = Area.query.order_by(asc(Area.EN_NAME)).all()
    areas_list = []
    for area in areas:
        areas_list.append(area.to_json())

    good_categories = GoodCategory.query.order_by(asc(GoodCategory.EN_NAME)).all()
    good_categories_list = []
    for good_category in good_categories:
        good_categories_list.append(good_category.to_json())

    good_sizes = GoodSize.query.order_by(asc(GoodSize.SIZE)).all()
    good_sizes_list = []
    for good_size in good_sizes:
        good_sizes_list.append(good_size.to_json())

    return render_template("admin/editProducts.html", lang=lang[lang_type],
                           lang_type=lang_type, route="editProducts",
                           addition=set_addition(add="-" + sub_page, location=sub_page),
                           data={"areas": areas_list, "goodCategories": good_categories_list,
                                 "goodSizes": good_sizes_list, "goodInfo": good_info,
                                 "productType": good_info["CLASS"]})


@views.route('/<lang_type>/previewProducts', methods=['GET', 'POST'])
@login_required
def preview_products(lang_type):
    """ 预览产品"""
    info_data = request.args.to_dict()
    lang_type, sub_page = lang_type.split("-")

    if lang_type not in ["zh_cn", "en_us"]:
        return render_template("404.html", lang_type=lang_type, route="previewProducts")

    good = Good.query.get(info_data.get("goodId"))
    good_info = good.to_json()
    good_info["CATEGORY_ID"] = good.category.NAME if lang_type == "zh_cn" else good.category.EN_NAME

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

    return render_template("admin/previewProducts.html", lang=lang[lang_type], lang_type=lang_type,
                           route="previewProducts?goodId={}".format(good_info["ID"]),
                           goodInfo=good_info, addition=set_addition(add="-" + sub_page, location="previewProducts"),
                           data={"productType": good_info["CLASS"]})


@views.route('/<lang_type>/publishedProduct', methods=['GET', 'POST'])
@login_required
def published_product(lang_type):
    """ 已发布产品"""
    info_data = request.args.to_dict()
    user_id = info_data.get("userId", "")
    category = info_data.get("category", "")
    product = info_data.get("product", "")
    color = info_data.get("color", "")

    if lang_type not in ["zh_cn", "en_us"]:
        return render_template("404.html", lang_type=lang_type, route="publishedProduct")

    user = User.query.get(user_id)

    good_categories = GoodCategory.query.order_by(asc(GoodCategory.EN_NAME)).all()
    good_categories_dict = dict()
    good_categories_list = list()
    for good_category in good_categories:
        good_categories_list.append(good_category.to_json())
        good_categories_dict[good_category.EN_NAME] = good_category.ID

    goods = Good.query.filter(
        Good.USER_ID.like("%" + user_id + "%"),
        Good.CLASS.like("%" + "" if category == "all" else category + "%"),
        Good.IS_PUBLISHED.like("%1%"),
        Good.CATEGORY_ID.like("%" + good_categories_dict.get(product, "") + "%"),
        Good.COLOR.like("%" + "" if color == "all" else color + "%"),
    ).order_by(desc(Good.CREATE_DATETIME)).all()

    goods_list = list()
    for good in goods:
        good_info = good.to_json()

        if good.CLASS != "DESIGN":
            if good.CLASS == "SAMPLE":
                min_price, max_price = 10000000, 0
                for price in good.goodPrices:
                    min_price = price.PRICE if price.PRICE < min_price else min_price
                    max_price = price.PRICE if price.PRICE > max_price else max_price
                if min_price != max_price:
                    good_info["PRICE"] = "{}{} - {}".format(get_currency_op(good_info["CURRENCY"]), "%.2f" % min_price,
                                                            "%.2f" % max_price)
                else:
                    good_info["PRICE"] = "{}{}".format(get_currency_op(good_info["CURRENCY"]), "%.2f" % min_price)
            else:
                good_info["PRICE"] = "{}{}".format(get_currency_op(good_info["CURRENCY"]), "%.2f" % good_info["PRICE"])
        else:
            good_info["PRICE"] = ""

        good_info["COLOR"] = get_color_op(good_info["COLOR"]) if lang_type == 'zh_cn' else good_info["COLOR"]
        good_info["CATEGORY"] = good.category.NAME if lang_type == 'zh_cn' else good.category.EN_NAME
        goods_list.append(good_info)

    addition = set_addition(location="login", categories="publishedProduct")

    return render_template("admin/publishedProduct.html", lang=lang[lang_type],
                           lang_type=lang_type,
                           route="publishedProduct?userId={}&category={}".format(user_id, category),
                           addition=addition,
                           data={"user": user, "category": category, "product": product, "color": color,
                                 "categories": good_categories_list, "goods": goods_list,
                                 "add": "-" + info_data.get("category", "SAMPLE")})


##############################超管###############################

@views.route('/<lang_type>/addUser', methods=['GET', 'POST'])
@login_required
def add_user(lang_type):
    """ 添加账号"""
    lang_type, sub_page = lang_type.split("-")

    if lang_type not in ["zh_cn", "en_us"]:
        return render_template("404.html", lang_type=lang_type, route="addUser")

    if sub_page not in ["customer", "staff"]:
        return render_template("404.html", lang_type=lang_type, route="addUser")

    areas = Area.query.order_by(asc(Area.EN_NAME)).all()
    areas_list = []
    for area in areas:
        areas_list.append(area.to_json())

    return render_template("admin/manage/addUser.html", lang=lang[lang_type],
                           lang_type=lang_type, route="addUser",
                           addition=set_addition(location="addUser", add="-" + sub_page),
                           data={"areas": areas_list, "subPage": sub_page})


@views.route('/<lang_type>/editUser', methods=['GET', 'POST'])
@login_required
def edit_user(lang_type):
    """ 编辑账号"""
    info_data = request.args.to_dict()
    lang_type, sub_page = lang_type.split("-")

    if lang_type not in ["zh_cn", "en_us"]:
        return render_template("404.html", lang_type=lang_type, route="editUser")

    if sub_page not in ["customer", "staff"]:
        return render_template("404.html", lang_type=lang_type, route="editUser")

    user_id = info_data.get("userId", "")
    user = User.query.get(user_id)

    areas = Area.query.order_by(asc(Area.EN_NAME)).all()
    areas_list = []
    for area in areas:
        areas_list.append(area.to_json())

    return render_template("admin/manage/editUser.html", lang=lang[lang_type],
                           lang_type=lang_type, route="editUser?userId=" + user_id,
                           addition=set_addition(location="editUser", add="-" + sub_page),
                           data={"areas": areas_list, "subPage": sub_page, "user": user})


@views.route('/<lang_type>/manageStaffAccounts', methods=['GET', 'POST'])
@login_required
def manage_staff_accounts(lang_type):
    """ 管理员工账号"""
    info_data = request.args.to_dict()

    if current_user.ROLE == "USER":
        return render_template("error/accessDeny.html", lang=lang[lang_type])

    if lang_type not in ["zh_cn", "en_us"]:
        return render_template("404.html", lang_type=lang_type, route="manageStaffAccounts")

    if info_data.get("sort", "") == "az":
        if current_user.ROLE == 'SUPER':
            if info_data.get("position", "") == "" or info_data.get("position", "") == "all":
                users = User.query.filter(or_(User.ROLE == "AGENT", User.ROLE == "ADMIN")).order_by(
                    asc(User.ORDERS)).all()
            else:
                users = User.query.filter_by(
                    ROLE="AGENT" if info_data.get("position", "") == "junior" else "ADMIN").order_by(
                    asc(User.ORDERS)).all()
        elif current_user.ROLE == 'ADMIN':
            users = User.query.filter_by(ROLE="AGENT").order_by(asc(User.ORDERS)).all()
    else:
        if current_user.ROLE == 'SUPER':
            if info_data.get("position", "") == "" or info_data.get("position", "") == "all":
                users = User.query.filter(or_(User.ROLE == "AGENT", User.ROLE == "ADMIN")).order_by(
                    desc(User.ORDERS)).all()
            else:
                users = User.query.filter_by(
                    ROLE="AGENT" if info_data.get("position", "") == "junior" else "ADMIN").order_by(
                    asc(User.ORDERS)).all()
        elif current_user.ROLE == 'ADMIN':
            users = User.query.filter_by(ROLE="AGENT").order_by(desc(User.ORDERS)).all()

    addition = set_addition(location="manageStaffAccounts", categories="manageStaffAccounts")

    return render_template("admin/manage/manageStaffAccounts.html", lang=lang[lang_type],
                           lang_type=lang_type, route="manageStaffAccounts",
                           addition=addition, data={"users": users, "position": info_data.get("position", ""),
                                                    "sort": info_data.get("sort", "")})


@views.route('/<lang_type>/manageCustomerAccounts', methods=['GET', 'POST'])
@login_required
def manage_customer_accounts(lang_type):
    """ 管理客户账号"""
    info_data = request.args.to_dict()

    if current_user.ROLE == "USER":
        return render_template("error/accessDeny.html", lang=lang[lang_type])

    if lang_type not in ["zh_cn", "en_us"]:
        return render_template("404.html", lang_type=lang_type, route="manageCustomerAccounts")

    areas = Area.query.order_by(asc(Area.EN_NAME)).all()
    areas_list = []
    area_dict = {"public": "public"}
    for area in areas:
        area_dict[area.EN_NAME] = area.ID
        areas_list.append(area.to_json())

    if info_data.get("sort", "") == "less_more":
        if info_data.get("area", "") == "" or info_data.get("area", "") == "all":
            users = User.query.filter_by(ROLE="USER").order_by(asc(User.ORDERS)).all()
        else:
            users = User.query.filter(
                and_(User.ROLE == "USER", User.AREA_ID == area_dict.get(info_data["area"], ""))).order_by(
                asc(User.ORDERS)).all()
    else:
        if info_data.get("area", "") == "" or info_data.get("area", "") == "all":
            users = User.query.filter_by(ROLE="USER").order_by(desc(User.ORDERS)).all()
        else:
            users = User.query.filter(
                and_(User.ROLE == "USER", User.AREA_ID == area_dict.get(info_data["area"], ""))).order_by(
                desc(User.ORDERS)).all()

    addition = set_addition(location="manageCustomerAccounts", categories="manageCustomerAccounts")

    return render_template("admin/manage/manageCustomerAccounts.html", lang=lang[lang_type],
                           lang_type=lang_type, route="manageCustomerAccounts",
                           addition=addition, data={"areas": areas_list, "sort": info_data.get("sort", ""),
                                                    "area": info_data.get("area", ""), "users": users})


##############################订单###############################

@views.route('/<lang_type>/orderHistory', methods=['GET', 'POST'])
@login_required
def orde_history(lang_type):
    """ 历史订单"""
    info_data = request.args.to_dict()
    user_id = info_data.get("userId", "")
    sort = info_data.get("sort", "")

    if lang_type not in ["zh_cn", "en_us"]:
        return render_template("404.html", lang_type=lang_type, route="orderHistory")

    user = User.query.get(user_id)
    order_list = list()
    if sort == "less_more":
        orders = Order.query.filter_by(USER_ID=user_id, CLASS="NORMAL").order_by(asc(Order.TOTAL_AMOUNT)).all()
    else:
        orders = Order.query.filter_by(USER_ID=user_id, CLASS="NORMAL").order_by(desc(Order.TOTAL_AMOUNT)).all()

    for order in orders:
        order_info = order.to_json()
        order_info["ORDER_GOOD"] = list()
        order_info["CREATE_DATETIME"] = order.CREATE_DATETIME.strftime('%Y-%m-%d')
        currency = ""
        for order_good in order.orderGoods:
            order_good_info = order_good.to_json()
            color = get_color_op(order_good.good.COLOR) if lang_type == 'zh_cn' else order_good.good.COLOR
            cate = order_good.good.category.NAME if lang_type == 'zh_cn' else order_good.good.category.EN_NAME
            order_good_info["TITLE"] = "{} {} {}".format(order_good.good.BRAND, color, cate)
            order_good_info["PRICE"] = "{}{}".format(
                get_currency_op(order_good.good.CURRENCY), "%.2f" % order_good_info["PRICE"])
            currency = get_currency_op(order_good.good.CURRENCY)
            order_good_info["COVER"] = order_good.good.COVER

            order_info["ORDER_GOOD"].append(order_good_info)

        order_info["TOTAL_AMOUNT"] = "{}{}".format(currency, "%.2f" % order.TOTAL_AMOUNT)
        order_list.append(order_info)

    return render_template("admin/manage/orderHistory.html", lang=lang[lang_type],
                           lang_type=lang_type, route="orderHistory?userId={}&sort={}".format(user_id, sort),
                           addition=set_addition(location="orderHistory", categories="orderHistory"),
                           data={"userId": user_id, "user": user, "orders": order_list, "sort": sort})


##############################shoppingbag###############################

@views.route('/<lang_type>/adminShoppingBag', methods=['GET', 'POST'])
@login_required
def admin_shopping_bag(lang_type):
    """ 员工的shoppingbag"""
    info_data = request.args.to_dict()

    if current_user.ROLE == "USER":
        return render_template("error/accessDeny.html", lang=lang[lang_type])

    if lang_type not in ["zh_cn", "en_us"]:
        return render_template("404.html", lang_type=lang_type, route="adminShoppingBag")

    areas = Area.query.order_by(asc(Area.EN_NAME)).all()
    areas_list = []
    area_dict = {"public": "public"}
    for area in areas:
        area_dict[area.EN_NAME] = area.ID
        areas_list.append(area.to_json())

    if info_data.get("sort", "") == "less_more":
        users = User.query.filter(
            User.AREA_ID.like("%" + "" if info_data.get("area", "") == "all" else info_data.get("area", "") + "%"),
            User.ROLE.like("%USER%"),
            User.NAME.like("%" + info_data.get("name", "") + "%")
        ).order_by(asc(User.ORDERS)).all()
    else:
        users = User.query.filter(
            User.AREA_ID.like("%" + "" if info_data.get("area", "") == "all" else info_data.get("area", "") + "%"),
            User.ROLE.like("%USER%"),
            User.NAME.like("%" + info_data.get("name", "") + "%")
        ).order_by(desc(User.ORDERS)).all()

    addition = set_addition(location="shoppingBag", categories="shoppingBag")

    return render_template("admin/shoppingBag.html", lang=lang[lang_type],
                           lang_type=lang_type, route="adminShoppingBag",
                           addition=addition, data={"areas": areas_list, "sort": info_data.get("sort", ""),
                                                    "area": info_data.get("area", ""), "users": users})


@views.route('/<lang_type>/adminSampleBag', methods=['GET', 'POST'])
@login_required
def admin_sample_bag(lang_type):
    """ 员工的SampleBag"""
    info_data = request.args.to_dict()

    if current_user.ROLE == "USER":
        return render_template("error/accessDeny.html", lang=lang[lang_type])

    if lang_type not in ["zh_cn", "en_us"]:
        return render_template("404.html", lang_type=lang_type, route="adminSampleBag")

    areas = Area.query.order_by(asc(Area.EN_NAME)).all()
    areas_list = []
    area_dict = {"public": "public"}
    for area in areas:
        area_dict[area.EN_NAME] = area.ID
        areas_list.append(area.to_json())

    if info_data.get("sort", "") == "less_more":
        users = User.query.filter(
            User.AREA_ID.like("%" + "" if info_data.get("area", "") == "all" else info_data.get("area", "") + "%"),
            User.ROLE.like("%USER%"),
            User.NAME.like("%" + info_data.get("name", "") + "%")
        ).order_by(asc(User.ORDERS)).all()
    else:
        users = User.query.filter(
            User.AREA_ID.like("%" + "" if info_data.get("area", "") == "all" else info_data.get("area", "") + "%"),
            User.ROLE.like("%USER%"),
            User.NAME.like("%" + info_data.get("name", "") + "%")
        ).order_by(desc(User.ORDERS)).all()

    addition = set_addition(location="sampleBag", categories="sampleBag")

    return render_template("admin/sampleBag.html", lang=lang[lang_type],
                           lang_type=lang_type, route="adminSampleBag",
                           addition=addition, data={"areas": areas_list, "sort": info_data.get("sort", ""),
                                                    "area": info_data.get("area", ""), "users": users})


@views.route('/<lang_type>/bagProductMode', methods=['GET', 'POST'])
def bag_product_mode(lang_type):
    """ 产品模式"""
    info_data = request.args.to_dict()

    product = info_data.get("products", "")
    color = info_data.get("colors", "")
    sort = info_data.get("sort", "")

    addition = set_addition(categories="shoppingBag", page=info_data.get("page", 1),
                            products=product, sort=sort, colors=color, location="shoppingBag")

    good_categories = GoodCategory.query.order_by(asc(GoodCategory.EN_NAME)).all()
    good_categories_list = list()
    for good_category in good_categories:
        good_categories_list.append(good_category.to_json())

    area_id = "public"
    if hasattr(current_user, "ROLE"):
        area_id = current_user.AREA_ID if current_user.ROLE == "USER" else ""

    if sort == "latest" or sort == "":
        goods = Good.query.filter(
            Good.BRAND.like("%" + info_data.get("brand", "") + "%"),
            Good.AREA_ID.like("%" + area_id + "%"),
            Good.CATEGORY.like("%" + product + "%"),
            Good.COLOR.like("%" + color + "%")
        ).order_by(desc(Good.CREATE_DATETIME)).all()
    elif sort == "trending":
        goods = Good.query.filter(
            Good.BRAND.like("%" + info_data.get("brand", "") + "%"),
            Good.AREA_ID.like("%" + area_id + "%"),
            Good.CATEGORY.like("%" + product + "%"),
            Good.COLOR.like("%" + color + "%")
        ).order_by(desc(Good.NUM)).all()
    elif sort == "lowHigh":
        goods = Good.query.filter(
            Good.BRAND.like("%" + info_data.get("brand", "") + "%"),
            Good.AREA_ID.like("%" + area_id + "%"),
            Good.CATEGORY.like("%" + product + "%"),
            Good.COLOR.like("%" + color + "%")
        ).order_by(asc(Good.PRICE)).all()
    else:
        goods = Good.query.filter(
            Good.BRAND.like("%" + info_data.get("brand", "") + "%"),
            Good.AREA_ID.like("%" + area_id + "%"),
            Good.CATEGORY.like("%" + product + "%"),
            Good.COLOR.like("%" + color + "%")
        ).order_by(desc(Good.PRICE)).all()

    if lang_type not in ["zh_cn", "en_us"]:
        return render_template("404.html", lang_type=lang_type, route="bagProductMode")

    goods_list = list()
    for good in goods:
        good_info = good.to_json()
        if good.CLASS != "DESIGN":
            if good.CLASS == "SAMPLE":
                min_price, max_price = 10000000, 0
                for price in good.goodPrices:
                    min_price = price.PRICE if price.PRICE < min_price else min_price
                    max_price = price.PRICE if price.PRICE > max_price else max_price
                if min_price != max_price:
                    good_info["PRICE"] = "{}{} - {}".format(get_currency_op(good_info["CURRENCY"]), "%.2f" % min_price,
                                                            "%.2f" % max_price)
                else:
                    good_info["PRICE"] = "{}{}".format(get_currency_op(good_info["CURRENCY"]), "%.2f" % min_price)
            else:
                good_info["PRICE"] = "{}{}".format(get_currency_op(good_info["CURRENCY"]), "%.2f" % good_info["PRICE"])
        else:
            good_info["PRICE"] = ""

        good_info["COLOR"] = get_color_op(good_info["COLOR"]) if lang_type == 'zh_cn' else good_info["COLOR"]
        good_info["CATEGORY"] = good.category.NAME if lang_type == 'zh_cn' else good.category.EN_NAME
        goods_list.append(good_info)

    return render_template("admin/bagProductMode.html", lang=lang[lang_type], lang_type=lang_type,
                           route="bagProductMode", addition=addition,
                           data={"goods": goods_list, "categories": good_categories_list})

@views.route('/<lang_type>/allProducts', methods=['GET', 'POST'])
def all_products(lang_type):
    """ 搜索所有产品页"""
    info_data = request.args.to_dict()

    product_class = info_data.get("class", "")
    name = info_data.get("name", "")
    product = info_data.get("products", "")
    color = info_data.get("colors", "")
    sort = info_data.get("sort", "")

    addition = set_addition(categories="search", page=info_data.get("page", 1),
                            products=product, sort=sort, colors=color, location="search")

    good_categories = GoodCategory.query.order_by(asc(GoodCategory.EN_NAME)).all()
    good_categories_list = list()
    for good_category in good_categories:
        good_categories_list.append(good_category.to_json())

    area_id = "public"
    if hasattr(current_user, "ROLE"):
        area_id = current_user.AREA_ID if current_user.ROLE == "USER" else ""

    if sort == "latest" or sort == "":
        goods = Good.query.filter(
            Good.BRAND.like("%" + name + "%"),
            Good.AREA_ID.like("%" + area_id + "%"),
            Good.TYPE.like("%" + '' if product_class == 'all' else product_class + "%"),
            Good.CATEGORY.like("%" + product + "%"),
            Good.COLOR.like("%" + color + "%"),
        ).order_by(desc(Good.CREATE_DATETIME)).all()
    elif sort == "trending":
        goods = Good.query.filter(
            Good.BRAND.like("%" + name + "%"),
            Good.AREA_ID.like("%" + area_id + "%"),
            Good.TYPE.like("%" + '' if product_class == 'all' else product_class + "%"),
            Good.CATEGORY.like("%" + product + "%"),
            Good.COLOR.like("%" + color + "%")
        ).order_by(desc(Good.NUM)).all()
    elif sort == "lowHigh":
        goods = Good.query.filter(
            Good.BRAND.like("%" + name + "%"),
            Good.AREA_ID.like("%" + area_id + "%"),
            Good.TYPE.like("%" + '' if product_class == 'all' else product_class + "%"),
            Good.CATEGORY.like("%" + product + "%"),
            Good.COLOR.like("%" + color + "%")
        ).order_by(asc(Good.PRICE)).all()
    else:
        goods = Good.query.filter(
            Good.BRAND.like("%" + name + "%"),
            Good.AREA_ID.like("%" + area_id + "%"),
            Good.TYPE.like("%" + '' if product_class == 'all' else product_class + "%"),
            Good.CATEGORY.like("%" + product + "%"),
            Good.COLOR.like("%" + color + "%")
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
        if good.CLASS != "DESIGN":
            if good.CLASS == "SAMPLE":
                min_price, max_price = 10000000, 0
                for price in good.goodPrices:
                    min_price = price.PRICE if price.PRICE < min_price else min_price
                    max_price = price.PRICE if price.PRICE > max_price else max_price
                if min_price != max_price:
                    good_info["PRICE"] = "{}{} - {}".format(get_currency_op(good_info["CURRENCY"]), "%.2f" % min_price,
                                                            "%.2f" % max_price)
                else:
                    good_info["PRICE"] = "{}{}".format(get_currency_op(good_info["CURRENCY"]), "%.2f" % min_price)
            else:
                good_info["PRICE"] = "{}{}".format(get_currency_op(good_info["CURRENCY"]), "%.2f" % good_info["PRICE"])
        else:
            good_info["PRICE"] = ""

        good_info["COLOR"] = get_color_op(good_info["COLOR"]) if lang_type == 'zh_cn' else good_info["COLOR"]
        good_info["CATEGORY"] = good.category.NAME if lang_type == 'zh_cn' else good.category.EN_NAME
        goods_list.append(good_info)

    return render_template("admin/allProducts.html", lang=lang[lang_type], lang_type=lang_type, route="allProducts",
                           addition=addition, data={"goods": goods_list, "categories": good_categories_list,
                                                    "class": product_class, "name": name,
                                                    "pageCount": page_count})
