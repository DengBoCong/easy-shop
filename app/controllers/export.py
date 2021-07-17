import os
import time
import json
import uuid
import shutil
from datetime import datetime
from . import controllers
from .. import db
from ..models import *
from flask import request, send_file
from flask import jsonify
from flask_login import login_required, current_user
from ..utils import make_zip
from ..setting import TEMP_FILE_DIR, FILE_SUFFIX, FRAME_FILE_SUFFIX
from werkzeug.utils import secure_filename

URL_PREFIX = "/export"


# ==============================Verb相关================================
@controllers.route('{}/export!verb_info'.format(URL_PREFIX), methods=['GET'])
@login_required
def export_verb_info():
    info_data = request.args.to_dict()
    temp_dir = time.strftime("%Y/%m/", time.localtime()) + str(uuid.uuid1()) + "/" + str(uuid.uuid1()) + "/"
    base_path = os.path.abspath(os.path.join(os.getcwd())).replace("\\", "/") + TEMP_FILE_DIR
    download_path = os.path.join(base_path, temp_dir)
    is_exist = os.path.exists(download_path)

    verb_info = Verb.query.get(info_data.get("verbId"))
    if not is_exist:
        os.makedirs(download_path, 0o777)

    download_path = download_path + verb_info.NAME + FILE_SUFFIX

    export_single_verb_info(verb_info, download_path)

    return send_file(download_path, mimetype='text/csv', attachment_filename=verb_info.NAME + FILE_SUFFIX,
                     as_attachment=True)


# ==============================Frame相关================================
@controllers.route('{}/export!frame_info'.format(URL_PREFIX), methods=['GET'])
@login_required
def export_frame_info():
    info_data = request.args.to_dict()
    temp_dir = time.strftime("%Y/%m/", time.localtime()) + str(uuid.uuid1()) + "/"
    base_path = os.path.abspath(os.path.join(os.getcwd())).replace("\\", "/") + TEMP_FILE_DIR
    download_path = os.path.join(base_path, temp_dir)
    is_exist = os.path.exists(download_path)

    frame_info = Frame.query.get(info_data.get("frameId"))
    if not is_exist:
        os.makedirs(download_path, 0o777)

    download_path = download_path + frame_info.NAME + FRAME_FILE_SUFFIX
    export_single_frame_info(frame_info, download_path)

    return send_file(download_path, mimetype='text/csv', attachment_filename=frame_info.NAME + FRAME_FILE_SUFFIX,
                     as_attachment=True)


@controllers.route('{}/export!frame_with_sub_info'.format(URL_PREFIX), methods=['GET'])
@login_required
def export_frame_with_sub_info():
    info_data = request.args.to_dict()
    frame_info = Frame.query.get(info_data.get("frameId"))
    temp_dir = time.strftime("%Y/%m/", time.localtime()) + str(uuid.uuid1()) + "/" + frame_info.NAME
    base_path = os.path.abspath(os.path.join(os.getcwd())).replace("\\", "/") + TEMP_FILE_DIR
    download_path = os.path.join(base_path, temp_dir + "/")
    final_zip_path = os.path.join(base_path, temp_dir + ".zip")

    if not os.path.exists(download_path):
        os.makedirs(download_path, 0o777)

    first_path = download_path + frame_info.NAME + FRAME_FILE_SUFFIX
    export_single_frame_info(frame_info, first_path)
    if frame_info.child:
        for second_frame in frame_info.child:
            second_path = download_path + second_frame.NAME + "/"
            if not os.path.exists(second_path):
                os.makedirs(second_path, 0o777)
            export_single_frame_info(second_frame, second_path + second_frame.NAME + FRAME_FILE_SUFFIX)
            if second_frame.child:
                for third_frame in second_frame.child:
                    third_path = second_path + third_frame.NAME + "/"
                    if not os.path.exists(third_path):
                        os.makedirs(third_path, 0o777)
                    export_single_frame_info(third_frame, third_path + third_frame.NAME + FRAME_FILE_SUFFIX)
                    if third_frame.verbs:
                        for verb in third_frame.verbs:
                            export_single_verb_info(verb, third_path + verb.NAME + FILE_SUFFIX)
            if second_frame.verbs:
                for verb in second_frame.verbs:
                    export_single_verb_info(verb, second_path + verb.NAME + FILE_SUFFIX)
    if frame_info.verbs:
        for verb in frame_info.verbs:
            export_single_verb_info(verb, download_path + verb.NAME + FILE_SUFFIX)

    make_zip(source_dir=download_path, output_filename=final_zip_path)

    return send_file(final_zip_path, mimetype='text/csv', attachment_filename=frame_info.NAME + ".zip",
                     as_attachment=True)


def export_single_verb_info(verb_info, download_path):
    with open(download_path, "a", encoding="utf-8") as file:
        file.write("## pinyin: {}\n## frequency: {}\n\n".format(verb_info.PIN_YIN, verb_info.FREQUENCY))
        for pattern in verb_info.patterns:
            if pattern.CONSTRUCTION:
                file.write("%%CONSTRUCTION: {}\n".format(pattern.CONSTRUCTION))
            file.write("%%PATTERN: {}\n".format(pattern.PATTERN))
            for sample in pattern.samples:
                file.write("{}\n".format(sample.CONTENT))
            file.write("\n")


def export_single_frame_info(frame_info, download_path):
    with open(download_path, "w", encoding="utf-8") as file:
        file.write("Frame: {}\nDef.: {}\nFrame type: {} frame\n\nVerb: {}\n".format(frame_info.NAME,
                                                                                    frame_info.DEF,
                                                                                    frame_info.FRAME_TYPE,
                                                                                    frame_info.NAME))
        lemma_list, sub_frame_list = list(), list()
        if frame_info.verbs:
            for verb in frame_info.verbs:
                lemma_list.append(verb.NAME)
        if frame_info.child:
            for second in frame_info.child:
                sub_frame_list.append(second.NAME)
                if second.verbs:
                    for verb in second.verbs:
                        lemma_list.append(verb.NAME)
                if second.child:
                    for third in second.child:
                        sub_frame_list.append(third.NAME)
                        if third.verbs:
                            for verb in third.verbs:
                                lemma_list.append(verb.NAME)
        file.write("Lemma: {}\n".format(",".join(lemma_list)))
        file.write("Subframes: [Basic frame] {}\n".format(",".join(sub_frame_list)))
        file.write("Pattern: {}\n".format(frame_info.PATTERN))
        file.write("Sample: {}\n\n".format(frame_info.SAMPLE))

        core_elements, non_core_elements, marker = list(), list(), list()
        for element in frame_info.frameElements:
            element_info = element.to_json()
            element_info["TYPE"] = element.type.NAME
            if element.elementSamples:
                for element_sample in element.elementSamples:
                    if element_sample.FRAME_ID == frame_info.ID:
                        element_info["LEMMA"] = element_sample.LEMMA
                        element_info["SAMPLE"] = element_sample.SAMPLE
                        break
            if element.type.TYPE == "Core Frame Elements":
                core_elements.append(element_info)
            elif element.type.TYPE == "Non-core Frame Elements":
                non_core_elements.append(element_info)
            elif element.type.TYPE == "Construction Marker":
                marker.append(element_info)

        file.write("[Core]\n\n")
        for core in core_elements:
            file.write("Tag: {}\nDef.: {}\nLemma: {}\nSample: {}\n\n".format(core.get("TYPE", "None"), core["DEF"],
                                                                             core["LEMMA"], core["SAMPLE"]))
        file.write("[Non-core]\n\n")
        for core in non_core_elements:
            file.write("Tag: {}\nDef.: {}\nLemma: {}\nSample: {}\n\n".format(core.get("TYPE", "None"), core["DEF"],
                                                                             core["LEMMA"], core["SAMPLE"]))
        file.write("[*Construction Marker]\n\n")
        for core in marker:
            file.write("Tag: {}\nDef.: {}\nLemma: {}\nSample: {}\n\n".format(core.get("TYPE", "None"), core["DEF"],
                                                                             core["LEMMA"], core["SAMPLE"]))
