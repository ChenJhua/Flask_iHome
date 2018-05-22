//模态框居中的控制
function centerModals(){
    $('.modal').each(function(i){   //遍历每一个模态框
        var $clone = $(this).clone().css('display', 'block').appendTo('body');    
        var top = Math.round(($clone.height() - $clone.find('.modal-content').height()) / 2);
        top = top > 0 ? top : 0;
        $clone.remove();
        $(this).find('.modal-content').css("margin-top", top-30);  //修正原先已经有的30个像素
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    $('.modal').on('show.bs.modal', centerModals);      //当模态框出现的时候
    $(window).on('resize', centerModals);

    // TODO: 查询房客订单
    $.get("/api/v1.0/orders?role=lodger", function (resp) {
        if(resp.errno == "0"){
            // 查询成功
            var html = template("orders-list-tmpl", {"orders": resp.data});
            $(".orders-list").html(html);

            // TODO: 查询成功之后需要设置评论的相关处理
            $(".order-comment").on("click", function(){
                var orderId = $(this).parents("li").attr("order-id");
                $(".modal-comment").attr("order-id", orderId);
            });

            // 订单评论
            $(".modal-comment").click(function (resp) {
                // 获取订单id
                var orderId = $(this).attr("order-id");

                var comment = $("#comment").val();
                if(!comment){
                    alert("请输入评论信息！");
                    return;
                }

                var params = {
                    "comment": comment
                }

                $.ajax({
                    "url":"/api/v1.0/order/"+orderId+"/comment",
                    "type": "put",
                    "data": JSON.stringify(params),
                    "contentType": "application/json",
                    "headers": {
                        "X-CSRFToken": getCookie("csrf_token")
                    },
                    "success": function (resp) {
                        if(resp.errno == "0"){
                            // 评价成功
                            // 设置页面上的订单状态
                            $(".orders-list>li[order-id="+ orderId +"]>div.order-content>div.order-text>ul li:eq(4)>span").html("已完成");
                            // 隐藏评价按钮
                            $("ul.orders-list>li[order-id="+ orderId +"]>div.order-title>div.order-operate").hide();
                            // 隐藏弹出框
                            $("#comment-modal").modal("hide");
                        }else if(resp.errno == "4101"){
                            location.href = "login.html"
                        }else{
                            // 评价失败
                            alert(resp.errmsg);
                        }
                    }
                })

            });

        }else if(resp.errno == "4101"){
            location.href = "login.html";
        }else{
            // 查询失败
            alert(resp.errmsg);
        }

    });


});
