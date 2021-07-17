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


    table.render({
        elem: '#LAY-system-log-manage'
        , url: 'api/log/get!get_all_system_log'
        , toolbar: '#systemLogToolbarDemo'
        , defaultToolbar: ['filter', 'exports', 'print']
        , cols: [[
            {type: 'checkbox', fixed: 'left'}
            , {field: 'ID', width: 150, title: 'ID', sort: true, fixed: 'left', style: 'overflow:hidden'}
            , {field: 'LEVEL', width: 100, title: '日志级别', sort: true, templet: '#levelTpl'}
            , {field: 'USER_NAME', width: 150, title: '用户名称', sort: true}
            , {field: 'MESSAGE', width: 200, title: '描述'}
            , {field: 'ACTION', width: 150, title: '动作', sort: true}
            , {field: 'PATH', width: 350, title: '请求路径', sort: true}
            , {field: 'IP', width: 200, title: '操作IP', sort: true}
            , {field: 'CREATE_DATETIME', width: 200, title: '时间', sort: true}
            , {field: 'AGENT', width: 200, title: '用户代理', sort: true}
        ]]
        , page: true
        , limit: 30
        , loading: true
        , height: 'full-0'
        , text: '对不起，加载出现异常！'
    });

    table.render({
        elem: '#LAY-data-log-manage'
        , url: 'api/log/get!get_all_data_log'
        , toolbar: '#dataLogToolbarDemo'
        , defaultToolbar: ['filter', 'exports', 'print']
        , cols: [[
            {type: 'checkbox', fixed: 'left'}
            , {field: 'ID', title: 'ID', sort: true, fixed: 'left', style: 'overflow:hidden'}
            , {field: 'LEVEL', title: '日志级别', sort: true, templet: '#levelTpl'}
            , {field: 'USER_NAME', title: '用户名称', sort: true}
            , {field: 'DESCRIPTION', title: '描述'}
            , {field: 'ACTION', title: '动作', sort: true}
            , {field: 'DATA', title: '数据', sort: true}
            , {field: 'CREATE_DATETIME', title: '时间', sort: true}
        ]]
        , page: true
        , limit: 30
        , loading: true
        , height: 'full-0'
        , text: '对不起，加载出现异常！'
    });

    exports('logAbout', {})
});