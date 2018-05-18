function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function() {
    $("#mobile").focus(function(){
        $("#mobile-err").hide();
    });
    $("#password").focus(function(){
        $("#password-err").hide();
    });
    // TODO: 添加登录表单提交操作
    $(".form-login").submit(function(e){
        // 阻止表单默认提交
        e.preventDefault();
        var mobile = $("#mobile").val();
        var passwd = $("#password").val();
        if (!mobile) {
            $("#mobile-err span").html("请填写正确的手机号！");
            $("#mobile-err").show();
            return;
        } 
        if (!passwd) {
            $("#password-err span").html("请填写密码!");
            $("#password-err").show();
            return;
        }

        // 组织参数
        var params = {
            "mobile": mobile,
            "password": passwd,
        };
        // todo:请求进行登录
        $.ajax({
            "url":"/api/v1.0/sessions",
            "type": "post",
            "data": JSON.stringify(params),
            "contentType": "application/json",
            "headers": {
                "X-CSRFToken": getCookie("csrf_token")
            },
            "success": function (resp) {
                if(resp.errno == "0"){
                    //登录成功，跳转到首页
                    location.href = "index.html"
                }else{
                    // 登录失败
                    $("#password-err span").html(resp.errmsg);
                    $("#password-err").show()
                }
            }
        })
    });
});




