import os
import time
import json
import uuid
from datetime import datetime
from . import controllers
from .. import db
from ..models import Attachment
from flask import request
from flask import jsonify
from flask_login import login_required, current_user
from ..utils import set_system_log
from ..setting import IMAGE_FILE_DIR, FILE_DIR
from werkzeug.utils import secure_filename

URL_PREFIX = "/common"


@controllers.route('{}/upload!single_image_upload'.format(URL_PREFIX), methods=['POST'])
@login_required
def single_image_upload():
    image = request.files["file"]
    attachment_dir = time.strftime("%Y/%m/", time.localtime())
    base_path = os.path.abspath(os.path.join(os.getcwd())).replace("\\", "/") + IMAGE_FILE_DIR
    upload_path = os.path.join(base_path, attachment_dir)

    is_exist = os.path.exists(upload_path)
    try:
        if not is_exist:
            os.makedirs(upload_path, 0o777)

        image_filename = str(uuid.uuid1()) + "." + image.filename.rsplit('.', 1)[1]
        src = os.path.join(upload_path + secure_filename(image_filename))  # image.filename
        image.save(src)

        set_system_log(PATH="/api/common/upload!single_image_upload", ACTION="common", MESSAGE="成功上传了图片", LEVEL="INFO")

        return jsonify({'code': 0, 'msg': '上传成功',
                        'data': {'url': '/static/uploads/images/{}{}'.format(attachment_dir, image_filename)}})
    except:
        set_system_log(PATH="/api/common/upload!single_image_upload", ACTION="common", MESSAGE="图片上传失败", LEVEL="ERROR")
        return jsonify({'code': 1, 'msg': '上传失败', 'data': {}})


@controllers.route('{}/upload!multi_file_upload'.format(URL_PREFIX), methods=['POST'])
@login_required
def multi_file_upload():
    file = request.files["file"]
    attachment_dir = time.strftime("%Y/%m/", time.localtime())
    base_path = os.path.abspath(os.path.join(os.getcwd())).replace("\\", "/") + FILE_DIR
    upload_path = os.path.join(base_path, attachment_dir)

    is_exist = os.path.exists(upload_path)
    try:
        if not is_exist:
            os.makedirs(upload_path, 0o777)

        filename = str(uuid.uuid1()) + "." + file.filename.rsplit('.', 1)[1]
        src = os.path.join(upload_path + secure_filename(filename))  # image.filename
        file.save(src)

        set_system_log(PATH="/api/common/upload!multi_file_upload", ACTION="common", MESSAGE="成功上传了附件", LEVEL="INFO")

        return jsonify({'code': 0, 'msg': '上传成功',
                        'data': {'url': '/static/uploads/files/{}{}'.format(attachment_dir, filename),
                                 "filename": file.filename}})
    except:
        set_system_log(PATH="/api/common/upload!multi_file_upload", ACTION="common", MESSAGE="附件上传失败", LEVEL="ERROR")
        return jsonify({'code': 1, 'msg': '上传失败', 'data': {}})


@controllers.route('{}/add!add_attachment'.format(URL_PREFIX), methods=['POST'])
@login_required
def add_attachment():
    try:
        info_data = json.loads(request.get_data())
        attach_id = uuid.uuid1()
        attach = Attachment(ID=attach_id, CREATE_DATETIME=datetime.now(), UPDATE_DATETIME=datetime.now(),
                            USER_ID=current_user.ID, DATA_ID="", NAME=info_data.get("name"),
                            PATH=info_data.get("url"), VERB_NOTICE_ID=info_data.get("noticeId"))
        db.session.add(attach)
        db.session.commit()
        return jsonify({'code': 0, 'msg': '添加成功', 'data': attach_id})
    except:
        return jsonify({'code': 1, 'msg': '网络异常，更新失败', 'data': {}})
