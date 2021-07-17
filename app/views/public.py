import re
import json
from . import views
from flask import jsonify
from flask import render_template, request
from flask_login import login_required, logout_user
from datetime import datetime
from ..models import *
from ..setting import *
from ..utils import get_frame_tree_for_dropdown


@views.route('/home', methods=['GET'])
def home():
    info = get_system_info()
    return render_template("public/home.html", message=info)


@views.route('/publications', methods=['GET'])
def publications():
    info = get_system_info()
    return render_template("public/publications.html", message=info)


@views.route('/contributors', methods=['GET'])
def contributors():
    info = get_system_info()
    return render_template("public/contributors.html", message=info)


# ==================tagsets相关=======================
@views.route('/tagsets', methods=['GET'])
def targets():
    info_data = request.args.to_dict()
    element_type_list = []
    count = 0
    if info_data.get("TYPE", None):
        frame_element_types = FrameElementType.query.filter_by(TYPE=info_data.get("TYPE")).all()
        for element_type in frame_element_types:
            count += 1
            element_type_list.append(element_type.to_json())
    info = get_system_info()
    return render_template("public/tagsets/tagsets.html", message=info, elementTypes=element_type_list,
                           count=count, elementTypeName=info_data.get("TYPE", ""))


@views.route('/tagsetsList', methods=['GET'])
def tagsets_list():
    info_data = request.args.to_dict()
    element_type = FrameElementType.query.get(info_data.get("typeId"))
    frames_list, count, color_count, color_map = list(), 0, 0, dict()
    match_re = re.compile(r'[/](.*?)[]]', re.S)
    whole_re = re.compile(r'[\[](.*?)[]]', re.S)

    for element in element_type.elements:
        for frame in element.frames:
            frame_info = frame.to_json()
            frame_info["parent"] = []
            frame_info["color"] = TEXT_COLOR[count % len(TEXT_COLOR)]
            count += 1
            if frame.parent:
                if frame.parent.parent and frame.parent.parent.ID != ROOT_NODE_ID:
                    frame_info["parent"].append({"ID": frame.parent.parent.ID, "NAME": frame.parent.parent.NAME})
                if frame.parent.ID != ROOT_NODE_ID:
                    frame_info["parent"].append({"ID": frame.parent.ID, "NAME": frame.parent.NAME})
            frame_info["element"] = element.to_json()
            if element.elementSamples:
                for element_sample in element.elementSamples:
                    if element_sample.FRAME_ID == frame.ID:
                        frame_info["element"]["LEMMA"] = element_sample.LEMMA
                        frame_info["element"]["SAMPLE"] = element_sample.SAMPLE
                        break
            if not frame_info["element"].get("LEMMA", None):
                frame_info["element"]["LEMMA"] = ""
            if not frame_info["element"].get("SAMPLE", None):
                frame_info["element"]["SAMPLE"] = ""

            temp_list = re.findall(match_re, frame_info["element"]["SAMPLE"])
            whole_list = re.findall(whole_re, frame_info["element"]["SAMPLE"])
            for temp in temp_list:
                if not color_map.get(temp, None):
                    temp_element_type = FrameElementType.query.filter_by(NAME=temp).first()
                    if temp_element_type:
                        color_map[temp] = COLOR_MAP[temp_element_type.TYPE]
            for whole in whole_list:
                frame_info["element"]["SAMPLE"] = frame_info["element"]["SAMPLE"].replace(
                    whole, '<span style="background-color: ' + color_map.get(
                        whole.split("/")[1], "transparent") + ';">' + whole + '</span>')
            frames_list.append(frame_info)
    detail = element_type.to_json()
    detail["frames"] = frames_list
    info = get_system_info()
    return render_template("public/tagsets/tagsetsList.html", message=info, detail=detail)


# ==================frames相关=======================
@views.route('/frames', methods=['GET'])
def frames():
    top_frames_list = []
    root_frame = Frame.query.get(ROOT_NODE_ID)
    if root_frame.child:
        for top_frame in root_frame.child:
            frame_info = top_frame.to_json()
            frame_info["children"] = []
            frame_info["count"] = 0
            if top_frame.child:
                for second_frame in top_frame.child:
                    second_count = 0
                    if second_frame.verbs:
                        for _ in second_frame.verbs:
                            second_count += 1
                            frame_info["count"] += 1
                    frame_info["children"].append(
                        {"id": second_frame.ID, "name": second_frame.NAME, "count": second_count,
                         "parent": [{"id": second_frame.ID, "name": second_frame.NAME}]})
                    if second_frame.child:
                        for third_frame in second_frame.child:
                            third_count = 0
                            if third_frame.verbs:
                                for _ in third_frame.verbs:
                                    third_count += 1
                                    frame_info["count"] += 1
                            frame_info["children"].append(
                                {"id": third_frame.ID, "name": third_frame.NAME, "count": third_count,
                                 "parent": [{"id": second_frame.ID, "name": second_frame.NAME},
                                            {"id": third_frame.ID, "name": third_frame.NAME}]})
            top_frames_list.append(frame_info)

    info = get_system_info()
    return render_template("public/frames/frames.html", message=info, frames=top_frames_list)


@views.route('/framesList', methods=['GET'])
def frames_list():
    info_data = request.args.to_dict()
    frame = Frame.query.get(info_data.get("frameId"))
    frame_info, color_map = frame.to_json(), dict()
    match_re = re.compile(r'[/](.*?)[]]', re.S)
    whole_re = re.compile(r'[\[](.*?)[]]', re.S)

    frame_info["parent"] = list()
    frame_info["verbs"] = list()
    if frame.parent and frame.parent.ID != ROOT_NODE_ID:
        if frame.parent.parent and frame.parent.parent.ID != ROOT_NODE_ID:
            frame_info["parent"].append({"id": frame.parent.parent.ID, "name": frame.parent.parent.NAME})
        frame_info["parent"].append({"id": frame.parent.ID, "name": frame.parent.NAME})
    if frame.verbs:
        for verb in frame.verbs:
            frame_info["verbs"].append(verb.to_json())
    if frame.child:
        for second in frame.child:
            if second.verbs:
                for verb in second.verbs:
                    frame_info["verbs"].append(verb.to_json())
            if second.child:
                for third in second.child:
                    if third.verbs:
                        for verb in third.verbs:
                            frame_info["verbs"].append(verb.to_json())

    frame_info["coreElements"] = list()
    frame_info["nonElements"] = list()
    frame_info["markerElements"] = list()
    for element in frame.frameElements:
        element_json = element.to_json()
        if element.elementSamples:
            for element_sample in element.elementSamples:
                if element_sample.FRAME_ID == frame.ID:
                    element_json["LEMMA"] = element_sample.LEMMA
                    element_json["SAMPLE"] = element_sample.SAMPLE
                    break
        if not element_json.get("LEMMA", None):
            element_json["LEMMA"] = ""
        if not element_json.get("SAMPLE", None):
            element_json["SAMPLE"] = ""
        element_json["TYPE"] = element.type.NAME
        element_json["ELEMENT_TYPE"] = element.type.NAME
        if not color_map.get(element_json["TYPE"], None):
            color_map[element_json["TYPE"]] = COLOR_MAP[element.type.TYPE]
        if element.type.TYPE == "Core Frame Elements":
            frame_info["coreElements"].append(element_json)
        elif element.type.TYPE == "Non-core Frame Elements":
            frame_info["nonElements"].append(element_json)
        elif element.type.TYPE == "Construction Marker":
            frame_info["markerElements"].append(element_json)

    for i in range(len(frame_info["coreElements"])):
        frame_info["coreElements"][i]["color"] = COLOR_MAP["Core Frame Elements"]
        temp_list = re.findall(match_re, frame_info["coreElements"][i]["SAMPLE"])
        whole_list = re.findall(whole_re, frame_info["coreElements"][i]["SAMPLE"])
        for temp in temp_list:
            if not color_map.get(temp, None):
                temp_element_type = FrameElementType.query.filter_by(NAME=temp).first()
                if temp_element_type:
                    color_map[temp] = COLOR_MAP[temp_element_type.TYPE]
        for whole in whole_list:
            frame_info["coreElements"][i]["SAMPLE"] = frame_info["coreElements"][i]["SAMPLE"].replace(
                whole, '<span style="background-color: ' + color_map.get(
                    whole.split("/")[1], "transparent") + ';">' + whole + '</span>')
        frame_info["coreElements"][i]["TYPE"] = '<span style="background-color: ' + color_map.get(
            frame_info["coreElements"][i]["TYPE"], "transparent") + ';">' + frame_info["coreElements"][i]["TYPE"] + '</span>'

    for i in range(len(frame_info["nonElements"])):
        frame_info["nonElements"][i]["color"] = COLOR_MAP["Non-core Frame Elements"]

        temp_list = re.findall(match_re, frame_info["nonElements"][i]["SAMPLE"])
        whole_list = re.findall(whole_re, frame_info["nonElements"][i]["SAMPLE"])
        for temp in temp_list:
            if not color_map.get(temp, None):
                temp_element_type = FrameElementType.query.filter_by(NAME=temp).first()
                if temp_element_type:
                    color_map[temp] = COLOR_MAP[temp_element_type.TYPE]
        for whole in whole_list:
            frame_info["nonElements"][i]["SAMPLE"] = frame_info["nonElements"][i]["SAMPLE"].replace(
                whole, '<span style="background-color: ' + color_map.get(
                    whole.split("/")[1], "transparent") + ';">' + whole + '</span>')
        frame_info["nonElements"][i]["TYPE"] = '<span style="background-color: ' + color_map.get(
            frame_info["nonElements"][i]["TYPE"], "transparent") + ';">' + frame_info["nonElements"][i]["TYPE"] + '</span>'

    for i in range(len(frame_info["markerElements"])):
        frame_info["markerElements"][i]["color"] = COLOR_MAP["Construction Marker"]

        temp_list = re.findall(match_re, frame_info["markerElements"][i]["SAMPLE"])
        whole_list = re.findall(whole_re, frame_info["markerElements"][i]["SAMPLE"])
        for temp in temp_list:
            if not color_map.get(temp, None):
                temp_element_type = FrameElementType.query.filter_by(NAME=temp).first()
                if temp_element_type:
                    color_map[temp] = COLOR_MAP[temp_element_type.TYPE]
        for whole in whole_list:
            frame_info["markerElements"][i]["SAMPLE"] = frame_info["markerElements"][i]["SAMPLE"].replace(
                whole, '<span style="background-color: ' + color_map.get(
                    whole.split("/")[1], "transparent") + ';">' + whole + '</span>')

        frame_info["markerElements"][i]["TYPE"] = '<span style="background-color: ' + color_map.get(
            frame_info["markerElements"][i]["TYPE"], "transparent") + ';">' + frame_info["markerElements"][i]["TYPE"] + '</span>'

    info = get_system_info()
    return render_template("public/frames/framesList.html", message=info, frameInfo=frame_info)


# ==================Verbs相关=======================
@views.route('/verbs', methods=['GET'])
def verbs():
    top_frames_list = []
    root_frame = Frame.query.get(ROOT_NODE_ID)
    if root_frame.child:
        for top_frame in root_frame.child:
            frame_info = get_verb_with_frame_info(top_frame)
            top_frames_list.append(frame_info)

    info = get_system_info()
    return render_template("public/verbs/verbs.html", message=info, frames=top_frames_list)


@views.route('/verbsList', methods=['GET'])
def verbs_list():
    info_data = request.args.to_dict()
    verb = Verb.query.get(info_data.get("verbId"))
    verb_info = verb.to_json()
    verb_info["parent"] = list()
    if verb.frame and verb.frame.ID != ROOT_NODE_ID:
        if verb.frame.parent and verb.frame.parent.ID != ROOT_NODE_ID:
            if verb.frame.parent.parent and verb.frame.parent.parent.ID != ROOT_NODE_ID:
                verb_info["parent"].append({"id": verb.frame.parent.parent.ID, "name": verb.frame.parent.parent.NAME})
            verb_info["parent"].append({"id": verb.frame.parent.ID, "name": verb.frame.parent.NAME})
        verb_info["parent"].append({"id": verb.frame.ID, "name": verb.frame.NAME})

    info = get_system_info()
    return render_template("public/verbs/verbsList.html", message=info, verbInfo=verb_info)


# ==================Search相关=======================
@views.route('/searchContent', methods=['GET'])
def public_search():
    info_data = request.args.to_dict()
    info = get_system_info()
    frame_result, verb_result = list(), list()

    frame_all = Frame.query.filter(Frame.NAME.like("%" + info_data.get("search") + "%")).all()
    if frame_all:
        for frame in frame_all:
            frame_info = frame.to_json()
            frame_info["parent"] = list()
            if frame.parent and frame.parent.ID != ROOT_NODE_ID:
                if frame.parent and frame.parent.ID == USER_NODE_ID:
                    break
                if frame.parent.parent and frame.parent.parent.ID != ROOT_NODE_ID:
                    if frame.parent.parent and frame.parent.parent.ID == USER_NODE_ID:
                        break
                    frame_info["parent"].append({"ID": frame.parent.parent.ID, "NAME": frame.parent.parent.NAME})
                frame_info["parent"].append({"ID": frame.parent.ID, "NAME": frame.parent.NAME})
            frame_result.append(frame_info)

    verb_all = Verb.query.filter(Verb.NAME.like("%" + info_data.get("search") + "%")).all()
    if verb_all:
        for verb in verb_all:
            verb_info = verb.to_json()
            verb_info["parent"] = list()
            if verb.frame:
                if verb.frame.parent and verb.frame.parent.ID != ROOT_NODE_ID:
                    if verb.frame.parent.parent and verb.frame.parent.parent.ID != ROOT_NODE_ID:
                        verb_info["parent"].append(
                            {"ID": verb.frame.parent.parent.ID, "NAME": verb.frame.parent.parent.NAME})
                    verb_info["parent"].append({"ID": verb.frame.parent.ID, "NAME": verb.frame.parent.NAME})
                verb_info["parent"].append({"ID": verb.frame.ID, "NAME": verb.frame.NAME})
            verb_result.append(verb_info)

    return render_template("public/search.html", message=info, frames=frame_result, verbs=verb_result,
                           searchContent=info_data.get("search"))


# ==================compare相关=======================
@views.route('/compareVerb', methods=['GET'])
def compare_verb():
    info_data = request.args.to_dict()
    verb1 = Verb.query.get(info_data.get("verb1"))
    verb2 = Verb.query.get(info_data.get("verb2"))
    info = get_system_info()
    return render_template("public/verbs/compare.html", message=info,
                           verb1=verb1.to_json(), verb2=verb2.to_json())


@views.route('/compareLayer', methods=['GET'])
def compare_verb_layer():
    info_data = request.args.to_dict()
    verb = Verb.query.get(info_data.get("verbId"))
    top_frame = None
    if verb.frame and verb.frame.ID != ROOT_NODE_ID:
        top_frame = verb.frame
        if verb.frame.parent and verb.frame.parent.ID != ROOT_NODE_ID:
            top_frame = verb.frame.parent
            if verb.frame.parent.parent and verb.frame.parent.parent.ID != ROOT_NODE_ID:
                top_frame = verb.frame.parent.parent
    frame_info = get_verb_with_frame_info(top_frame)
    info = get_system_info()
    return render_template("public/verbs/compareLayer.html", message=info, frameInfo=frame_info, verbId=info_data.get("verbId"))


def get_system_info():
    system = System.query.first()
    return system.to_json()


def get_verb_with_frame_info(top_frame):
    frame_info = top_frame.to_json()
    frame_info["verbs"] = list()
    if top_frame.child:
        for second_frame in top_frame.child:
            if second_frame.child:
                for third_frame in second_frame.child:
                    if third_frame.verbs:
                        for verb in third_frame.verbs:
                            frame_info["verbs"].append({"ID": verb.ID, "NAME": verb.NAME,
                                                        "FREQUENCY": verb.FREQUENCY, "PARENT": [
                                    {"ID": top_frame.ID, "NAME": top_frame.NAME},
                                    {"ID": second_frame.ID, "NAME": second_frame.NAME},
                                    {"ID": third_frame.ID, "NAME": third_frame.NAME}]})
            if second_frame.verbs:
                for verb in second_frame.verbs:
                    frame_info["verbs"].append({"ID": verb.ID, "NAME": verb.NAME, "FREQUENCY": verb.FREQUENCY,
                                                "PARENT": [{"ID": top_frame.ID, "NAME": top_frame.NAME},
                                                           {"ID": second_frame.ID, "NAME": second_frame.NAME}]})
    if top_frame.verbs:
        for verb in top_frame.verbs:
            frame_info["verbs"].append({"ID": verb.ID, "NAME": verb.NAME, "FREQUENCY": verb.FREQUENCY,
                                        "PARENT": [{"ID": top_frame.ID, "NAME": top_frame.NAME}]})
    return frame_info
