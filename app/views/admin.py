from . import views
from flask import jsonify
from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user
from datetime import datetime
from ..models import *
from sqlalchemy import asc
from ..utils.set import set_addition
from ..utils.get import get_currency_op
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
    if lang_type not in ["zh_cn", "en_us"]:
        return render_template("404.html", lang_type=lang_type, route="publishedProduct")
    return render_template("admin/publishedProduct.html", lang=lang[lang_type],
                           lang_type=lang_type, route="publishedProduct",
                           addition=set_addition(location="publishedProduct"))


##############################超管###############################

@views.route('/<lang_type>/manageStaffAccounts', methods=['GET', 'POST'])
@login_required
def manage_staff_accounts(lang_type):
    """ 管理员工账号"""
    if lang_type not in ["zh_cn", "en_us"]:
        return render_template("404.html", lang_type=lang_type, route="manageStaffAccounts")
    return render_template("admin/manageStaffAccounts.html", lang=lang[lang_type],
                           lang_type=lang_type, route="manageStaffAccounts",
                           addition=set_addition(location="manageStaffAccounts"))


@views.route('/<lang_type>/manageCustomerAccounts', methods=['GET', 'POST'])
@login_required
def manage_customer_accounts(lang_type):
    """ 管理客户账号"""
    if lang_type not in ["zh_cn", "en_us"]:
        return render_template("404.html", lang_type=lang_type, route="manageCustomerAccounts")
    return render_template("admin/manageCustomerAccounts.html", lang=lang[lang_type],
                           lang_type=lang_type, route="manageCustomerAccounts",
                           addition=set_addition(location="manageCustomerAccounts"))
