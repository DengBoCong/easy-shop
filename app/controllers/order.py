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
from ..utils.get import *

URL_PREFIX = "/order"


@controllers.route('{}/add!place_order'.format(URL_PREFIX), methods=['POST'])
@login_required
def place_order():
    info_data = json.loads(request.get_data())
    lang_type = info_data["langType"]

    try:
        order_id = uuid.uuid1()
        shopping_goods = ShoppingGood.query.filter_by(USER_ID=current_user.ID).all()
        goods_list, order_good_list = list(), list()
        amount, shipping = 0.0, 0.0

        for shopping_good in shopping_goods:
            single_price = 0.0
            if shopping_good.good.CLASS != "DESIGN":
                if shopping_good.good.CLASS != "REFERENCE":
                    single_price = float(shopping_good.good.PRICE)
                    amount += single_price * shopping_good.NUM
                else:
                    for price in shopping_good.good.goodPrices:
                        if price.START_NUM < shopping_good.NUM < price.END_NUM:
                            single_price = float(price.PRICE)
                            amount += single_price * shopping_good.NUM
                            break

            order_good = OrderGood(ID=uuid.uuid1(), CREATE_DATETIME=datetime.now(), ORDER_ID=order_id,
                                   GOOD_ID=shopping_good.good.ID, NUM=shopping_good.NUM, TITLE="",
                                   PRICE=single_price, EMAIL=shopping_good.good.STAFF_EMAIL)
            order_good_list.append(order_good)

        db.session.add_all(order_good_list)
        order = Order(ID=order_id, CREATE_DATETIME=datetime.now(), NUM=get_order_code(), TOTAL_AMOUNT=amount,
                      STATUS="Processing", TRACK_NUM=str(uuid.uuid1()).replace("-", ""), USER_ID=current_user.ID,
                      CLASS="NORMAL")
        db.session.add(order)
        user = User.query.get(current_user.ID)
        user.ORDERS += 1
        db.session.commit()

        return jsonify({'code': 0, 'msg': lang[lang_type]["inner_add_success"], 'data': {"orderId": order_id}})
    except:
        return jsonify({'code': 1, 'msg': lang[lang_type]["inner_network_abnormal"], 'data': {}})


@controllers.route('{}/add!place_sample_order'.format(URL_PREFIX), methods=['POST'])
@login_required
def place_sample_order():
    info_data = json.loads(request.get_data())
    lang_type = info_data["langType"]

    try:
        order_id = uuid.uuid1()
        sample_goods = SampleGood.query.filter_by(USER_ID=current_user.ID).all()
        goods_list, order_good_list = list(), list()
        amount, shipping = 0.0, 0.0

        for sample_good in sample_goods:
            single_price = 0.0
            if sample_good.good.CLASS != "DESIGN":
                if sample_good.good.CLASS != "REFERENCE":
                    single_price = float(sample_good.good.PRICE)
                    amount += single_price * sample_good.NUM
                else:
                    for price in sample_good.good.goodPrices:
                        if price.START_NUM < sample_good.NUM < price.END_NUM:
                            single_price = float(price.PRICE)
                            amount += single_price * sample_good.NUM
                            break

            order_good = OrderGood(ID=uuid.uuid1(), CREATE_DATETIME=datetime.now(), ORDER_ID=order_id,
                                   GOOD_ID=sample_good.good.ID, NUM=sample_good.NUM, TITLE="",
                                   PRICE=single_price, EMAIL=sample_good.good.STAFF_EMAIL)
            order_good_list.append(order_good)

        db.session.add_all(order_good_list)
        order = Order(ID=order_id, CREATE_DATETIME=datetime.now(), NUM=get_order_code(), TOTAL_AMOUNT=amount,
                      STATUS="Processing", TRACK_NUM=str(uuid.uuid1()).replace("-", ""), USER_ID=current_user.ID,
                      CLASS="SAMPLE")

        db.session.add(order)
        user = User.query.get(current_user.ID)
        user.ORDERS += 1
        db.session.commit()

        return jsonify({'code': 0, 'msg': lang[lang_type]["inner_add_success"], 'data': {"orderId": order_id}})
    except:
        return jsonify({'code': 1, 'msg': lang[lang_type]["inner_network_abnormal"], 'data': {}})
