import os
import random
import time
import json
import uuid
from datetime import datetime
from . import controllers
from .. import db
from flask import request
from flask import jsonify
from flask_login import login_required, current_user
from ..setting import IMAGE_FILE_DIR, INDEX_IMAGE_FILE_DIR
from ..i18 import lang
from werkzeug.utils import secure_filename

URL_PREFIX = "/common"


@controllers.route('{}/upload!single_image_upload'.format(URL_PREFIX), methods=['POST'])
@login_required
def single_image_upload():
    image = request.files["file"]
    attachment_dir = time.strftime("%Y/%m/", time.localtime())
    base_path = os.path.abspath(os.path.join(os.getcwd())).replace("\\", "/") + IMAGE_FILE_DIR
    upload_path = os.path.join(base_path, attachment_dir)

    try:
        if not os.path.exists(upload_path):
            os.makedirs(upload_path, 0o777)

        origin_filename = image.filename
        image_filename = str(uuid.uuid1()) + "." + image.filename.rsplit('.', 1)[1]
        src = os.path.join(upload_path + secure_filename(image_filename))  # image.filename
        image.save(src)

        return jsonify({'code': 0, 'msg': 'Success',
                        'data': {'url': '/static/uploads/images/{}{}'.format(attachment_dir, image_filename),
                                 'originFileName': origin_filename, 'code': 0}})
    except:
        return jsonify({'code': 0, 'msg': 'Fail', 'data': {'code': 1}})


@controllers.route('{}/upload!index_men_image_upload'.format(URL_PREFIX), methods=['POST'])
@login_required
def index_men_image_upload():
    image = request.files["file"]
    upload_path = os.path.abspath(os.path.join(os.getcwd())).replace("\\", "/") + INDEX_IMAGE_FILE_DIR

    try:
        if not os.path.exists(upload_path):
            os.makedirs(upload_path, 0o777)

        origin_filename = image.filename
        image_filename = "indexMen.jpg"
        src = os.path.join(upload_path + secure_filename(image_filename))  # image.filename
        image.save(src)

        return jsonify({'code': 0, 'msg': 'Success',
                        'data': {'url': '/static/uploads/indexMen.jpg?rand={}'.format(random.randint(0, 10000)),
                                 'code': 0}})
    except:
        return jsonify({'code': 0, 'msg': 'Fail',
                        'data': {'url': '/static/uploads/indexMen.jpg?rand={}'.format(random.randint(0, 10000)),
                                 'code': 1}})


@controllers.route('{}/upload!index_women_image_upload'.format(URL_PREFIX), methods=['POST'])
@login_required
def index_women_image_upload():
    image = request.files["file"]
    upload_path = os.path.abspath(os.path.join(os.getcwd())).replace("\\", "/") + INDEX_IMAGE_FILE_DIR

    try:
        if not os.path.exists(upload_path):
            os.makedirs(upload_path, 0o777)

        origin_filename = image.filename
        image_filename = "indexWomen.jpg"
        src = os.path.join(upload_path + secure_filename(image_filename))  # image.filename
        image.save(src)

        return jsonify({'code': 0, 'msg': 'Success',
                        'data': {'url': '/static/uploads/indexWomen.jpg?rand={}'.format(random.randint(0, 10000)),
                                 'code': 0}})
    except:
        return jsonify({'code': 0, 'msg': 'Fail',
                        'data': {'url': '/static/uploads/indexWomen.jpg?rand={}'.format(random.randint(0, 10000)),
                                 'code': 1}})


@controllers.route('{}/upload!index_new_image_upload'.format(URL_PREFIX), methods=['POST'])
@login_required
def index_new_image_upload():
    image = request.files["file"]
    upload_path = os.path.abspath(os.path.join(os.getcwd())).replace("\\", "/") + INDEX_IMAGE_FILE_DIR

    try:
        if not os.path.exists(upload_path):
            os.makedirs(upload_path, 0o777)

        origin_filename = image.filename
        image_filename = "indexNew.jpg"
        src = os.path.join(upload_path + secure_filename(image_filename))  # image.filename
        image.save(src)

        return jsonify({'code': 0, 'msg': 'Success',
                        'data': {'url': '/static/uploads/indexNew.jpg?rand={}'.format(random.randint(0, 10000)),
                                 'code': 0}})
    except:
        return jsonify({'code': 0, 'msg': 'Fail',
                        'data': {'url': '/static/uploads/indexNew.jpg?rand={}'.format(random.randint(0, 10000)),
                                 'code': 1}})


@controllers.route('{}/upload!index_about_image_upload'.format(URL_PREFIX), methods=['POST'])
@login_required
def index_about_image_upload():
    image = request.files["file"]
    upload_path = os.path.abspath(os.path.join(os.getcwd())).replace("\\", "/") + INDEX_IMAGE_FILE_DIR

    try:
        if not os.path.exists(upload_path):
            os.makedirs(upload_path, 0o777)

        origin_filename = image.filename
        image_filename = "aboutUs.jpg"
        src = os.path.join(upload_path + secure_filename(image_filename))  # image.filename
        image.save(src)

        return jsonify({'code': 0, 'msg': 'Success',
                        'data': {'url': '/static/uploads/aboutUs.jpg?rand={}'.format(random.randint(0, 10000)), 'code': 0}})
    except:
        return jsonify({'code': 0, 'msg': 'Fail',
                        'data': {'url': '/static/uploads/aboutUs.jpg?rand={}'.format(random.randint(0, 10000)), 'code': 1}})


@controllers.route('{}/upload!index_contact_image_upload'.format(URL_PREFIX), methods=['POST'])
@login_required
def index_contact_image_upload():
    image = request.files["file"]
    upload_path = os.path.abspath(os.path.join(os.getcwd())).replace("\\", "/") + INDEX_IMAGE_FILE_DIR

    try:
        if not os.path.exists(upload_path):
            os.makedirs(upload_path, 0o777)

        origin_filename = image.filename
        image_filename = "contactUs.jpg"
        src = os.path.join(upload_path + secure_filename(image_filename))  # image.filename
        image.save(src)

        return jsonify({'code': 0, 'msg': 'Success',
                        'data': {'url': '/static/uploads/contactUs.jpg?rand={}'.format(random.randint(0, 10000)),
                                 'code': 0}})
    except:
        return jsonify({'code': 0, 'msg': 'Fail',
                        'data': {'url': '/static/uploads/contactUs.jpg?rand={}'.format(random.randint(0, 10000)),
                                 'code': 1}})
