import re
import os
import time
import json
import uuid
from datetime import datetime
from . import controllers
from .. import db
from ..models import *
from flask import request
from flask import jsonify
from flask_login import login_required, current_user
from ..utils import set_system_log, is_all_chinese
from ..setting import TEMP_FILE_DIR, USER_NODE_ID
from werkzeug.utils import secure_filename

URL_PREFIX = "/preprocess"


@controllers.route('{}/upload!multi_verb_file_upload'.format(URL_PREFIX), methods=['POST'])
@login_required
def multi_verb_file_upload():
    file = request.files["file"]
    temp_dir = time.strftime("%Y/%m/", time.localtime()) + str(uuid.uuid1()) + "/"
    base_path = os.path.abspath(os.path.join(os.getcwd())).replace("\\", "/") + TEMP_FILE_DIR
    upload_path = os.path.join(base_path, temp_dir)

    is_exist = os.path.exists(upload_path)
    try:
        if not is_exist:
            os.makedirs(upload_path, 0o777)

        src = os.path.join(upload_path + file.filename)
        file.save(src)

        set_system_log(PATH="/api/preprocess/upload!multi_verb_file_upload", ACTION="preprocess",
                       MESSAGE="成功上传了Verb标注数据文件", LEVEL="INFO")

        return jsonify({'code': 0, 'msg': '上传成功',
                        'data': {'url': TEMP_FILE_DIR + '{}{}'.format(temp_dir, file.filename),
                                 "tagName": file.filename.rsplit('.', 1)[0]}})
    except:
        set_system_log(PATH="/api/preprocess/upload!multi_verb_file_upload", ACTION="preprocess",
                       MESSAGE="Verb数据标注文件上传失败", LEVEL="ERROR")
        return jsonify({'code': 1, 'msg': '上传失败', 'data': {}})


@controllers.route('{}/process!multi_verb_data'.format(URL_PREFIX), methods=['POST'])
@login_required
def process_multi_verb_data():
    info_data = json.loads(request.get_data())
    file_list = info_data.get("fileList")
    tag_names = info_data.get("tagNames")
    finish_list, skip_list = list(), list()
    match_re = re.compile(r'[\[](.*?)[]]', re.S)
    try:
        for file_path, tag_name in zip(file_list, tag_names):
            verb = Verb.query.filter_by(NAME=tag_name).all()
            if verb:
                skip_list.append({"fileName": tag_name, "reason": "当前Frame中已存在该Verb"})
                continue
            file_path = os.path.abspath(os.path.join(os.getcwd())).replace("\\", "/") + file_path
            patterns, pattern, flag, skip_flag = list(), dict(), False, True
            if not is_all_chinese(tag_name):
                skip_list.append({"fileName": tag_name, "reason": "文件名不符合要求"})
                continue
            verb_info = {"NAME": tag_name}
            with open(file_path, "r", encoding="utf-8") as file:
                for line in file:
                    line = line.strip("\n").strip()
                    if line == "":
                        continue
                    if line[0] == "#":
                        line = line.split(":")
                        if "pinyin" in line[0]:
                            verb_info["PIN_YIN"] = line[1].strip().strip("\n")
                        elif "frequency" in line[0]:
                            verb_info["FREQUENCY"] = int(line[1].strip().strip("\n"))
                    elif line[0] == "%":
                        if flag:
                            if not pattern.get("pattern", None):
                                skip_list.append({"fileName": tag_name, "reason": "数据文件中存在Pattern信息残缺"})
                                skip_flag = False
                                break
                            patterns.append(pattern)
                            pattern = dict()
                            flag = False
                        line = line.split(":")
                        if "CONSTRUCTION" in line[0]:
                            temp = line[1].strip().strip("\n")
                            element_list = re.findall(match_re, temp)
                            pattern["construction"] = "[" + "]-[".join(element_list) + "]"
                        elif "PATTERN" in line[0]:
                            temp = line[1].strip().strip("\n")
                            element_list = re.findall(match_re, temp)
                            pattern["pattern"] = "[" + "]-[".join(element_list) + "]"
                            pattern["sample"] = list()
                            flag = True
                    else:
                        if not pattern.get("pattern", None):
                            skip_list.append({"fileName": tag_name, "reason": "数据文件中存在Pattern信息残缺"})
                            skip_flag = False
                            break
                        pattern["sample"].append(line)

            if skip_flag:
                verb_id = uuid.uuid1()
                verb = Verb(ID=verb_id, CREATE_DATETIME=datetime.now(), UPDATE_DATETIME=datetime.now(),
                            NAME=verb_info.get("NAME", "None"), PIN_YIN=verb_info.get("PIN_YIN", "None"),
                            FREQUENCY=verb_info.get("FREQUENCY", 0), FRAMES_ID=info_data.get("frameId"))
                for sub_pattern in patterns:
                    sub_pattern_id = uuid.uuid1()
                    pattern_info = VerbPattern(ID=sub_pattern_id, CREATE_DATETIME=datetime.now(),
                                               UPDATE_DATETIME=datetime.now(),
                                               CONSTRUCTION=sub_pattern.get("construction", "None"), VERB_ID=verb_id,
                                               PATTERN=sub_pattern.get("pattern", "None"))

                    db.session.execute(
                        Sample.__table__.insert(),
                        [{"ID": uuid.uuid1(), "CREATE_DATETIME": datetime.now(), "UPDATE_DATETIME": datetime.now(),
                          "CONTENT": sample, "VERB_PATTERN_ID": sub_pattern_id} for sample in sub_pattern["sample"]]
                    )
                    db.session.add(pattern_info)
                db.session.add(verb)
                db.session.commit()
                finish_list.append(tag_name)

        set_system_log(PATH="/api/preprocess/process!multi_verb_data", ACTION="preprocess",
                       MESSAGE="成功上传了Verb标注数据文件", LEVEL="INFO")

        return jsonify({'code': 0, 'msg': '上传成功', 'data': {"finish": finish_list, "skip": skip_list}})
    except:
        set_system_log(PATH="/api/preprocess/upload!preprocess", ACTION="preprocess",
                       MESSAGE="Verb数据标注文件上传失败", LEVEL="ERROR")
        return jsonify({'code': 1, 'msg': '上传失败', 'data': {"finish": finish_list}})


@controllers.route('{}/upload!multi_frame_file_upload'.format(URL_PREFIX), methods=['POST'])
@login_required
def multi_frame_file_upload():
    file = request.files["file"]
    temp_dir = time.strftime("%Y/%m/", time.localtime()) + str(uuid.uuid1()) + "/"
    base_path = os.path.abspath(os.path.join(os.getcwd())).replace("\\", "/") + TEMP_FILE_DIR
    upload_path = os.path.join(base_path, temp_dir)

    is_exist = os.path.exists(upload_path)
    try:
        if not is_exist:
            os.makedirs(upload_path, 0o777)

        src = os.path.join(upload_path + file.filename)
        file.save(src)

        set_system_log(PATH="/api/preprocess/upload!multi_frame_file_upload", ACTION="preprocess",
                       MESSAGE="成功上传了Frame数据文件", LEVEL="INFO")

        return jsonify({'code': 0, 'msg': '上传成功',
                        'data': {'url': TEMP_FILE_DIR + '{}{}'.format(temp_dir, file.filename),
                                 "tagName": file.filename.rsplit('.', 1)[0]}})
    except:
        set_system_log(PATH="/api/preprocess/upload!multi_frame_file_upload", ACTION="preprocess",
                       MESSAGE="Frame数据文件上传失败", LEVEL="ERROR")
        return jsonify({'code': 1, 'msg': '上传失败', 'data': {}})


@controllers.route('{}/process!multi_frame_data'.format(URL_PREFIX), methods=['POST'])
@login_required
def process_multi_frame_data():
    info_data = json.loads(request.get_data())
    file_list = info_data.get("fileList")
    tag_names = info_data.get("tagNames")
    finish_list, skip_list = list(), list()
    match_re = re.compile(r'[\[](.*?)[]]', re.S)
    try:
        for file_path, tag_name in zip(file_list, tag_names):
            frame = Frame.query.filter_by(NAME=tag_name).all()
            if frame:
                skip_list.append({"fileName": tag_name, "reason": "该Frame已存在数据库中"})
                continue
            file_path = os.path.abspath(os.path.join(os.getcwd())).replace("\\", "/") + file_path
            element_flag, skip_flag = None, True
            frame_element_list, element_sample_list = list(), list()

            # if not tag_name.encode('UTF-8').isalpha():
            #     skip_list.append({"fileName": tag_name, "reason": "文件名不符合要求"})
            #     continue
            frame_info = {"ID": uuid.uuid1(), "CREATE_DATETIME": datetime.now(),
                          "UPDATE_DATETIME": datetime.now(), "NAME": tag_name, "PARENT_ID": USER_NODE_ID}
            with open(file_path, "r", encoding="utf-8") as file:
                lines = file.readlines()
                for i in range(len(lines)):
                    line = lines[i].strip("\n").strip()
                    if line == "":
                        continue
                    elif line.lower() == "[core]":
                        element_flag = "Core Frame Elements"
                        continue
                    elif line.lower() == "[non-core]":
                        element_flag = "Non-core Frame Elements"
                        continue
                    elif line.lower() == "[*construction marker]":
                        element_flag = "Construction Marker"
                        continue

                    line = line.split(":")
                    if not element_flag:
                        if "Def." in line[0]:
                            frame_info["DEF"] = line[1].strip().strip("\n")
                        elif "Frame type" in line[0]:
                            frame_info["FRAME_TYPE"] = line[1].strip().strip("\n").split(" ")[0]
                        elif "Pattern" in line[0]:
                            frame_info["PATTERN"] = line[1].strip().strip("\n")
                        elif "Sample" in line[0]:
                            frame_info["SAMPLE"] = line[1].strip().strip("\n")
                        elif len(line) == 1:
                            frame_info["SAMPLE"] += line[0].strip().strip("\n")
                    else:
                        if "Tag" in line[0]:
                            tag = line[1].strip().strip("\n")
                            def_str, lemma_str, sample_str = "", "", ""
                            element_type = FrameElementType.query.filter(FrameElementType.NAME==tag, FrameElementType.TYPE==element_flag).first()
                            if not element_type:
                                element_type = FrameElementType(ID=uuid.uuid1(), CREATE_DATETIME=datetime.now(),
                                                                TYPE=element_flag, NAME=tag)
                                db.session.add(element_type)

                            def_line = lines[i + 1].strip("\n").strip().split(":")
                            if "Def." in def_line[0]:
                                def_str = def_line[1].strip().strip("\n")
                            lemma_line = lines[i + 2].strip("\n").strip().split(":")
                            if "Lemma" in lemma_line[0]:
                                lemma_str = lemma_line[1].strip().strip("\n")
                            sample_line = lines[i + 3].strip("\n").strip().split(":")
                            if "Sample" in sample_line[0]:
                                sample_str = sample_line[1].strip().strip("\n")

                            temp_count = 4
                            while i + temp_count < len(lines) and lines[i + temp_count].strip("\n").strip() != "" and len(lines[i + temp_count].strip("\n").strip().split(":")) == 1:
                                sample_str += lines[i + temp_count].strip("\n").strip()
                                temp_count += 1

                            frame_element = FrameElement.query.filter(FrameElement.DEF==def_str, FrameElement.ELEMENT_TYPE_ID==element_type.ID).first()
                            if not frame_element:
                                frame_element = FrameElement(ID=uuid.uuid1(), CREATE_DATETIME=datetime.now(),
                                                             DEF=def_str, ELEMENT_TYPE_ID=element_type.ID)
                                db.session.add(frame_element)

                            frame_element_list.append(frame_element)
                            element_sample_list.append({"ID": uuid.uuid1(), "CREATE_DATETIME": datetime.now(), "LEMMA": lemma_str,
                                                        "SAMPLE": sample_str, "FRAME_ID": frame_info["ID"], "ELEMENT_ID": frame_element.ID})

            if skip_flag:
                frame = Frame(ID=frame_info["ID"], CREATE_DATETIME=datetime.now(), UPDATE_DATETIME=datetime.now(),
                              NAME=frame_info["NAME"], DEF=frame_info.get("DEF", ""), FRAME_TYPE=frame_info.get("FRAME_TYPE", ""),
                              PATTERN=frame_info.get("PATTERN", ""), IMAGE_URL="", SAMPLE=frame_info.get("SAMPLE", ""),
                              PARENT_ID=USER_NODE_ID)
                db.session.add(frame)
                for element in frame_element_list:
                    frame.frameElements.append(element)

                db.session.execute(
                    FrameElementSample.__table__.insert(), element_sample_list
                )
                db.session.commit()
                finish_list.append(tag_name)

        set_system_log(PATH="/api/preprocess/process!multi_verb_data", ACTION="preprocess",
                       MESSAGE="成功上传了Verb标注数据文件", LEVEL="INFO")

        return jsonify({'code': 0, 'msg': '上传成功', 'data': {"finish": finish_list, "skip": skip_list}})
    except:
        set_system_log(PATH="/api/preprocess/upload!preprocess", ACTION="preprocess",
                       MESSAGE="Verb数据标注文件上传失败", LEVEL="ERROR")
        return jsonify({'code': 1, 'msg': '上传失败', 'data': {"finish": finish_list}})
