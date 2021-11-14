import random
from datetime import datetime


def get_currency_op(currency: str):
    index_dict = {
        "rmb": "￥",
        "jpn": "￥",
        "eur": "€",
        "usd": "$"
    }

    return index_dict.get(currency.lower(), "￥")


def get_currency_lang_op(currency: str):
    index_dict = {
        "rmb": "人民币",
        "jpn": "日元",
        "eur": "欧元",
        "usd": "美元"
    }

    return index_dict.get(currency.lower(), "￥")


def get_color_op(color: str):
    index_dict = {
        "brown": "棕色",
        "blue": "黑色",
        "gray": "灰色",
        "white": "白色",
        "pink": "粉色",
        "purple": "紫色",
        "red": "红色",
        "green": "绿色",
        "yellow": "黄色",
        "black": "黑色"
    }

    return index_dict.get(color.lower(), "")


def get_order_code():
    base_code = datetime.now().strftime('%Y%m%d%H%M%S')
    return base_code + str(random.randint(0, 1000))
