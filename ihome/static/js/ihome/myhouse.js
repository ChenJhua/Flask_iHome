$(document).ready(function(){
    // TODO: 对于发布房源，只有认证后的用户才可以，所以先判断用户的实名认证状态
    $.get("/api/v1.0/user/auth", function (resp) {
        if(resp.errno == "0"){
            // 获取实名认证成功
            if(resp.data.real_name && resp.data.id_card){
                // 已实名认证
                // TODO: 如果用户已实名认证,那么就去请求之前发布的房源
                $.get("/api/v1.0/user/houses", function (resp) {
                    if(resp.errno == "0"){
                        var html = template("houses-list-tmpl", {"houses": resp.data})
                        $(".houses-list").html(html)
                    }else if(resp.errno == "4101"){
                        location.href = "login.html"
                    }else{
                        // 获取实名认证失败
                        alert(resp.errmsg);
                    }
                })
            }else{
                // 未实名认证
                $(".auth-warn").show();
            }

        }else if(resp.errno == "4101"){
            location.href = "login.html"
        }else{
            // 获取实名认证失败
            alert(resp.errmsg);
        }

    });



});
