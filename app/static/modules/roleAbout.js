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


    //权限管理
    table.render({
        elem: '#LAY-privilege-manage'
        , url: 'api/role/get!all_privilege_info'
        , toolbar: '#privilegeToolbarDemo'
        , defaultToolbar: ['filter', 'exports', 'print']
        , cols: [[
            {type: 'checkbox', fixed: 'left'}
            , {field: 'ID', width: 100, title: 'ID', sort: true, fixed: 'left', style: 'overflow:hidden'}
            , {field: 'NAME', width: 200, title: '命名', sort: true, edit: 'text'}
            , {field: 'TARGET', width: 200, title: '权限目标地址'} // event: 'setRole'
            , {field: 'ACTION', width: 150, title: '动作', sort: true, templet: '#actionTpl'}
            , {field: 'DESCRIPTION', width: 300, title: '描述', edit: 'text'}
            , {field: 'UPDATE_DATETIME', width: 200, title: '更新时间', sort: true}
            , {field: 'CREATE_DATETIME', width: 200, title: '创建时间', sort: true}
            , {field: 'SORT', width: 100, title: '排序', edit: 'text', sort: true}
            , {title: '操作', width: 150, align: 'center', fixed: 'right', toolbar: '#table-privilege-opt'}
        ]]
        , page: true
        , limit: 30
        , loading: true
        , height: 'full-0'
        , text: '对不起，加载出现异常！'
    });

    //权限管理
    table.render({
        elem: '#LAY-role-manage'
        , url: 'api/role/get!all_role_info'
        , toolbar: '#roleToolbarDemo'
        , defaultToolbar: ['filter', 'exports', 'print']
        , parseData: function (res) { //res 即为原始返回的数据
            return {
                "code": res.code, //解析接口状态
                "msg": res.msg, //解析提示文本
                "count": res.count, //解析数据长度
                "data": res.data.roles //解析数据列表
            };
        }
        , cols: [[
            {type: 'checkbox', fixed: 'left'}
            , {field: 'ID', width: 200, title: 'ID', sort: true, fixed: 'left', style: 'overflow:hidden'}
            , {field: 'NAME', width: 200, title: '角色名称', sort: true, edit: 'text'}
            , {field: 'TYPE', width: 200, title: '创建类型', sort: true, templet: '#typeTpl'}
            , {field: 'DESCRIPTION', width: 350, title: '描述', edit: 'text'}
            , {field: 'UPDATE_DATETIME', width: 200, title: '更新时间', sort: true}
            , {field: 'CREATE_DATETIME', width: 200, title: '创建时间', sort: true}
            , {title: '操作', width: 250, align: 'center', fixed: 'right', toolbar: '#table-role-opt'}
        ]]
        , page: true
        , limit: 30
        , loading: true
        , height: 'full-0'
        , text: '对不起，加载出现异常！'
    });

    //监听工具条
    table.on('tool(LAY-privilege-manage)', function (obj) {
        var data = new Array(obj.data);

        if (obj.event === 'del') {
            layer.confirm('确认删除数据？', {
                icon: 3
                , title: '敏感操作'
            }, function (index) {
                admin.req({
                    method: "post",
                    url: 'api/role/delete!delete_privileges',
                    data: JSON.stringify(data),
                    done: function (res) {
                        if (res.code == 0) {
                            table.reload('LAY-privilege-manage');
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
                url: 'api/role/update!privilege_info',
                data: JSON.stringify(obj.data),
                done: function (res) {
                    if (res.code == 0) {
                        table.reload('LAY-privilege-manage');
                        layer.msg('更新成功');
                    } else {
                        layer.msg(res.msg, {icon: 5});
                    }
                }
            });
        }
    });

    table.on('tool(LAY-role-manage)', function (obj) {
        var data = new Array(obj.data);

        if (obj.event === 'del') {
            layer.confirm('确认删除数据？', {
                icon: 3
                , title: '敏感操作'
            }, function (index) {
                admin.req({
                    method: "post",
                    url: 'api/role/delete!delete_roles',
                    data: JSON.stringify(data),
                    done: function (res) {
                        if (res.code == 0) {
                            table.reload('LAY-role-manage');
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
                url: 'api/role/update!role_info',
                data: JSON.stringify(obj.data),
                done: function (res) {
                    if (res.code == 0) {
                        table.reload('LAY-role-manage');
                        layer.msg('更新成功');
                    } else {
                        layer.msg(res.msg, {icon: 5});
                    }
                }
            });
        } else if (obj.event === 'addPrivilege') {
            layer.open({
                type: 2,
                title: '角色赋权',
                maxmin: true,
                shadeClose: true,
                content: 'roleForm?roleId=' + obj.data.ID,
                area: ['800px', '100%'],
                success: function (layero, index) {}
            });
        }
    });

    exports('roleAbout', {})
});