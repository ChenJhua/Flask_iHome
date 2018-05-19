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

$(document).ready(function () {
    // TODO: 在页面加载完毕向后端查询用户的信息
    $.get("/api/v1.0/user", function (resp) {
        if(resp.errno == "0"){
            // 获取信息成功
            // 设置用户头像img的src
            $("#user-avatar").attr("src", resp.data.avatar_url);
            // 设置用户用户名
            $("#user-name").val(resp.data.username);
        }else if(resp.errno == "4101"){
            //用户未登录，跳转到登录页面
            location.href = "login.html"
        }else{
            // 获取失败
            alert(resp.errmsg);
        }
    });
    // TODO: 管理上传用户头像表单的行为
    $("#form-avatar").submit(function (e) {
        e.preventDefault();
        // 模拟表单提交
        $(this).ajaxSubmit({
            "url": "/api/v1.0/user/avatar",
            "type": "post",
            "headers":{
                "X-CSRFToken": getCookie("csrf_token")
            },
            "success": function (resp) {
                if(resp.errno == "0"){
                    // 上传成功
                    // 设置用户头像img标签src
                    $("#user-avatar").attr("src", resp.data.avatar_url);
                }else if(resp.errno == "4101"){
                    //用户未登录，跳转到登录页面
                    location.href = "login.html"
                }else{
                    // 上传失败
                    alert(resp.errmsg);
                }
            }

        })
    });

    // TODO: 管理用户名修改的逻辑
    $("#form-name").submit(function (e) {
        e.preventDefault();

        // 获取参数
        var username = $("#user-name").val();

        if(!username){
            alert("请输入用户名！")
            return;
        }

        var params = {
            "username": username
        };

        // 请求用户名
        $.ajax({
            "url":"/api/v1.0/user/name",
            "type": "put",
            "data": JSON.stringify(params),
            "contentType": "application/json",
            "headers": {
                "X-CSRFToken": getCookie("csrf_token")
            },
            "success": function (resp) {
                if(resp.errno == "0"){
                    // 修改成功
                    showSuccessMsg();
                }else if(resp.errno == "4101"){
                    //用户未登录，跳转到登录页面
                    location.href = "login.html"
                }else{
                    // 修改失败
                    alert(resp.errmsg);
                }
            }
        })

    })

})

