/**

 @Name：layuiAdmin 用户登入和注册等
 @Author：DengBoCong
 @Site：www.dengbocong.cn
 @License：Apache 2.0

 */

layui.define(['form', 'upload'], function (exports) {
    var $ = layui.$
        , layer = layui.layer
        , laytpl = layui.laytpl
        , setter = layui.setter
        , view = layui.view
        , admin = layui.admin
        , form = layui.form
        , upload = layui.upload;

    var $body = $('body');

    //自定义验证
    form.verify({
        nickname: function (value, item) { //value：表单的值、item：表单的DOM对象
            if (value !== "") {
                if (!new RegExp("^[a-zA-Z0-9_\u4e00-\u9fa5\\s·]+$").test(value)) {
                    return '用户名不能为空或有特殊字符';
                }
                if (/(^\_)|(\__)|(\_+$)/.test(value)) {
                    return '用户名首尾不能出现下划线\'_\'';
                }
                if (/^\d+\d+\d$/.test(value)) {
                    return '用户名不能全为数字';
                }
            }
        }

        //我们既支持上述函数式的方式，也支持下述数组的形式
        //数组的两个值分别代表：[正则匹配、匹配不符时的提示文字]
        , pass: [
            /^[\S]{6,18}$/
            , '密码必须6到12位，且不能出现空格'
        ], modify_pass: function (value, item) { //value：表单的值、item：表单的DOM对象
            if (!/^[\S]{6,18}$/.test(value)) {
                return '密码必须6到12位，且不能出现空格';
            }
            if (value == $('#current_password').val()) {
                return '修改密码不能和当前密码重复';
            }
        }, repass: function (value) {
            if (value !== $('#LAY_password').val()) {
                return '两次密码输入不一致';
            }
        }, age: [
            /^((1[0-5])|[1-9])?\d$/
            , '年龄应为0-159'
        ], weChat: function (value, item) { //value：表单的值、item：表单的DOM对象
            if (value != "" && !/^[a-zA-Z]{1}[-_a-zA-Z0-9]{5,19}$/.test(value)) {
                return '请填写正确的微信号';
            }
        }, qq: function (value, item) { //value：表单的值、item：表单的DOM对象
            if (value != "" && !/^[1-9]\d{4,10}$/.test(value)) {
                return '请填写正确的QQ号';
            }
        }
    });


    //设置我的资料
    form.on('submit(setmyinfo)', function (obj) {
        update_data = obj.field
        delete update_data.file
        //提交修改
        admin.req({
            method: "post",
            url: 'api/user/update!user_info',
            data: JSON.stringify(obj.field),
            done: function (res) {
                if (res.code == 0) {
                    layer.msg(res.msg, {
                        offset: '15px'
                        , icon: 1
                        , time: 1000
                    }, function () {
                        location.href = 'personInfo'; //后台主页
                    });
                } else {
                    layer.msg(res.msg, {icon: 5});
                }
            }
        });
    });

    //设置密码
    form.on('submit(setmypass)', function (obj) {
        obj.field["access_token"] = layui.data('verb').access_token
        //提交修改
        admin.req({
            method: "post",
            url: 'api/user/update!user_pwd',
            data: JSON.stringify(obj.field),
            done: function (res) {
                if (res.code == 0) {
                    layer.msg(res.msg, {
                        offset: '15px'
                        , icon: 1
                        , time: 1000
                    }, function () {
                        top.document.location.href = 'login'; //后台主页
                    });
                } else {
                    layer.msg(res.msg, {icon: 5});
                }
            }
        });
    });

    //上传头像
    var avatarSrc = $('#LAY_avatarSrc');
    upload.render({
        url: '/api/common/upload!single_image_upload'
        , elem: '#LAY_avatarUpload'
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
    admin.events.avartatPreview = function (othis) {
        var src = avatarSrc.val();
        layer.photos({
            photos: {
                "title": "查看头像" //相册标题
                , "data": [{
                    "src": src //原图地址
                }]
            }
            , shade: 0.01
            , closeBtn: 1
            , anim: 5
        });
    };


    //发送短信验证码
    admin.sendAuthCode({
        elem: '#LAY-user-getsmscode'
        , elemPhone: '#LAY-user-login-cellphone'
        , elemVercode: '#LAY-user-login-vercode'
        , ajax: {
            url: layui.setter.base + 'json/user/sms.js' //实际使用请改成服务端真实接口
        }
    });

    //对外暴露的接口
    exports('user', {});
});