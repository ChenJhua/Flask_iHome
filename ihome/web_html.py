# coding=utf-8
# 此蓝图给浏览器提供静态页面
from flask import Blueprint
from flask import current_app


html = Blueprint("html", __name__)


@html.route("/<file_name>")
def get_static_html(file_name):
    # 获取静态文件目录下方对应的静态文件的内容并返回给浏览器
    file_name = "html/" + file_name

    return current_app.send_static_file(file_name)




