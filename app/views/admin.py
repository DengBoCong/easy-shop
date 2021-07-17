from . import views
from flask import jsonify
from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user
from datetime import datetime
from ..services.auth import permission_required
from ..utils.get import *


@views.route('/', methods=['GET', 'POST'])
@login_required
@permission_required("/index")
def index_top():
    info = get_system_info()
    user = User.query.get(current_user.ID)
    privilege_list = list()
    if user:
        for privilege_info in user.roles.privilege:
            privilege_list.append(privilege_info.TARGET)
    return render_template("index.html", message=info, privilege=privilege_list)


@views.route('/index', methods=['GET', 'POST'])
@login_required
@permission_required("/index")
def index():
    info = get_system_info()
    user = User.query.get(current_user.ID)
    privilege_list = list()
    if user:
        for privilege_info in user.roles.privilege:
            privilege_list.append(privilege_info.TARGET)
    return render_template("index.html", message=info, privilege=privilege_list)


@views.route('/admin', methods=['GET', 'POST'])
@permission_required("/admin")
@login_required
def admin():
    links = Link.query.all()
    links_list = []
    for link in links:
        user_json = link.to_json()
        links_list.append(user_json)

    mem_total, mem_free, _, mem_percent, cpu = get_cpu_info()

    info = get_system_info()
    info["links"] = links_list
    info["links_count"] = len(links_list)
    info["mem_total"] = mem_total
    info["mem_free"] = mem_free
    info["mem_percent"] = mem_percent
    info["cpu"] = cpu
    info["cpu_count"] = len(cpu)

    notices = Notice.query.filter_by(IF_TOP=True).all()

    return render_template("admin.html", message=info, all=round(mem_free / mem_total, 4) * 100, notices=notices)


# ==================User相关=======================
@views.route('/login', methods=['GET', 'POST'])
def login():
    info = get_system_info()
    return render_template("user/login.html", message=info)


@views.route('/forget', methods=['GET', 'POST'])
def forget():
    info = get_system_info()
    return render_template("user/forget.html", message=info)


@views.route('/personInfo', methods=['GET', 'POST'])
@permission_required("/personInfo")
@login_required
def person_info():
    return render_template("user/info.html")


@views.route('/personPwd', methods=['GET', 'POST'])
@permission_required("/personPwd")
@login_required
def person_pwd():
    return render_template("user/password.html")


@views.route('/userSystem', methods=['GET', 'POST'])
@permission_required("/userSystem")
@login_required
def user_system():
    roles = get_all_role()
    return render_template("user/userList.html", roles=roles)


@views.route('/userForm', methods=['GET', 'POST'])
@permission_required("/userForm")
@login_required
def user_from():
    return render_template("user/userForm.html")


# ==================Role相关=======================
@views.route('/role', methods=['GET', 'POST'])
@permission_required("/role")
@login_required
def role():
    return render_template("role/role.html")


@views.route('/roleForm', methods=['GET', 'POST'])
@permission_required("/roleForm")
@login_required
def role_form():
    info_data = request.args.to_dict()
    return render_template("role/roleForm.html", roleId=info_data.get("roleId"))


@views.route('/roleAddForm', methods=['GET', 'POST'])
@permission_required("/roleAddForm")
@login_required
def role_add_form():
    return render_template("role/roleAddForm.html")


@views.route('/privilege', methods=['GET', 'POST'])
@permission_required("/privilege")
@login_required
def privilege():
    return render_template("role/privilege.html")


@views.route('/privilegeForm', methods=['GET', 'POST'])
@permission_required("/privilegeForm")
@login_required
def privilege_form():
    return render_template("role/privilegeForm.html")


# ==================Message相关=======================
@views.route('/message', methods=['GET', 'POST'])
@permission_required("/message")
@login_required
def message():
    return render_template("person/message/index.html")


@views.route('/message=<detail_id>', methods=['GET', 'POST'])
@permission_required("/message")
@login_required
def message_detail(detail_id):
    info = get_system_info()
    info["title"] = "中文动词语义网"
    info[
        "content"] = "一直以来，layui 秉承无偿开源的初心，虔诚致力于服务各层次前后端 Web 开发者，在商业横飞的当今时代，这一信念从未动摇。即便身单力薄，仍然重拾决心，埋头造轮，以尽可能地填补产品本身的缺口。在过去的一段的时间，我一直在寻求持久之道，已维持你眼前所见的一切。而 layuiAdmin 是我们尝试解决的手段之一。我相信真正有爱于 layui 生态的你，定然不会错过这一拥抱吧。"
    info["time"] = datetime.now()
    return render_template("person/message/detail.html", message=info)


# ==================Search相关=======================
@views.route('/search', methods=['GET', 'POST'])
@permission_required("/search")
@login_required
def search():
    return render_template("system/search.html")


# ==================Website相关=======================
@views.route('/systemWebsite', methods=['GET', 'POST'])
@permission_required("/systemWebsite")
@login_required
def system_website():
    info = get_system_info()
    return render_template("system/website.html", message=info)


@views.route('/quickLink', methods=['GET', 'POST'])
@permission_required("/quickLink")
@login_required
def quick_kink():
    return render_template("system/quickLink.html")


@views.route('/linkForm', methods=['GET', 'POST'])
@permission_required("/linkForm")
@login_required
def link_from():
    return render_template("system/linkForm.html")


@views.route('/contacts', methods=['GET', 'POST'])
@permission_required("/contacts")
@login_required
def contacts():
    return render_template("system/contacts.html")


@views.route('/editHome', methods=['GET', 'POST'])
@permission_required("/editHome")
@login_required
def edit_home():
    return render_template("edit/editHome.html")


@views.route('/editPublications', methods=['GET', 'POST'])
@permission_required("/editPublications")
@login_required
def edit_publications():
    return render_template("edit/editPublications.html")


@views.route('/editContributors', methods=['GET', 'POST'])
@permission_required("/editContributors")
@login_required
def edit_contributors():
    return render_template("edit/editContributors.html")


# ==================log相关=======================
@views.route('/systemLog', methods=['GET', 'POST'])
@permission_required("/systemLog")
@login_required
def system_log():
    return render_template("log/systemLog.html")


@views.route('/dataLog', methods=['GET', 'POST'])
@permission_required("/dataLog")
@login_required
def data_log():
    return render_template("log/dataLog.html")


# ==================数据相关=======================
@views.route('/frameManage', methods=['GET', 'POST'])
@permission_required("/frameManage")
@login_required
def frame_manage():
    return render_template("data/frame/frameManage.html")


@views.route('/frameDetails', methods=['GET', 'POST'])
@permission_required("/frameDetails")
@login_required
def frame_details():
    info_data = request.args.to_dict()
    frame = Frame.query.get(info_data.get("frame"))
    core_elements, non_core_elements, marker = list(), list(), list()
    for element in frame.frameElements:
        element_info = element.to_json()
        if element.elementSamples:
            for element_sample in element.elementSamples:
                if element_sample.FRAME_ID == frame.ID:
                    element_info["LEMMA"] = element_sample.LEMMA
                    element_info["SAMPLE"] = element_sample.SAMPLE
                    element_info["SAMPLE_ID"] = element_sample.ID
                    break
        element_info["NAME"] = element.type.NAME
        if element.type.TYPE == "Core Frame Elements":
            core_elements.append(element_info)
        elif element.type.TYPE == "Non-core Frame Elements":
            non_core_elements.append(element_info)
        elif element.type.TYPE == "Construction Marker":
            marker.append(element_info)
    return render_template("data/frame/frameDetails.html", frame=frame, core_elements=core_elements,
                           non_core_elements=non_core_elements, marker=marker)


@views.route('/frameAddElementPage', methods=['GET', 'POST'])
@permission_required("/frameAddElementPage")
@login_required
def frame_add_element():
    info_data = request.args.to_dict()
    return render_template("data/frame/frameAddElementPage.html",
                           info={"frameId": info_data.get("frameId"), "type": info_data.get("type")})


@views.route('/frameEditElementPage', methods=['GET', 'POST'])
@permission_required("/frameEditElementPage")
@login_required
def frame_edit_element():
    info_data = request.args.to_dict()
    return render_template("data/frame/frameEditElementPage.html", elementId=info_data.get("elementId"))


# ==================Element相关=======================
@views.route('/elementTypeManage', methods=['GET', 'POST'])
@permission_required("/elementTypeManage")
@login_required
def element_type_manage():
    return render_template("data/element/elementManage.html")


@views.route('/elementTypeManageForm', methods=['GET', 'POST'])
@permission_required("/elementTypeManageForm")
@login_required
def element_type_manage_form():
    return render_template("data/element/elementManageForm.html")


@views.route('/elementFrameDetails', methods=['GET', 'POST'])
@permission_required("/elementFrameDetails")
@login_required
def element_frame_details():
    info_data = request.args.to_dict()
    element_type = FrameElementType.query.get(info_data.get("elementTypeId"))
    relation_list, element_list = list(), list()
    if element_type.elements:
        for element in element_type.elements:
            element_list.append(element.to_json())
            if element.frames:
                for frame in element.frames:
                    relation_list.append({"frame": frame.NAME, "def": element.DEF})
    return render_template("data/element/elementFrameDetails.html", relation=relation_list, elementList=element_list)


# ==================Verb相关=======================
@views.route('/verbManage', methods=['GET', 'POST'])
@permission_required("/verbManage")
@login_required
def verb_manage():
    return render_template("data/verb/verbManage.html")


@views.route('/verbDetails', methods=['GET', 'POST'])
@permission_required("/verbDetails")
@login_required
def verb_details():
    info_data = request.args.to_dict()
    verb = Verb.query.get(info_data.get("verbId"))
    verb_info = verb.to_json()
    verb_info["pattern"] = list()
    verb_info["count"] = 0
    for pattern in verb.patterns:
        pattern_info = pattern.to_json()
        pattern_info["samples"] = list()
        pattern_info["count"] = 0
        for sample in pattern.samples:
            pattern_info["samples"].append(sample.to_json())
            pattern_info["count"] += 1
        verb_info["count"] += 1
        verb_info["pattern"].append(pattern_info)
    verb_info["pattern"] = sorted(verb_info["pattern"], key=lambda x: x["PATTERN"])
    return render_template("data/verb/verbDetails.html", verb=verb_info)


@views.route('/verbPatternAddBatchPage', methods=['GET', 'POST'])
@permission_required("/verbPatternAddBatchPage")
@login_required
def verb_add_batch():
    info_data = request.args.to_dict()
    verb = Verb.query.get(info_data.get("verbId"))
    element_type_list = list()
    for element in verb.frame.frameElements:
        element_type_list.append({"ID": element.type.ID, "NAME": element.type.NAME})
    pattern_list = list()
    for pattern in verb.patterns:
        pattern_info = pattern.to_json()
        pattern_list.append(pattern_info)
    return render_template("data/verb/verbPatternAddBatchPage.html", patterns=pattern_list,
                           elementList=element_type_list, verbInfo=verb.to_json())


@views.route('/verbPatternEditBatchPage', methods=['GET', 'POST'])
@permission_required("/verbPatternEditBatchPage")
@login_required
def verb_edit_batch():
    info_data = request.args.to_dict()
    verb = Verb.query.get(info_data.get("verbId"))
    sample = Sample.query.get(info_data.get("sampleId"))
    element_type_list = list()
    for element in verb.frame.frameElements:
        element_type_list.append({"ID": element.type.ID, "NAME": element.type.NAME})
    return render_template("data/verb/verbPatternEditBatchPage.html", verb=verb,
                           element_type=element_type_list, sample=sample)


@views.route('/verbFileAddPage', methods=['GET', 'POST'])
@permission_required("/verbFileAddPage")
@login_required
def verb_file_add_page():
    info_data = request.args.to_dict()
    return render_template("data/verb/verbFileAddPage.html", frameId=info_data.get("frameId"))


@views.route('/verbAddPage', methods=['GET', 'POST'])
@permission_required("/verbAddPage")
@login_required
def verb_add():
    info_data = request.args.to_dict()
    return render_template("data/verb/verbAddPage.html", frameId=info_data.get("frameId"))


@views.route('/verbPatternAddPage', methods=['GET', 'POST'])
@permission_required("/verbPatternAddPage")
@login_required
def verb_pattern_add():
    info_data = request.args.to_dict()
    return render_template("data/verb/verbPatternAddPage.html", verbId=info_data.get("verbId"))


@views.route('/verbPatternEditPage', methods=['GET', 'POST'])
@permission_required("/verbPatternEditPage")
@login_required
def verb_pattern_edit():
    info_data = request.args.to_dict()
    verb_pattern = VerbPattern.query.get(info_data.get("patternId"))
    return render_template("data/verb/verbPatternEditPage.html", verbPattern=verb_pattern)


# ==================通告手册相关=======================
@views.route('/notice', methods=['GET', 'POST'])
@permission_required("/notice")
@login_required
def notice():
    return render_template("notice/notice.html")


@views.route('/noticeAddPage', methods=['GET', 'POST'])
@permission_required("/noticeAddPage")
@login_required
def notice_add_page():
    return render_template("notice/noticeAddPage.html")


@views.route('/noticeContent', methods=['GET', 'POST'])
@permission_required("/noticeContent")
@login_required
def notice_content_page():
    info_data = request.args.to_dict()
    notices = Notice.query.get(info_data.get("noticeId"))
    return render_template("notice/noticeContent.html", notice=notices.to_json())


@views.route('/showNotice', methods=['GET', 'POST'])
@permission_required("/showNotice")
@login_required
def show_notice():
    info_data = request.args.to_dict()
    notices = Notice.query.get(info_data.get("noticeId"))
    attach_list = list()
    if notices.attachments:
        for attachment in notices.attachments:
            attach_list.append(attachment.to_json())
    return render_template("notice/content.html", notice=notices.to_json(), attachList=attach_list)


@views.route('/noticeAttach', methods=['GET', 'POST'])
@permission_required("/noticeAttach")
@login_required
def notice_attach():
    info_data = request.args.to_dict()
    notices = Notice.query.get(info_data.get("noticeId"))
    attach_list = list()
    if notices:
        for attachment in notices.attachments:
            attach_list.append(attachment.to_json())
    return render_template("notice/attach.html", notice=notices.to_json(), attachList=attach_list)


# ==================调配与审核相关=======================
@views.route('/review', methods=['GET', 'POST'])
@permission_required("/review")
@login_required
def review():
    return render_template("data/review/review.html")


@views.route('/reviewDetails', methods=['GET', 'POST'])
@permission_required("/reviewDetails")
@login_required
def review_details():
    info_data = request.args.to_dict()
    frame = Frame.query.get(info_data.get("frame"))
    core_elements, non_core_elements, marker = list(), list(), list()
    for element in frame.frameElements:
        element_info = element.to_json()
        if element.elementSamples:
            for element_sample in element.elementSamples:
                if element_sample.FRAME_ID == frame.ID:
                    element_info["LEMMA"] = element_sample.LEMMA
                    element_info["SAMPLE"] = element_sample.SAMPLE
                    element_info["SAMPLE_ID"] = element_sample.ID
                    break
        element_info["NAME"] = element.type.NAME
        if element.type.TYPE == "Core Frame Elements":
            core_elements.append(element_info)
        elif element.type.TYPE == "Non-core Frame Elements":
            non_core_elements.append(element_info)
        elif element.type.TYPE == "Construction Marker":
            marker.append(element_info)
    return render_template("data/review/reviewDetails.html", frame=frame, core_elements=core_elements,
                           non_core_elements=non_core_elements, marker=marker)


@views.route('/reviewVerbDetails', methods=['GET', 'POST'])
@permission_required("/reviewVerbDetails")
@login_required
def review_verb_details():
    info_data = request.args.to_dict()
    verb = Verb.query.get(info_data.get("verbId"))
    verb_info = verb.to_json()
    verb_info["userName"] = "不分配标注者"
    verb_info["userId"] = ""
    if verb.user:
        verb_info["userName"] = verb.user.NAME
        verb_info["userId"] = verb.user.ID
    temp_frame = Frame.query.get(verb.TEMP_FRAME_ID)
    verb_info["tempFrame"] = ""
    verb_info["tempFrameId"] = ""
    if temp_frame:
        verb_info["tempFrame"] = temp_frame.NAME
        verb_info["tempFrameId"] = temp_frame.ID
    verb_info["pattern"] = list()
    verb_info["count"] = 0
    for pattern in verb.patterns:
        pattern_info = pattern.to_json()
        pattern_info["samples"] = list()
        pattern_info["count"] = 0
        for sample in pattern.samples:
            pattern_info["samples"].append(sample.to_json())
            pattern_info["count"] += 1
        verb_info["count"] += 1
        verb_info["pattern"].append(pattern_info)
    verb_info["pattern"] = sorted(verb_info["pattern"], key=lambda x: x["PATTERN"])
    return render_template("data/review/reviewVerbDetails.html", verb=verb_info)


@views.route('/frameFileAddPage', methods=['GET', 'POST'])
@permission_required("/frameFileAddPage")
@login_required
def frame_file_add_page():
    return render_template("data/review/frameFileAddPage.html")


# ==================标注相关=======================
@views.route('/dataLabel', methods=['GET', 'POST'])
@permission_required("/dataLabel")
@login_required
def data_label():
    return render_template("label/label.html")


@views.route('/labelDetails', methods=['GET', 'POST'])
@permission_required("/labelDetails")
@login_required
def label_details():
    info_data = request.args.to_dict()
    frame = Frame.query.get(info_data.get("frame"))
    core_elements, non_core_elements, marker = list(), list(), list()
    for element in frame.frameElements:
        element_info = element.to_json()
        if element.elementSamples:
            for element_sample in element.elementSamples:
                if element_sample.FRAME_ID == frame.ID:
                    element_info["LEMMA"] = element_sample.LEMMA
                    element_info["SAMPLE"] = element_sample.SAMPLE
                    break
        element_info["NAME"] = element.type.NAME
        if element.type.TYPE == "Core Frame Elements":
            core_elements.append(element_info)
        elif element.type.TYPE == "Non-core Frame Elements":
            non_core_elements.append(element_info)
        elif element.type.TYPE == "Construction Marker":
            marker.append(element_info)
    return render_template("label/labelDetails.html", frame=frame, core_elements=core_elements,
                           non_core_elements=non_core_elements, marker=marker)


@views.route('/labelVerbDetails', methods=['GET', 'POST'])
@permission_required("/labelVerbDetails")
@login_required
def label_verb_details():
    info_data = request.args.to_dict()
    verb = Verb.query.get(info_data.get("verbId"))
    verb_info = verb.to_json()
    verb_info["pattern"] = list()
    verb_info["count"] = 0
    for pattern in verb.patterns:
        pattern_info = pattern.to_json()
        pattern_info["samples"] = list()
        pattern_info["count"] = 0
        for sample in pattern.samples:
            pattern_info["samples"].append(sample.to_json())
            pattern_info["count"] += 1
        verb_info["count"] += 1
        verb_info["pattern"].append(pattern_info)
    verb_info["pattern"] = sorted(verb_info["pattern"], key=lambda x: x["PATTERN"])
    return render_template("label/labelVerbDetails.html", verb=verb_info)
