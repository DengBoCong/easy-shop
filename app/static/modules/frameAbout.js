/**

 @Name：layuiAdmin 用户管理 管理员管理 角色管理
 @Author：star1029
 @Site：http://www.layui.com/admin/
 @License：LPPL

 */

layui.define(['table', 'form', 'upload'], function (exports) {
    var $ = layui.$
        , admin = layui.admin
        , table = layui.table
        , form = layui.form
        , upload = layui.upload;


    admin.events.frameElementAdd = function (othis) {
        layer.open({
            type: 2
            , title: 'Frame关联Element元素'
            , content: 'frameAddElementPage?frameId=' + $('#frame-remain-id').val() + '&type=' + $(this).data('type')
            , maxmin: true
            , area: ['100%', '80%']
            , success: function (layero, index) {}
        });
    };

    admin.events.frameElementDelete = function (othis) {
        var arr = new Array();
        $("input:checkbox[name='coreElement']:checked").each(function(i){
            arr[i] = $(this).val();
        });
        if (arr.length === 0) {
            layer.msg("未选中数据");
            return
        }
        admin.req({
            method: "post",
            url: 'api/data/delete!delete_frame_element',
            data: JSON.stringify({'FRAME_ID': $('#frame-remain-id').val(), 'ID_LIST': arr}),
            done: function (res) {
                layer.msg(res.msg);
            }
        });
    };

    admin.events.frameElementEdit = function (othis) {
        var arr = new Array();
        $("input:checkbox[name='coreElement']:checked").each(function(i){
            arr[i] = $(this).val();
        });
        if (arr.length === 0) {
            layer.msg("未选中数据");
            return
        }
        if (arr.length !== 1) {
            layer.msg("最多同时只能修改一个Element");
            return
        }
        layer.open({
            type: 2
            , title: '更新Frame关联Element元素的信息'
            , content: 'frameEditElementPage?elementId=' + arr[0]
            , maxmin: true
            , area: ['100%', '50%']
            , success: function (layero, index) {}
        });
    };

    var avatarSrc = $('#LAY_frame_avatarSrc');
    upload.render({
        url: '/api/common/upload!single_image_upload'
        , elem: '#LAY_frame_avatarUpload'
        , size: 200
        , done: function (res) {
            if (res.code == 0) {
                layer.msg(res.msg, {icon: 1});
                avatarSrc.val(res.data.url);
            } else {
                layer.msg(res.msg, {icon: 5});
            }
        }
    });

    //查看头像
    admin.events.frameAvartatPreview = function (othis) {
        var src = avatarSrc.val();
        layer.photos({
            photos: {
                "title": "查看图片" //相册标题
                , "data": [{
                    "src": src //原图地址
                }]
            }
            , shade: 0.01
            , closeBtn: 1
            , anim: 5
        });
    };

    exports('frameAbout', {})
});