import re
import json
import collections
from . import controllers
from .. import db
from ..models import *
from datetime import datetime
from flask import request
from flask import jsonify
from ..setting import *
from ..utils import get_frame_tree_for_dropdown, get_frame_tree_for_dropdown_with_verb

URL_PREFIX = "/public"


@controllers.route('{}/get!get_all_frame'.format(URL_PREFIX), methods=['GET'])
def get_all_frame_for_dropdown():
    info_data = request.args.to_dict()
    try:
        frames = Frame.query.get(ROOT_NODE_ID)
        frame = get_frame_tree_for_dropdown(frames, info_data.get("url") + "?" + info_data.get("param") + "=")

        return jsonify({'code': 0, 'msg': '', 'data': frame.get("child")})
    except:
        return jsonify({'code': 1, 'msg': '网络异常，加载失败', 'data': [{}]})


@controllers.route('{}/get!get_all_frame_for_compare'.format(URL_PREFIX), methods=['GET'])
def get_all_frame_for_compare_for_dropdown():
    info_data = request.args.to_dict()
    try:
        frames = Frame.query.get(ROOT_NODE_ID)
        frame = get_frame_tree_for_dropdown_with_verb(
            frames, info_data.get("url") + "?" + "verb1=" + info_data.get("verbId") + "&verb2=")

        return jsonify({'code': 0, 'msg': '', 'data': frame.get("child")})
    except:
        return jsonify({'code': 1, 'msg': '网络异常，加载失败', 'data': [{}]})


@controllers.route('{}/get!get_all_element_type_for_tree'.format(URL_PREFIX), methods=['GET'])
def get_all_element_type_for_tree():
    try:
        core_elements_types = FrameElementType.query.filter_by(TYPE="Core Frame Elements").all()
        non_core_elements_types = FrameElementType.query.filter_by(TYPE="Non-core Frame Elements").all()
        marker_elements_types = FrameElementType.query.filter_by(TYPE="Construction Marker").all()
        res_list = [{"id": "", "title": "Core Frame Elements", "parent": 1, "children": []},
                    {"id": "", "title": "Non-core Frame Elements", "parent": 1, "children": []},
                    {"id": "", "title": "Construction Marker", "parent": 1, "children": []}]
        for element in core_elements_types:
            res_list[0]["children"].append({"id": element.ID, "title": element.NAME})
        for element in non_core_elements_types:
            res_list[1]["children"].append({"id": element.ID, "title": element.NAME})
        for element in marker_elements_types:
            res_list[2]["children"].append({"id": element.ID, "title": element.NAME})
    except:
        return jsonify({'code': 1, 'msg': '网络异常，加载失败', 'data': [{}]})

    return jsonify({'code': 0, 'msg': '', 'data': res_list})


@controllers.route('{}/get!get_verb_info_for_details'.format(URL_PREFIX), methods=['GET'])
def get_verb_info_for_details():
    info_data = request.args.to_dict()
    verb = Verb.query.get(info_data.get("verbId"))
    verb_info = verb.to_json()
    verb_info["pattern_info"] = list()

    whole_re = re.compile(r'[\[](.*?)[]]', re.S)
    frame_def, frame_count, color_map = dict(), collections.Counter(), dict()
    color_count, total = 0, 0
    if verb.frame.frameElements:
        for element in verb.frame.frameElements:
            frame_def[element.type.NAME] = element.DEF

    if verb.patterns:
        for pattern in verb.patterns:
            pattern_info = pattern.to_json()
            pattern_info["samples"] = list()
            sample_size = 0
            temp_list = re.findall(whole_re, pattern_info["PATTERN"])

            for temp in temp_list:
                if not color_map.get(temp, None):
                    if frame_def.get(temp, None):
                        temp_element_type = FrameElementType.query.filter_by(NAME=temp).first()
                        if temp_element_type:
                            color_map[temp] = COLOR_MAP[temp_element_type.TYPE]
            if pattern.samples:
                for sample in pattern.samples:
                    whole_list = re.findall(whole_re, sample.CONTENT)
                    content = sample.CONTENT
                    sample_size += 1
                    for whole in whole_list:
                        content = content.replace(
                            whole, '<span style="background-color: ' + color_map.get(
                                whole.split("/")[1], "transparent") + ';">' + whole + '</span>')
                    pattern_info["samples"].append(content)
                total += sample_size
                pattern_info["total"] = sample_size
            for temp in temp_list:
                if pattern.samples:
                    frame_count[temp] += sample_size
                pattern_info["PATTERN"] = pattern_info["PATTERN"].replace(
                    temp, '<span style="background-color: ' + color_map.get(temp, "transparent") + ';">' + temp + '</span>')

            verb_info["pattern_info"].append(pattern_info)
    verb_info["total"] = total
    vote_verb_info = verb_info.copy()
    verb_info["pattern_info"] = sorted(verb_info["pattern_info"], key=lambda x: -x["total"])
    vote_verb_info["pattern_info"] = sorted(vote_verb_info["pattern_info"], key=lambda x: x["PATTERN"])

    frame_type = dict()
    frame_element_types = FrameElementType.query.filter_by(TYPE="Construction Marker").all()
    for element_type in frame_element_types:
        frame_type[element_type.NAME] = element_type.TYPE

    frame_info, marker_info = list(), list()
    for key, value in frame_count.items():
        if frame_type.get(key) != "Construction Marker":
            frame_info.append({"NAME": '<span style="background-color: ' + color_map.get(key, "transparent") + ';">' + key + '</span>',
                               "COUNT": value, "DEF": frame_def.get(key, " ")})
        else:
            marker_info.append(
                {"NAME": '<span style="background-color: ' + color_map.get(key, "transparent") + ';">' + key + '</span>',
                 "COUNT": value, "DEF": frame_def.get(key, " ")})

    frame_info = sorted(frame_info, key=lambda x: -x["COUNT"])
    return jsonify({'code': 0, 'msg': '', 'data': {"verb": verb_info, "frame": frame_info,
                                                   "marker": marker_info, "vote": vote_verb_info}})


@controllers.route('{}/get!get_verb_compare_detail'.format(URL_PREFIX), methods=['GET'])
def get_verb_compare_detail():
    info_data = request.args.to_dict()
    verb1 = Verb.query.get(info_data.get("verb1"))
    verb2 = Verb.query.get(info_data.get("verb2"))
    verb_info, color_map, color_count = dict(), dict(), 0
    verb_info["common"], verb_info["verb1"], verb_info["verb2"] = dict(), dict(), dict()
    whole_re = re.compile(r'[\[](.*?)[]]', re.S)
    match_re = re.compile(r'[/](.*?)[]]', re.S)

    verb1_patterns, verb2_patterns = set(), set()
    for pattern in verb1.patterns:
        verb1_patterns.add(pattern.PATTERN)
        temp_list = re.findall(whole_re, pattern.PATTERN)
        for temp in temp_list:
            if not color_map.get(temp, None):
                temp_element_type = FrameElementType.query.filter_by(NAME=temp).first()
                if temp_element_type:
                    color_map[temp] = COLOR_MAP[temp_element_type.TYPE]
    for pattern in verb2.patterns:
        verb2_patterns.add(pattern.PATTERN)
        temp_list = re.findall(whole_re, pattern.PATTERN)
        for temp in temp_list:
            if not color_map.get(temp, None):
                temp_element_type = FrameElementType.query.filter_by(NAME=temp).first()
                if temp_element_type:
                    color_map[temp] = COLOR_MAP[temp_element_type.TYPE]

    common_patterns = verb1_patterns.intersection(verb2_patterns)
    verb1_total, verb2_total = 0, 0
    for pattern in verb1.patterns:
        if pattern.PATTERN in common_patterns:
            flag_text = "common"
        else:
            flag_text = "verb1"
        if not verb_info[flag_text].get(pattern.PATTERN, None):
            verb_info[flag_text][pattern.PATTERN] = {"pattern": list(), "verb1Count": 0, "verb2Count": 0}
        for sample in pattern.samples:
            verb1_total += 1
            verb_info[flag_text][pattern.PATTERN]["verb1Count"] += 1
            sample_content = sample.CONTENT
            temp_list = re.findall(match_re, sample_content)
            for temp in temp_list:
                if not color_map.get(temp, None):
                    temp_element_type = FrameElementType.query.filter_by(NAME=temp).first()
                    if temp_element_type:
                        color_map[temp] = COLOR_MAP[temp_element_type.TYPE]
            whole_list = re.findall(whole_re, sample_content)
            for whole in whole_list:
                sample_content = sample_content.replace(
                    whole, '<span style="background-color: ' + color_map.get(
                        whole.split("/")[1], "transparent") + ';">' + whole + '</span>')
            verb_info[flag_text][pattern.PATTERN]["pattern"].append(sample_content)

    for pattern in verb2.patterns:
        if pattern.PATTERN in common_patterns:
            flag_text = "common"
        else:
            flag_text = "verb2"
        if not verb_info[flag_text].get(pattern.PATTERN, None):
            verb_info[flag_text][pattern.PATTERN] = {"pattern": list(), "verb1Count": 0, "verb2Count": 0}
        for sample in pattern.samples:
            verb2_total += 1
            verb_info[flag_text][pattern.PATTERN]["verb2Count"] += 1
            sample_content = sample.CONTENT
            temp_list = re.findall(match_re, sample_content)
            for temp in temp_list:
                if not color_map.get(temp, None):
                    temp_element_type = FrameElementType.query.filter_by(NAME=temp).first()
                    if temp_element_type:
                        color_map[temp] = COLOR_MAP[temp_element_type.TYPE]
            whole_list = re.findall(whole_re, sample_content)
            for whole in whole_list:
                sample_content = sample_content.replace(
                    whole, '<span style="background-color: ' + color_map.get(
                        whole.split("/")[1], "transparent") + ';">' + whole + '</span>')
            verb_info[flag_text][pattern.PATTERN]["pattern"].append(sample_content)

    common_info = dict()
    for key, _ in verb_info["common"].items():
        whole_list = re.findall(whole_re, key)
        temp_content = key
        for whole in whole_list:
            temp_content = temp_content.replace(
                whole, '<span style="background-color: ' + color_map.get(whole, "transparent") + ';">' + whole + '</span>')
        common_info[temp_content] = verb_info["common"][key]

    verb1_info = dict()
    for key, _ in verb_info["verb1"].items():
        whole_list = re.findall(whole_re, key)
        temp_content = key
        for whole in whole_list:
            temp_content = temp_content.replace(
                whole, '<span style="background-color: ' + color_map.get(whole, "transparent") + ';">' + whole + '</span>')
        verb1_info[temp_content] = verb_info["verb1"][key]

    verb2_info = dict()
    for key, _ in verb_info["verb2"].items():
        whole_list = re.findall(whole_re, key)
        temp_content = key
        for whole in whole_list:
            temp_content = temp_content.replace(
                whole, '<span style="background-color: ' + color_map.get(whole, "transparent") + ';">' + whole + '</span>')
        verb2_info[temp_content] = verb_info["verb2"][key]

    return jsonify({'code': 0, 'msg': '', 'data': {"common": common_info, "verb1": verb1_info, "verb2": verb2_info,
                                                   "verb1Total": verb1_total, "verb2Total": verb2_total,
                                                   "verb1Info": verb1.to_json(), "verb2Info": verb2.to_json()}})


@controllers.route('{}/search!searchVerbContent'.format(URL_PREFIX), methods=['POST'])
def public_search_verb():
    info_data = json.loads(request.get_data())
    verb_result = list()

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

    return jsonify({'code': 0, 'msg': '', 'data': verb_result})
