/**

 @Name：layuiAdmin 公共业务
 @Author：DengBoCong
 @Site：www.dengbocong.cn
 @License：Apache 2.0

 */

layui.define(function (exports) {
    var $ = layui.$
        , layer = layui.layer
        , laytpl = layui.laytpl
        , setter = layui.setter
        , dropdown = layui.dropdown
        , view = layui.view
        , admin = layui.admin

    $('#dropdownFrame').on('click', function () {
        window.location.href = "frames"
    });

    admin.req({
        method: "get",
        url: 'api/public/get!get_all_frame?url=framesList&param=frameId',
        done: function (res) {
            if (res.code == 0) {
                dropdown.render({
                    elem: '#dropdownFrame'
                    , id: 'dropdownFrame'
                    , trigger: 'hover'
                    , data: res.data
                    , click: function (data, othis) {}
                });
            } else {
                layer.msg(res.msg, {icon: 5});
            }
        }
    });

    $('#public-verb-search-button').on('click', function () {
        window.location.href = "searchContent?search=" + $('#public-verb-search-input').val()
    });

    //对外暴露的接口
    exports('publicCommon', {});
});