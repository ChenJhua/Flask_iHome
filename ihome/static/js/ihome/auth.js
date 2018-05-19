function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}


function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    // TODO: 查询用户的实名认证信息
    $.get("/api/v1.0/user/auth", function (resp) {
        if(resp.data.real_name && resp.data.id_card){
            // 已进行实名认证，显示实名认证信息
            $("#real-name").val(resp.data.real_name);
            $("#id-card").val(resp.data.id_card);
            // 禁用真实姓名和身份证输入框
            $("#real-name").attr("disabled", true);
            $("#id-card").attr("disabled", true);
            // 隐藏保存按钮
            $(".btn-success").hide();
        }

    });

    // TODO: 管理实名信息表单的提交行为
    $("#form-auth").submit(function (e) {
        e.preventDefault();

        // 获取用户输入的实名认证信息
        var real_name = $("#real-name").val();
        var id_card = $("#id-card").val();

        if(!real_name || !id_card){
            $(".error-msg").show();
            return;
        }else{
            $(".error-msg").hide();
        }

        // 组织参数
        var params = {
            "real_name": real_name,
            "id_card": id_card,
        }

        $.ajax({
            "url":"/api/v1.0/user/auth",
            "type": "post",
            "data": JSON.stringify(params),
            "contentType": "application/json",
            "headers": {
                "X-CSRFToken": getCookie("csrf_token")
            },
            "success": function (resp) {
                if(resp.errno == "0"){
                    // 实名认证成功
                    // 禁用真实姓名和身份证输入框
                    $("#real-name").attr("disabled", true);
                    $("#id-card").attr("disabled", true);
                    // 隐藏保存按钮
                    $(".btn-success").hide();
                }else if(resp.errno == "4101"){
                    // 未登录
                    location.href = "login.html"
                }
                else{
                    // 实名认证失败
                    alert(resp.errmsg);
                }
            }
        })

    })
})