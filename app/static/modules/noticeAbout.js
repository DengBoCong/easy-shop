/**

 @Name：layuiAdmin 用户管理 管理员管理 角色管理
 @Author：star1029
 @Site：http://www.layui.com/admin/
 @License：LPPL

 */


layui.define(['table', 'form'], function (exports) {
    var $ = layui.$
        , admin = layui.admin
        , table = layui.table
        , form = layui.form;

    //快捷链接管理
    table.render({
        elem: '#LAY-notice-manage'
        , url: 'api/notice/get!get_all_notice_info'
        , toolbar: '#noticeToolbarDemo'
        , defaultToolbar: ['filter', 'exports', 'print']
        , cols: [[
            {type: 'checkbox', fixed: 'left'}
            , {
                field: 'ID',
                width: 150,
                align: 'center',
                title: 'ID',
                sort: true,
                fixed: 'left',
                style: 'overflow:hidden'
            }
            , {field: 'TITLE', width: 300, align: 'center', title: '标题', sort: true, edit: 'text'}
            , {field: 'SUB_TITLE', width: 300, align: 'center', title: '子标题', sort: true, edit: 'text'}
            , {field: 'IF_TOP', width: 150, align: 'center', title: '是否置顶', templet: '#topTpl'}
            , {field: 'DESCRIPTION', width: 150, align: 'center', title: '备注', edit: 'text'}
            , {field: 'UPDATE_DATETIME', width: 200, align: 'center', title: '更新时间', sort: true}
            , {field: 'CREATE_DATETIME', width: 200, align: 'center', title: '创建时间', sort: true}
            , {title: '操作', width: 300, align: 'center', fixed: 'right', toolbar: '#table-notice-opt'}
        ]]
        , page: true
        , limit: 30
        , loading: true
        , height: 'full-0'
        , text: '对不起，加载出现异常！'
    });

    table.on('tool(LAY-notice-manage)', function (obj) {
        var data = new Array(obj.data);

        if (obj.event === 'del') {
            layer.confirm('确认删除数据？', {
                icon: 3
                , title: '敏感操作'
            }, function (index) {
                admin.req({
                    method: "post",
                    url: 'api/notice/delete!delete_notice',
                    data: JSON.stringify(data),
                    done: function (res) {
                        if (res.code == 0) {
                            table.reload('LAY-notice-manage');
                            layer.msg('已删除');
                        } else {
                            layer.msg(res.msg, {icon: 5});
                        }
                    }
                });
            });
        } else if (obj.event === 'edit') {
            admin.req({
                method: "post",
                url: 'api/notice/update!notice_info',
                data: JSON.stringify(obj.data),
                done: function (res) {
                    if (res.code == 0) {
                        table.reload('LAY-notice-manage');
                        layer.msg('更新成功');
                    } else {
                        layer.msg(res.msg, {icon: 5});
                    }
                }
            });
        } else if (obj.event === 'editContent') {
            layer.open({
                type: 2
                , title: '修改通告手册内容'
                , content: 'noticeContent?noticeId=' + obj.data.ID
                , maxmin: true
                , area: ['100%', '600px']
                , yes: function (index, layero) {}
            });
        } else if (obj.event === 'attach') {
            layer.open({
                type: 2
                , title: '附件'
                , content: 'noticeAttach?noticeId=' + obj.data.ID
                , maxmin: true
                , area: ['95%', '400px']
                , yes: function (index, layero) {}
            });
        }
    });

    exports('noticeAbout', {})
});