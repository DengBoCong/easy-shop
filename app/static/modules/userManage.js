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


    //用户管理
    table.render({
        elem: '#LAY-user-manage'
        , url: 'api/user/get!user_list'
        , toolbar: '#userToolbarDemo'
        , defaultToolbar: ['filter', 'exports', 'print']
        , cols: [[
            {type: 'checkbox', fixed: 'left'}
            , {field: 'ID', width: 150, title: 'ID', sort: true, fixed: 'left', style: 'overflow:hidden'}
            , {field: 'NAME', width: 100, title: '用户名', sort: true, edit: 'text'}
            , {field: 'ROLE_NAME', width: 150, title: '角色', templet: '#roleTpl'} // event: 'setRole'
            , {field: 'PHONE', width: 150, title: '手机', sort: true, edit: 'text'}
            , {field: 'EMAIL', width: 200, title: '邮箱', sort: true, edit: 'text'}
            , {field: 'SEX', width: 100, title: '性别', templet: '#sexTpl'}
            , {field: 'AGE', width: 100, title: '年龄', sort: true, edit: 'text'}
            , {field: 'WE_CHAT', width: 150, title: '微信', edit: 'text'}
            , {field: 'QQ', width: 150, title: 'QQ', edit: 'text'}
            , {field: 'LAST_IP', width: 150, title: '最后登录IP'}
            , {field: 'LAST_DATETIME', width: 200, title: '最后登录时间'}
            , {field: 'CREATE_DATETIME', width: 200, title: '加入时间', sort: true}
            , {field: 'IF_LOGIN', width: 100, title: '允许登录', templet: '#loginTpl'}
            , {field: 'DESCRIPTION', width: 300, title: '备注', edit: 'text'}
            , {title: '操作', width: 150, align: 'center', fixed: 'right', toolbar: '#table-useradmin-webuser'}
        ]]
        , page: true
        , limit: 30
        , loading: true
        , height: 'full-0'
        , text: '对不起，加载出现异常！'
    });

    //监听工具条
    table.on('tool(LAY-user-manage)', function (obj) {
        var data = new Array(obj.data);

        if (obj.event === 'del') {
            layer.confirm('确认删除数据？', {
                icon: 3
                , title: '敏感操作'
            }, function (index) {
                admin.req({
                    method: "post",
                    url: 'api/user/delete!delete_user',
                    data: JSON.stringify(data),
                    done: function (res) {
                        if (res.code == 0) {
                            table.reload('LAY-user-manage');
                            layer.msg('已删除');
                            admin.req({
                                method: "get",
                                url: 'api/role/get!all_role_info',
                                done: function (res) {
                                    if (res.code == 0) {
                                        roles_list = res.data.roles
                                        for (i = 0; i < roles_list.length; i++) {
                                            $('.role_select').append(new Option(roles_list[i].NAME, roles_list[i].ID));// 下拉菜单里添加元素
                                        }
                                        layui.form.render("select");//重新渲染 固定写法
                                    } else {
                                        layer.msg(res.msg, {icon: 5});
                                    }
                                }
                            });
                        } else {
                            layer.msg(res.msg, {icon: 5});
                        }
                    }
                });
            });
        } else if (obj.event === 'edit') {
            if (!new RegExp("^[a-zA-Z0-9_\u4e00-\u9fa5\\s·]+$").test(obj.data.NAME)) {
                layer.msg('用户名不能为空或有特殊字符', {icon: 5});
                return
            }
            if (/(^\_)|(\__)|(\_+$)/.test(obj.data.NAME)) {
                layer.msg('用户名首尾不能出现下划线\'_\'', {icon: 5});
                return
            }
            if (/^\d+\d+\d$/.test(obj.data.NAME)) {
                layer.msg('用户名不能全为数字', {icon: 5});
                return
            }
            if (!/^((1[0-5])|[1-9])?\d$/.test(obj.data.AGE)) {
                layer.msg('年龄应为0-159', {icon: 5});
                return
            }
            if (obj.data.WE_CHAT != "" && !/^[a-zA-Z]{1}[-_a-zA-Z0-9]{5,19}$/.test(obj.data.WE_CHAT)) {
                layer.msg('请填写正确的微信号', {icon: 5});
                return
            }

            if (obj.data.QQ != "" && !/^[1-9]\d{4,10}$/.test(obj.data.QQ)) {
                layer.msg('请填写正确的QQ号', {icon: 5});
                return
            }
            if (!/^1[3456789]\d{9}$/.test(obj.data.PHONE)) {
                layer.msg('请填写正确的手机号', {icon: 5});
                return
            }
            if (!/^[0-9a-zA-Z_.-]+[@][0-9a-zA-Z_.-]+([.][a-zA-Z]+){1,2}$/.test(obj.data.EMAIL)) {
                layer.msg('请填写正确的邮箱号', {icon: 5});
                return
            }
            update_data = obj.data
            delete update_data.CREATE_DATETIME
            delete update_data.ID
            delete update_data.LAST_DATETIME
            delete update_data.ROLE_NAME
            delete update_data.UPDATE_DATETIME
            update_data.IF_LOGIN = update_data.IF_LOGIN === "1"

            admin.req({
                method: "post",
                url: 'api/user/update!user_info',
                data: JSON.stringify(update_data),
                done: function (res) {
                    if (res.code == 0) {
                        table.reload('LAY-user-manage');
                        layer.msg('更新成功');
                    } else {
                        layer.msg(res.msg, {icon: 5});
                    }
                }
            });
        }
        // else if (obj.event === 'setRole') {
        //     layer.prompt({
        //         formType: 2
        //         , title: '修改 ID 为 [' + data.id + '] 的用户签名'
        //         , value: data.sign
        //     }, function (value, index) {
        //         layer.close(index);
        //
        //         //这里一般是发送修改的Ajax请求
        //
        //         //同步更新表格和缓存对应的值
        //         obj.update({
        //             sign: value
        //         });
        //     });
        // }
    });

    //监听单元格编辑
    // table.on('edit(test-table-cellEdit)', function (obj) {
    //     var value = obj.value //得到修改后的值
    //         , data = obj.data //得到所在行所有键值
    //         , field = obj.field; //得到字段
    //     layer.msg('[ID: ' + data.id + '] ' + field + ' 字段更改为：' + value, {
    //         offset: '15px'
    //     });
    // });

    //管理员管理
    table.render({
        elem: '#LAY-user-back-manage'
        , url: layui.setter.base + 'json/useradmin/mangadmin.js' //模拟接口
        , cols: [[
            {type: 'checkbox', fixed: 'left'}
            , {field: 'id', width: 80, title: 'ID', sort: true}
            , {field: 'loginname', title: '登录名'}
            , {field: 'telphone', title: '手机'}
            , {field: 'email', title: '邮箱'}
            , {field: 'role', title: '角色'}
            , {field: 'jointime', title: '加入时间', sort: true}
            , {field: 'check', title: '审核状态', templet: '#buttonTpl', minWidth: 80, align: 'center'}
            , {title: '操作', width: 150, align: 'center', fixed: 'right', toolbar: '#table-useradmin-admin'}
        ]]
        , text: '对不起，加载出现异常！'
    });

    //监听工具条
    table.on('tool(LAY-user-back-manage)', function (obj) {
        var data = obj.data;
        if (obj.event === 'del') {
            layer.prompt({
                formType: 1
                , title: '敏感操作，请验证口令'
            }, function (value, index) {
                layer.close(index);
                layer.confirm('确定删除此管理员？', function (index) {
                    console.log(obj)
                    obj.del();
                    layer.close(index);
                });
            });
        } else if (obj.event === 'edit') {
            var tr = $(obj.tr);

            layer.open({
                type: 2
                , title: '编辑管理员'
                , content: 'adminForm'
                , area: ['420px', '420px']
                , btn: ['确定', '取消']
                , yes: function (index, layero) {
                    var iframeWindow = window['layui-layer-iframe' + index]
                        , submitID = 'LAY-user-back-submit'
                        , submit = layero.find('iframe').contents().find('#' + submitID);

                    //监听提交
                    iframeWindow.layui.form.on('submit(' + submitID + ')', function (data) {
                        var field = data.field; //获取提交的字段

                        //提交 Ajax 成功后，静态更新表格中的数据
                        //$.ajax({});
                        table.reload('LAY-user-front-submit'); //数据刷新
                        layer.close(index); //关闭弹层
                    });

                    submit.trigger('click');
                }
                , success: function (layero, index) {

                }
            })
        }
    });

    //角色管理
    table.render({
        elem: '#LAY-user-back-role'
        , url: layui.setter.base + 'json/useradmin/role.js' //模拟接口
        , cols: [[
            {type: 'checkbox', fixed: 'left'}
            , {field: 'id', width: 80, title: 'ID', sort: true}
            , {field: 'rolename', title: '角色名'}
            , {field: 'limits', title: '拥有权限'}
            , {field: 'descr', title: '具体描述'}
            , {title: '操作', width: 150, align: 'center', fixed: 'right', toolbar: '#table-useradmin-admin'}
        ]]
        , text: '对不起，加载出现异常！'
    });

    //监听工具条
    table.on('tool(LAY-user-back-role)', function (obj) {
        var data = obj.data;
        if (obj.event === 'del') {
            layer.confirm('确定删除此角色？', function (index) {
                obj.del();
                layer.close(index);
            });
        } else if (obj.event === 'edit') {
            var tr = $(obj.tr);

            layer.open({
                type: 2
                , title: '编辑角色'
                , content: 'roleForm'
                , area: ['500px', '480px']
                , btn: ['确定', '取消']
                , yes: function (index, layero) {
                    var iframeWindow = window['layui-layer-iframe' + index]
                        , submit = layero.find('iframe').contents().find("#LAY-user-role-submit");

                    //监听提交
                    iframeWindow.layui.form.on('submit(LAY-user-role-submit)', function (data) {
                        var field = data.field; //获取提交的字段

                        //提交 Ajax 成功后，静态更新表格中的数据
                        //$.ajax({});
                        table.reload('LAY-user-back-role'); //数据刷新
                        layer.close(index); //关闭弹层
                    });

                    submit.trigger('click');
                }
                , success: function (layero, index) {

                }
            })
        }
    });

    exports('userManage', {})
});