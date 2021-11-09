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

    if (product == "" or product == "all") and (color == "" or color == "all"):
        goods = Good.query.filter(and_(Good.USER_ID == user_id,
                                       Good.CLASS == category,
                                       Good.IS_PUBLISHED == 1)).order_by(desc(Good.CREATE_DATETIME)).all()
    elif product != "" and product != "all" and color != "" and color != "all":
        goods = Good.query.filter(and_(Good.USER_ID == user_id,
                                       Good.CLASS == category,
                                       Good.IS_PUBLISHED == 1,
                                       Good.CATEGORY_ID == good_categories_dict.get(product, ""),
                                       Good.COLOR == color)).order_by(desc(Good.CREATE_DATETIME)).all()
    elif product != "" and product != "all":
        goods = Good.query.filter(and_(Good.USER_ID == user_id,
                                       Good.CLASS == category,
                                       Good.IS_PUBLISHED == 1,
                                       Good.CATEGORY_ID == good_categories_dict.get(product, "")
                                       )).order_by(desc(Good.CREATE_DATETIME)).all()
    elif color != "" and color != "all":
        goods = Good.query.filter(and_(Good.USER_ID == user_id,
                                       Good.CLASS == category,
                                       Good.IS_PUBLISHED == 1,
                                       Good.COLOR == color)).order_by(desc(Good.CREATE_DATETIME)).all()

    goods_list = list()
    for good in goods:
        good_info = good.to_json()
        min_price, max_price = 10000000, 0
        for price in good.goodPrices:
            min_price = price.PRICE if price.PRICE < min_price else min_price
            max_price = price.PRICE if price.PRICE > max_price else max_price
        if min_price != max_price:
            good_info["PRICE"] = "{}{} - {}".format(get_currency_op(good_info["CURRENCY"]), "%.2f" % min_price, "%.2f" % max_price)
        else:
            good_info["PRICE"] = "{}{}".format(get_currency_op(good_info["CURRENCY"]), "%.2f" % min_price)
        good_info["COLOR"] = get_color_op(good_info["COLOR"]) if lang_type == 'zh_cn' else good_info["COLOR"]
        good_info["CATEGORY"] = good.category.NAME if lang_type == 'zh_cn' else good.category.EN_NAME
        goods_list.append(good_info)

    addition = set_addition(location="publishedProduct", categories="manageStaffAccounts")

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

    if lang_type not in ["zh_cn", "en_us"]:
        return render_template("404.html", lang_type=lang_type, route="manageStaffAccounts")

    if info_data.get("sort", "") == "az":
        if current_user.ROLE == 'SUPER':
            if info_data.get("position", "") == "" or info_data.get("position", "") == "all":
                users = User.query.filter(or_(User.ROLE == "AGENT", User.ROLE == "ADMIN")).order_by(asc(User.ORDERS)).all()
            else:
                users = User.query.filter_by(
                    ROLE="AGENT" if info_data.get("position", "") == "junior" else "ADMIN").order_by(asc(User.ORDERS)).all()
        elif current_user.ROLE == 'ADMIN':
            users = User.query.filter_by(ROLE="AGENT").order_by(asc(User.ORDERS)).all()
    else:
        if current_user.ROLE == 'SUPER':
            if info_data.get("position", "") == "" or info_data.get("position", "") == "all":
                users = User.query.filter(or_(User.ROLE == "AGENT", User.ROLE == "ADMIN")).order_by(desc(User.ORDERS)).all()
            else:
                users = User.query.filter_by(
                    ROLE="AGENT" if info_data.get("position", "") == "junior" else "ADMIN").order_by(asc(User.ORDERS)).all()
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
    if sort == "less_more":
        orders = Order.query.filter_by(USER_ID=user_id).order_by(asc(Order.TOTAL_AMOUNT)).all()
    else:
        orders = Order.query.filter_by(USER_ID=user_id).order_by(desc(Order.TOTAL_AMOUNT)).all()

    return render_template("admin/manage/orderHistory.html", lang=lang[lang_type],
                           lang_type=lang_type, route="orderHistory?userId={}&sort={}".format(user_id, sort),
                           addition=set_addition(location="orderHistory", categories="orderHistory"),
                           data={"userId": user_id, "user": user, "orders": orders, "sort": sort})
