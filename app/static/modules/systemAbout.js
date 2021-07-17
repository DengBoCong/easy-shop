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
        elem: '#LAY-system-quick-link-manage'
        , url: 'api/system/get!link_list'
        , toolbar: '#quickLinkToolbarDemo'
        , defaultToolbar: ['filter', 'exports', 'print']
        , cols: [[
            {type: 'checkbox', fixed: 'left'}
            , {field: 'ID', width: 150, align: 'center', title: 'ID', sort: true, fixed: 'left', style: 'overflow:hidden'}
            , {field: 'NAME', width: 150, align: 'center', title: '名称', sort: true, edit: 'text'}
            , {field: 'URL', width: 250, align: 'center', title: 'URL', edit: 'text'} // event: 'setRole'
            , {field: 'ICON_CLS', width: 200, align: 'center', title: 'icon', sort: true}
            , {field: 'SORT', width: 100, align: 'center', title: '排序号', edit: 'text', sort: true}
            , {field: 'UPDATE_DATETIME', width: 180, align: 'center', title: '更新时间', sort: true}
            , {field: 'CREATE_DATETIME', width: 180, align: 'center', title: '创建时间', sort: true}
            , {title: '操作', width: 180, align: 'center', fixed: 'right', toolbar: '#table-quick-link-system-opt'}
        ]]
        , page: true
        , limit: 30
        , loading: true
        , height: 'full-0'
        , text: '对不起，加载出现异常！'
    });

    //快捷链接管理
    table.render({
        elem: '#LAY-system-contact-manage'
        , url: 'api/system/get!user_contacts'
        , toolbar: '#contactToolbarDemo'
        , defaultToolbar: ['filter', 'exports', 'print']
        , cols: [[
            {type: 'checkbox', fixed: 'left'}
            , {field: 'ID', width: 150, title: 'ID', sort: true, fixed: 'left'}
            , {field: 'NAME', width: 100, title: '用户名', sort: true}
            , {field: 'PHONE', width: 150, title: '手机', sort: true}
            , {field: 'EMAIL', width: 200, title: '邮箱', sort: true}
            , {field: 'WE_CHAT', width: 150, title: '微信'}
            , {field: 'QQ', width: 150, title: 'QQ'}
            , {field: 'DESCRIPTION', width: 300, title: '备注'}
            , {title: '操作', width: 100, align: 'center', fixed: 'right', toolbar: '#table-contact-system-opt'}
        ]]
        , page: true
        , limit: 30
        , loading: true
        , height: 'full-0'
        , text: '对不起，加载出现异常！'
    });

    //监听工具条
    table.on('tool(LAY-system-quick-link-manage)', function (obj) {
        var data = new Array(obj.data);

        if (obj.event === 'del') {
            layer.confirm('确认删除数据？', {
                icon: 3
                , title: '敏感操作'
            }, function (index) {
                admin.req({
                    method: "post",
                    url: 'api/system/delete!delete_link',
                    data: JSON.stringify(data),
                    done: function (res) {
                        if (res.code == 0) {
                            table.reload('LAY-system-quick-link-manage');
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
                url: 'api/system/update!link_info',
                data: JSON.stringify(obj.data),
                done: function (res) {
                    if (res.code == 0) {
                        table.reload('LAY-system-quick-link-manage');
                        layer.msg('更新成功');
                    } else {
                        layer.msg(res.msg, {icon: 5});
                    }
                }
            });
        }
    });

    table.on('tool(LAY-system-contact-manage)', function (obj) {
        var data = new Array(obj.data);

        if (obj.event === 'del') {
            layer.confirm('确认删除数据？', {
                icon: 3
                , title: '敏感操作'
            }, function (index) {
                admin.req({
                    method: "post",
                    url: 'api/system/delete!delete_contact',
                    data: JSON.stringify(data),
                    done: function (res) {
                        if (res.code == 0) {
                            table.reload('LAY-system-contact-manage');
                            layer.msg('已删除');
                        } else {
                            layer.msg(res.msg, {icon: 5});
                        }
                    }
                });
            });
        }
    });

    exports('systemAbout', {})
});