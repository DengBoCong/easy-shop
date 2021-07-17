/**

 @Name：layuiAdmin 用户管理 管理员管理 角色管理
 @Author：star1029
 @Site：http://www.layui.com/admin/
 @License：LPPL

 */

layui.define(['form'], function (exports) {
    var $ = layui.$
        , admin = layui.admin
        , form = layui.form;


    admin.events.clickVerbSample = function (othis) {
        sampleId = othis.attr("data-sampleId")
        verbId = $('#verb-details-verb-id').val()
        layer.open({
            type: 2
            , title: 'Sample更新--当前输入内容只更新当前Sample'
            , content: 'verbPatternEditBatchPage?sampleId=' + sampleId + '&verbId=' + verbId
            , maxmin: true
            , area: ['100%', '90%']
            , success: function (layero, index) {
            }
        });
    };

    admin.events.verbEdit = function (othis) {
        admin.req({
            method: "post",
            url: 'api/data/update!verb_basic_info',
            data: JSON.stringify({
                'ID': $('#verb-details-verb-id').val(),
                'NAME': $('#verb-details-edit-verb-name').val(),
                'PIN_YIN': $('#verb-details-edit-verb-pinyin').val(),
                'FREQUENCY': $('#verb-details-edit-verb-frequency').val(),
                'USER_ID': $('#verb-details-edit-verb-user').val(),
                'TEMP_FRAME_ID': $('#verb-details-edit-verb-frame').val()
            }),
            done: function (res) {
                layer.msg(res.msg);
            }
        });
    };

    admin.events.verbPatternAdd = function (othis) {
        layer.open({
            type: 2
            , title: '批量添加--不关闭弹出框，请勿重复添加'
            , content: 'verbPatternAddPage?verbId=' + $('#verb-details-verb-id').val()
            , maxmin: true
            , area: ['100%', '280px']
            , success: function (layero, index) {
            }
        });
    };

    admin.events.verbSampleBatchAdd = function (othis) {
        layer.open({
            type: 2
            , title: '批量添加--不关闭弹出框，请勿重复添加'
            , content: 'verbPatternAddBatchPage?verbId=' + $('#verb-details-verb-id').val()
            , maxmin: true
            , area: ['100%', '90%']
            , success: function (layero, index) {
            }
        });
    };

    admin.events.verbBatchDelete = function (othis) {
        var arr = new Array();
        $("input:checkbox[name='verbSampleCheck']:checked").each(function (i) {
            arr[i] = $(this).val();
        });
        if (arr.length === 0) {
            layer.msg("未选中数据");
            return
        }
        admin.req({
            method: "post",
            url: 'api/data/delete!delete_verb_pattern_sample',
            data: JSON.stringify(arr),
            done: function (res) {
                layer.msg(res.msg);
            }
        });
    };

    admin.events.verbPatternDel = function (othis) {
        patternId = othis.attr("data-patternId")
        admin.req({
            method: "post",
            url: 'api/data/delete!delete_verb_pattern_by_id',
            data: JSON.stringify({'ID': patternId}),
            done: function (res) {
                layer.msg(res.msg);
                $("#" + patternId).hide();
            }
        });
    };

    admin.events.verbPatternEdit = function (othis) {
        patternId = othis.attr("data-patternId")
        layer.open({
            type: 2
            , title: 'Pattern更新--不关闭弹出框，请勿重复更新'
            , content: 'verbPatternEditPage?patternId=' + patternId
            , maxmin: true
            , area: ['100%', '280px']
            , success: function (layero, index) {
            }
        });
    };

    exports('verbAbout', {})
});