import json
import uuid
from datetime import datetime
from .. import db
from . import controllers
from ..models import *
from flask import request, redirect, url_for
from flask import jsonify
from flask_login import current_user, logout_user, login_required
from sqlalchemy import asc, and_
from ..i18 import lang

URL_PREFIX = "/good"


@controllers.route('{}/get!get_all_good_category'.format(URL_PREFIX), methods=['GET'])
@login_required
def get_all_good_category():
    info_data = request.args.to_dict()
    lang_type = info_data["langType"]
    try:
        good_categories = GoodCategory.query.order_by(asc(GoodCategory.EN_NAME)).all()
        good_categories_list = []
        for good_category in good_categories:
            good_categories_list.append(good_category.to_json())
        return jsonify({'code': 0, 'msg': '', 'data': good_categories_list})
    except:
        return jsonify({'code': 1, 'msg': lang[lang_type]["inner_network_abnormal"], 'data': [{}]})


@controllers.route('{}/add!add_good_category'.format(URL_PREFIX), methods=['POST'])
@login_required
def add_good_category():
    info_data = json.loads(request.get_data())
    lang_type = info_data["langType"]

    try:
        name_good_category = GoodCategory.query.filter_by(NAME=info_data.get("NAME")).all()
        en_name_good_category = GoodCategory.query.filter_by(EN_NAME=info_data.get("EN_NAME")).all()

        if len(name_good_category) != 0:
            return jsonify({'code': 1, 'msg': lang[lang_type]["inner_zh_ch_repeat_reset"], 'data': {}})
        elif len(en_name_good_category) != 0:
            return jsonify({'code': 1, 'msg': lang[lang_type]["inner_en_us_repeat_reset"], 'data': {}})
        else:
            good_category = GoodCategory(ID=uuid.uuid1(), CREATE_DATETIME=datetime.now(), NAME=info_data.get("NAME"),
                                         EN_NAME=info_data.get("EN_NAME"), DESCRIPTION=info_data.get("DESCRIPTION", ""))
            db.session.add(good_category)
            db.session.commit()

            good_categories = GoodCategory.query.order_by(asc(GoodCategory.EN_NAME)).all()
            good_categories_list = []
            for good_category in good_categories:
                good_categories_list.append(good_category.to_json())

            return jsonify({'code': 0, 'msg': lang[lang_type]["inner_add_success"],
                            'data': {"goodCategories": good_categories_list}})
    except:
        return jsonify({'code': 1, 'msg': lang[lang_type]["inner_network_abnormal"], 'data': {}})


######################Good Size#########################

@controllers.route('{}/get!get_all_good_size'.format(URL_PREFIX), methods=['GET'])
@login_required
def get_all_good_size():
    info_data = request.args.to_dict()
    lang_type = info_data["langType"]
    try:
        good_sizes = GoodSize.query.order_by(asc(GoodSize.SIZE)).all()
        good_sizes_list = []
        for good_size in good_sizes:
            good_sizes_list.append(good_size.to_json())
        return jsonify({'code': 0, 'msg': '', 'data': good_sizes_list})
    except:
        return jsonify({'code': 1, 'msg': lang[lang_type]["inner_network_abnormal"], 'data': [{}]})


@controllers.route('{}/add!add_good_size'.format(URL_PREFIX), methods=['POST'])
@login_required
def add_good_size():
    info_data = json.loads(request.get_data())
    lang_type = info_data["langType"]

    try:
        size_good_size = GoodSize.query.filter_by(SIZE=info_data.get("SIZE")).all()

        if len(size_good_size) != 0:
            return jsonify({'code': 1, 'msg': lang[lang_type]["inner_repeat_reset"], 'data': {}})
        else:
            good_size = GoodSize(ID=uuid.uuid1(), CREATE_DATETIME=datetime.now(),
                                 SIZE=info_data.get("SIZE"), DESCRIPTION=info_data.get("DESCRIPTION", ""))
            db.session.add(good_size)
            db.session.commit()

            good_sizes = GoodSize.query.order_by(asc(GoodSize.SIZE)).all()
            good_sizes_list = []
            for good_size in good_sizes:
                good_sizes_list.append(good_size.to_json())

            return jsonify({'code': 0, 'msg': lang[lang_type]["inner_add_success"],
                            'data': {"goodSizes": good_sizes_list}})
    except:
        return jsonify({'code': 1, 'msg': lang[lang_type]["inner_network_abnormal"], 'data': {}})


######################Good#########################

@controllers.route('{}/add!add_good'.format(URL_PREFIX), methods=['POST'])
@login_required
def add_good():
    info_data = json.loads(request.get_data())
    lang_type = info_data["langType"]

    try:
        good_category = GoodCategory.query.get(info_data.get("CATEGORY_ID"))

        good_id = uuid.uuid1()
        good_prices, min_price = list(), float(info_data.get("PRICE", 100000000))
        for price in info_data.get("PRICE_RANGE", []):
            min_price = min(min_price, float(price.get("PRICE", 0)))
            good_prices.append(GoodPrice(ID=uuid.uuid1(), CREATE_DATETIME=datetime.now(), GOOD_ID=good_id,
                                         START_NUM=price.get("START_NUM", 0), END_NUM=price.get("END_NUM", 0),
                                         PRICE=price.get("PRICE", 0)))
        db.session.add_all(good_prices)
        good = Good(ID=good_id, CREATE_DATETIME=datetime.now(), BRAND=info_data.get("BRAND"),
                    COLOR=info_data.get("COLOR"), STYLE=info_data.get("STYLE"),
                    DESCRIPTION=info_data.get("DESCRIPTION"), SUPPLIER_COLOR=info_data.get("SUPPLIER_COLOR"),
                    MATERIAL=info_data.get("MATERIAL"), PLACE_OF_ORIGIN=info_data.get("PLACE_OF_ORIGIN"),
                    PRODUCT_NUMBER=info_data.get("PRODUCT_NUMBER"), FACTORY_CODE=info_data.get("FACTORY_CODE"),
                    AREA_ID=info_data.get("AREA_ID"), CURRENCY=info_data.get("CURRENCY"),
                    CATEGORY_ID=info_data.get("CATEGORY_ID"), SIZE=info_data.get("SIZE"),
                    SIZE_CHART=info_data.get("SIZE_CHART"), STAFF_EMAIL=info_data.get("STAFF_EMAIL"),
                    IS_PUBLISHED=info_data.get("IS_PUBLISHED"), CLASS=info_data.get("CLASS"),
                    TYPE=info_data.get("TYPE").upper(), COVER=info_data.get("GOOD_IMG", [""])[0],
                    USER_ID=info_data.get("USER_ID"), NUM=0, PRICE=min_price, CATEGORY=good_category.EN_NAME)
        db.session.add(good)

        good_img = list()
        for img in info_data.get("GOOD_IMG", [])[1:]:
            good_img.append(GoodImg(ID=uuid.uuid1(), CREATE_DATETIME=datetime.now(), GOOD_ID=good_id, URL=img))
        db.session.add_all(good_img)

        db.session.commit()

        return jsonify({'code': 0, 'msg': lang[lang_type]["common_redirecting"],
                        'data': {"goodId": good_id}})
        # if info_data.get("IS_PUBLISHED") == 0:
        #     return redirect(url_for('views.preview_products', lang_type=lang_type, good_id=good_id))
        # else:
        #     return redirect(url_for('views.product_details', lang_type=lang_type, good_id=good_id))
    except:
        return jsonify({'code': 1, 'msg': lang[lang_type]["inner_network_abnormal"], 'data': {}})


@controllers.route('{}/update!update_good'.format(URL_PREFIX), methods=['POST'])
@login_required
def update_good():
    info_data = json.loads(request.get_data())
    lang_type = info_data["langType"]
    good_id = info_data["ID"]

    if len(info_data.get("GOOD_IMG", [])) != 0:
        GoodImg.query.filter_by(GOOD_ID=good_id).delete()
        db.session.commit()
        good_img = list()
        for img in info_data.get("GOOD_IMG")[1:]:
            good_img.append(GoodImg(ID=uuid.uuid1(), CREATE_DATETIME=datetime.now(), GOOD_ID=good_id, URL=img))
        db.session.add_all(good_img)
        db.session.commit()

    min_price = float(info_data.get("PRICE", 100000000))
    if len(info_data.get("PRICE_RANGE", [])) != 0:
        GoodPrice.query.filter_by(GOOD_ID=good_id).delete()
        db.session.commit()
        good_prices = list()
        for price in info_data.get("PRICE_RANGE", []):
            if price:
                min_price = min(min_price, float(price.get("PRICE", 0)))
                good_prices.append(GoodPrice(ID=uuid.uuid1(), CREATE_DATETIME=datetime.now(), GOOD_ID=good_id,
                                             START_NUM=price.get("START_NUM", 0), END_NUM=price.get("END_NUM", 0),
                                             PRICE=price.get("PRICE", 0)))
        db.session.add_all(good_prices)
        db.session.commit()

    try:
        del info_data["langType"]
        if "PRICE_RANGE" in info_data.keys():
            del info_data["PRICE_RANGE"]
        if "GOOD_IMG" in info_data.keys():
            del info_data["GOOD_IMG"]

        if min_price:
            info_data["PRICE"] = min_price
        if info_data.get("CATEGORY_ID", None):
            good_category = GoodCategory.query.get(info_data.get("CATEGORY_ID"))
            info_data["CATEGORY"] = good_category.EN_NAME
        print(info_data)
        good = Good.query.filter_by(ID=info_data.get("ID")).update(info_data)
        print("极乐空间啥地方")
        if good == 1:
            db.session.commit()

            return jsonify({'code': 0, 'msg': lang[lang_type]["common_redirecting"],
                            'data': {"goodId": info_data.get("ID")}})
        else:
            return jsonify({'code': 1, 'msg': lang[lang_type]["common_update_fail"], 'data': {}})

    except:
        return jsonify({'code': 1, 'msg': lang[lang_type]["inner_network_abnormal"], 'data': {}})


######################WishGood#########################
@controllers.route('{}/add!add_wish_good'.format(URL_PREFIX), methods=['POST'])
@login_required
def add_wish_good():
    info_data = json.loads(request.get_data())
    lang_type = info_data["langType"]

    try:
        wish_good = WishGood.query.filter(and_(
            WishGood.USER_ID == current_user.ID,
            WishGood.GOOD_ID == info_data["GOOD_ID"],
            WishGood.SIZE == info_data["SIZE"])).all()

        if len(wish_good) != 0:
            return jsonify({'code': 1, 'msg': lang[lang_type]["inner_add_repeat"], 'data': {}})
        else:
            wish_good = WishGood(ID=uuid.uuid1(), CREATE_DATETIME=datetime.now(), USER_ID=current_user.ID,
                                 GOOD_ID=info_data["GOOD_ID"], SIZE=info_data["SIZE"], NUM=info_data["NUM"])
            db.session.add(wish_good)
            db.session.commit()

            return jsonify({'code': 0, 'msg': lang[lang_type]["inner_add_success"], 'data': {}})
    except:
        return jsonify({'code': 1, 'msg': lang[lang_type]["inner_network_abnormal"], 'data': {}})


@controllers.route('{}/delete!delete_wish_good'.format(URL_PREFIX), methods=['POST'])
@login_required
def delete_wish_good_by_id():
    info_data = json.loads(request.get_data())
    lang_type = info_data["langType"]
    wish_good = WishGood.query.get(info_data.get("ID"))

    if wish_good is not None:
        db.session.delete(wish_good)
        db.session.commit()

        return jsonify({'code': 0, 'msg': lang[lang_type]["inner_delete_success"], 'data': {}})
    else:
        return jsonify({'code': 1, 'msg': lang[lang_type]["inner_network_abnormal"], 'data': {}})
