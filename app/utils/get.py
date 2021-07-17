import psutil
from ..models import *
from ..setting import USER_NODE_ID


def get_system_info():
    system = System.query.first()
    return system.to_json()


def get_all_role():
    roles = Role.query.all()
    return roles


def get_home_by_type_not_api(type):
    page = HomePage.query.filter_by(TYPE=type).first()
    return page


def get_cpu_info():
    """
    mem_total: 总内存
    mem_free: 空闲内存
    mem_used: Linux: total - free,已使用内存
    mem_percent: 已使用内存占比
    cpu: 各个CPU使用占比
    :return:
    """
    mem = psutil.virtual_memory()
    mem_total = mem.total
    mem_free = mem.free
    mem_percent = mem.percent
    mem_used = mem.used
    cpu = psutil.cpu_percent(percpu=True)

    return mem_total, mem_free, mem_used, mem_percent, cpu


def get_frame_tree(frames, if_with_verb=False, layer=0, spread_id=""):
    spread = True if spread_id == frames.ID else False
    child_spread = False
    frame = {"id": frames.ID, "title": frames.NAME, "children": [],
             "if_third": 1 if layer == 3 else 0, "if_verb": 0, "has_verb": 0, "spread": spread}
    if layer < 3:
        for first_root in frames.child:
            temp_frame, temp_child_spread = get_frame_tree(first_root, if_with_verb, layer + 1, spread_id)
            child_spread = (child_spread or temp_child_spread)
            frame["children"].append(temp_frame)
    # if if_with_verb and frames.verbs:
    for verb in frames.verbs:
        frame["has_verb"] = 1
        if spread_id == verb.ID:
            spread = True
        frame["children"].append(
            {"id": verb.ID, "title": verb.NAME, "children": [], "has_verb": 0,
             "if_third": 1 if layer == 3 else 0, "if_verb": 1, "spread": spread})
    frame["spread"] = (spread or child_spread)
    return frame, (spread or child_spread)


# def get_frame_tree(frames, if_with_verb=False, layer=0, spread_id=""):
#     frame = {"id": frames.ID, "title": frames.NAME, "children": [],
#              "if_third": 1 if layer == 3 else 0, "if_verb": 0, "has_verb": 0,
#              "spread": True if spread_id == frames.ID else False}
#     for first_root in frames.child:
#         first = {"id": first_root.ID, "title": first_root.NAME, "if_third": 1 if layer + 1 == 3 else 0,
#                  "if_verb": 0, "children": [], "has_verb": 0, "spread": True if spread_id == first_root.ID else False}
#         if first_root.child:
#             for second_root in first_root.child:
#                 second = {"id": second_root.ID, "title": second_root.NAME,
#                           "if_third": 1 if layer + 2 == 3 else 0, "if_verb": 0, "children": [], "has_verb": 0,
#                           "spread": True if spread_id == second_root.ID else False}
#                 if second_root.child:
#                     for third_root in second_root.child:
#                         third = {"id": third_root.ID, "title": third_root.NAME,
#                                  "if_third": 1 if layer + 3 == 3 else 0, "if_verb": 0, "children": [],
#                                  "has_verb": 0, "spread": True if spread_id == third_root.ID else False}
#                         if if_with_verb and third_root.verbs:
#                             third["has_verb"] = 1
#                             for verb in third_root.verbs:
#                                 third["children"].append(
#                                     {"id": verb.ID, "title": verb.NAME, "children": [], "has_verb": 0,
#                                      "if_third": 1 if layer + 3 == 3 else 0, "if_verb": 1,
#                                      "spread": True if spread_id == verb.ID else False})
#                         second["children"].append(third)
#                 elif if_with_verb and second_root.verbs:
#                     second["has_verb"] = 1
#                     for verb in second_root.verbs:
#                         second["children"].append({"id": verb.ID, "title": verb.NAME, "children": [], "has_verb": 0,
#                                                    "if_third": 1 if layer + 2 == 3 else 0, "if_verb": 1,
#                                                    "spread": True if spread_id == verb.ID else False})
#                 first["children"].append(second)
#         elif if_with_verb and first_root.verbs:
#             first["has_verb"] = 1
#             for verb in first_root.verbs:
#                 first["children"].append(
#                     {"id": verb.ID, "title": verb.NAME, "if_third": 1 if layer + 1 == 3 else 0,
#                      "if_verb": 1, "children": [], "has_verb": 0,
#                      "spread": True if spread_id == verb.ID else False})
#         frame["children"].append(first)
#
#     return frame


def get_frame_tree_for_dropdown(frames, url):
    frame = {"id": frames.ID, "title": frames.NAME, "child": [], "href": url + frames.ID}
    for first_root in frames.child:
        first = {"id": first_root.ID, "title": first_root.NAME, "child": [], "href": url + first_root.ID}
        if first_root.child:
            for second_root in first_root.child:
                second = {"id": second_root.ID, "title": second_root.NAME, "child": [], "href": url + second_root.ID}
                if second_root.child:
                    for third_root in second_root.child:
                        third = {"id": third_root.ID, "title": third_root.NAME, "child": [],
                                 "href": url + third_root.ID}
                        second["child"].append(third)
                first["child"].append(second)
        frame["child"].append(first)

    return frame


def get_frame_tree_for_dropdown_with_verb(frames, url):
    frame = {"id": frames.ID, "title": frames.NAME, "child": [], "href": "javascript:;"}
    for first_root in frames.child:
        first = {"id": first_root.ID, "title": first_root.NAME, "child": [], "href": "javascript:;"}
        if first_root.child:
            for second_root in first_root.child:
                second = {"id": second_root.ID, "title": second_root.NAME, "child": [], "href": "javascript:;"}
                if second_root.child:
                    for third_root in second_root.child:
                        third = {"id": third_root.ID, "title": third_root.NAME, "child": [],
                                 "href": "javascript:;"}
                        if third_root.verbs:
                            for verb in third_root.verbs:
                                third["child"].append({"id": verb.ID, "title": verb.NAME,
                                                       "child": [], "href": url + verb.ID})
                        second["child"].append(third)
                if second_root.verbs:
                    for verb in second_root.verbs:
                        second["child"].append({"id": verb.ID, "title": verb.NAME,
                                                "child": [], "href": url + verb.ID})
                first["child"].append(second)
        if first_root.verbs:
            for verb in first_root.verbs:
                first["child"].append({"id": verb.ID, "title": verb.NAME,
                                       "child": [], "href": url + verb.ID})
        frame["child"].append(first)

    return frame


def get_frame_tree_for_review(frames, if_with_verb=False, layer=0, spread_id=""):
    spread = True if spread_id == frames.ID else False
    child_spread = False
    frame = {"id": frames.ID, "title": frames.NAME, "children": [], "spread": spread,
             "if_third": 1 if layer == 3 else 0, "if_verb": 0, "has_verb": 0, "has_frame": 0}
    if layer < 3:
        for first_root in frames.child:
            frame["has_frame"] = 1
            temp_frame, temp_child_spread = get_frame_tree_for_review(first_root, if_with_verb, layer + 1, spread_id)
            child_spread = (child_spread or temp_child_spread)
            frame["children"].append(temp_frame)
    for verb in frames.verbs:
        frame["has_verb"] = 1
        if spread_id == verb.ID:
            spread = True
        user_name = ""
        if verb.user:
            user_name = verb.user.NAME
        title = verb.NAME
        if verb.IF_FINISH == "1":
            title += "({}标注完成)".format(user_name)
        elif verb.IF_FINISH == "2":
            title += "({}已驳回)".format(user_name)
        else:
            title += user_name if user_name == "" else "({})".format(user_name)
        frame["children"].append({"id": verb.ID, "title": title, "has_frame": 0, "spread": spread,
                                  "if_third": 1 if layer == 3 else 0, "if_verb": 1, "children": [], "has_verb": 0})
    frame["spread"] = (spread or child_spread)
    return frame, (spread or child_spread)


# def get_frame_tree_for_review(frames, if_with_verb=False):
#     frame = {"id": frames.ID, "title": frames.NAME, "children": [],
#              "if_third": 0, "if_verb": 0, "has_verb": 0, "has_frame": 0}
#     for first_root in frames.child:
#         frame["has_frame"] = 1
#         first = {"id": first_root.ID, "if_third": 0, "if_verb": 0,
#                  "children": [], "has_verb": 0, "title": first_root.NAME, "has_frame": 0}
#         if first_root.child:
#             for second_root in first_root.child:
#                 first["has_frame"] = 1
#                 second = {"id": second_root.ID, "if_third": 0, "if_verb": 0,
#                           "children": [], "has_verb": 0, "title": second_root.NAME, "has_frame": 0}
#                 if second_root.child:
#                     for third_root in second_root.child:
#                         second["has_frame"] = 1
#                         third = {"id": third_root.ID, "if_third": 1, "if_verb": 0,
#                                  "children": [], "has_verb": 0, "title": third_root.NAME, "has_frame": 0}
#                         if if_with_verb and third_root.verbs:
#                             for verb in third_root.verbs:
#                                 third["has_verb"] = 1
#                                 user_name = ""
#                                 if verb.user:
#                                     user_name = verb.user.NAME
#                                 title = verb.NAME
#                                 if verb.IF_FINISH == "1":
#                                     title += "({}标注完成)".format(user_name)
#                                 elif verb.IF_FINISH == "2":
#                                     title += "({}已驳回)".format(user_name)
#                                 else:
#                                     title += "({})".format(user_name)
#                                 third["children"].append({"id": verb.ID, "title": title, "has_frame": 0,
#                                                           "if_third": 1, "if_verb": 1, "children": [], "has_verb": 0})
#                         second["children"].append(third)
#                 elif if_with_verb and second_root.verbs:
#                     for verb in second_root.verbs:
#                         second["has_verb"] = 1
#                         user_name = ""
#                         if verb.user:
#                             user_name = verb.user.NAME
#                         title = verb.NAME
#                         if verb.IF_FINISH == "1":
#                             title += "({}标注完成)".format(user_name)
#                         elif verb.IF_FINISH == "2":
#                             title += "({}已驳回)".format(user_name)
#                         else:
#                             title += "({})".format(user_name)
#                         second["children"].append({"id": verb.ID, "title": title, "has_frame": 0,
#                                                    "if_third": 0, "if_verb": 1, "children": [], "has_verb": 0})
#                 first["children"].append(second)
#         elif if_with_verb and first_root.verbs:
#             for verb in first_root.verbs:
#                 first["has_verb"] = 1
#                 user_name = ""
#                 if verb.user:
#                     user_name = verb.user.NAME
#                 title = verb.NAME
#                 if verb.IF_FINISH == "1":
#                     title += "({}标注完成)".format(user_name)
#                 elif verb.IF_FINISH == "2":
#                     title += "({}已驳回)".format(user_name)
#                 else:
#                     title += "({})".format(user_name)
#                 first["children"].append(
#                     {"id": verb.ID, "title": title, "if_third": 0, "if_verb": 1,
#                      "children": [], "has_verb": 0, "has_frame": 0})
#         frame["children"].append(first)
#
#     return frame


def get_frame_not_third(frames):
    frame = [{"ID": frames.ID, "NAME": frames.NAME}]
    for first_root in frames.child:
        frame.append({"ID": first_root.ID, "NAME": first_root.NAME})
        if first_root.child:
            for second_root in first_root.child:
                frame.append({"ID": second_root.ID, "NAME": second_root.NAME})

    return frame


def get_frame_with_third(frames):
    frame = [{"ID": frames.ID, "NAME": frames.NAME}]
    for first_root in frames.child:
        frame.append({"ID": first_root.ID, "NAME": first_root.NAME})
        if first_root.child:
            for second_root in first_root.child:
                frame.append({"ID": second_root.ID, "NAME": second_root.NAME})
                if second_root.child:
                    for third_root in second_root.child:
                        frame.append({"ID": third_root.ID, "NAME": third_root.NAME})

    return frame


def get_frame_with_third_where_not_frame(frames):
    frame = list()
    if not frames.child:
        frame = [{"ID": frames.ID, "NAME": frames.NAME}]
    for first_root in frames.child:
        if not first_root.child:
            frame.append({"ID": first_root.ID, "NAME": first_root.NAME})
        else:
            for second_root in first_root.child:
                if not second_root.child:
                    frame.append({"ID": second_root.ID, "NAME": second_root.NAME})
                else:
                    for third_root in second_root.child:
                        frame.append({"ID": third_root.ID, "NAME": third_root.NAME})

    return frame


def get_frame_not_third_where_not_verb(frames):
    frame = list()
    first_flag = True
    for _ in frames.verbs:
        first_flag = False
        break
    if first_flag:
        frame = [{"ID": frames.ID, "NAME": frames.NAME}]
    for first_root in frames.child:
        second_flag = True
        for _ in first_root.verbs:
            second_flag = False
            break
        if second_flag:
            frame.append({"ID": first_root.ID, "NAME": first_root.NAME})
        for second_root in first_root.child:
            third_flag = True
            for _ in second_root.verbs:
                third_flag = False
                break
            if third_flag:
                frame.append({"ID": second_root.ID, "NAME": second_root.NAME})

    return frame


def get_user_frame_tree(frames, if_with_verb=True):
    frame_data = list()
    if frames:
        for frame in frames:
            count = 1
            if frame.parent and frame.parent.ID != USER_NODE_ID:
                count = 2
                if frame.parent.parent and frame.parent.parent.ID != USER_NODE_ID:
                    count = 3
            frame_info = get_frame_tree(frames=frame, if_with_verb=if_with_verb, layer=count)
            frame_data.append(frame_info)
    return frame_data
