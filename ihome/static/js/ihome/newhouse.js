function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    // $('.popup_con').fadeIn('fast');
    // $('.popup_con').fadeOut('fast');

    // TODO: 在页面加载完毕之后获取区域信息
    $.get("/api/v1.0/areas", function (resp) {
        if(resp.errno == "0"){
            // 获取城区信息成功
            var areas = resp.data;

            // 遍历城区信息到城区下拉列表框中
            for(var i=0; i<areas.length;i++){
                var area = areas[i];

                var html = '<option value="'+area.id+'">' +area.aname+'</option>';
                $("#area-id").append(html);
            }
        }else{
            // 获取城区信息失败
            alert(resp.errmsg);
        }

    });

    // TODO: 处理房屋基本信息提交的表单数据

    // TODO: 处理图片表单的数据

})