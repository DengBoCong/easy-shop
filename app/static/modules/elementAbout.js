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
        elem: '#LAY-element-manage'
        , url: 'api/data/get!get_all_element_type'
        , toolbar: '#elementToolbarDemo'
        , defaultToolbar: ['filter', 'exports', 'print']
        , cols: [[
            {type: 'checkbox', fixed: 'left'}
            , {field: 'ID', width: 200, title: 'ID', sort: true, fixed: 'left', style: 'overflow:hidden'}
            , {field: 'NAME', width: 200, title: 'Element名称', sort: true, edit: 'text'}
            , {field: 'TYPE', width: 250, title: 'Element类型', sort: true, templet: '#typeTpl'}
            , {field: 'CREATE_DATETIME', width: 200, title: '创建时间', sort: true}
            , {title: '操作', width: 250, align: 'center', fixed: 'right', toolbar: '#table-element-opt'}
        ]]
        , page: true
        , limit: 30
        , loading: true
        , height: 'full-0'
        , text: '对不起，加载出现异常！'
    });


    //监听工具条
    table.on('tool(LAY-element-manage)', function (obj) {
        var data = new Array(obj.data);

        if (obj.event === 'del') {
            layer.confirm('确认删除数据？', {
                icon: 3
                , title: '敏感操作'
            }, function (index) {
                admin.req({
                    method: "post",
                    url: 'api/data/delete!delete_element_type',
                    data: JSON.stringify(data),
                    done: function (res) {
                        if (res.code == 0) {
                            table.reload('LAY-element-manage');
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
                url: 'api/data/update!element_type_info',
                data: JSON.stringify(obj.data),
                done: function (res) {
                    if (res.code == 0) {
                        table.reload('LAY-element-manage');
                        layer.msg('更新成功');
                    } else {
                        layer.msg(res.msg, {icon: 5});
                    }
                }
            });
        } else if (obj.event === 'read') {
            layer.open({
                type: 2
                , title: 'Element详情'
                , content: 'elementFrameDetails?elementTypeId=' + obj.data.ID
                , maxmin: true
                , area: ['70%', '100%']
                , btn: ['确定', '取消']
                , yes: function (index, layero) {}
            });
        }
    });

    exports('elementAbout', {})
});