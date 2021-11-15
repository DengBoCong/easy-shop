from flask_login import current_user
from .. import mail
from flask_mail import Mail, Message
from ..setting import *


def set_addition(add="", location="", categories="", products="", sort="", colors="", page=0):
    return {
        "add": add,
        "location": location,
        "categories": categories,
        "products": products,
        "sort": sort,
        "colors": colors,
        "page": page,
        "login": hasattr(current_user, "ID")
    }


def send_mail(single_email, user_email, order_num, trace_num):
    msg = Message('有一个新订单，请查收', sender=SEND_EMAIL, recipients=[single_email])
    msg.body = "订单客户：{}\n订单编号：#{}\n跟踪编号：{}".format(user_email, order_num, trace_num)
    mail.send(msg)
