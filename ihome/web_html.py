# coding=utf-8
# 此蓝图给浏览器提供静态页面
from flask import Blueprint
from flask import current_app
from flask import make_response
from flask.ext.wtf.csrf import generate_csrf

html = Blueprint("html", __name__)


# 当浏览器访问一个网站的时候，浏览器会自动访问网站下的一个文件favicon.ico为了获取网站的图标
# http://127.0.0.1:5000/favicon.ico
@html.route("/<re('.*'):file_name>")
def get_static_html(file_name):
    # 获取静态文件目录下方对应的静态文件的内容并返回给浏览器
    # print(file_name)
    if file_name == "":
        # 说明用户访问的是跟路径，默认返回index.html
        file_name = "index.html"
    # print(file_name)
    if file_name != "favicon.ico":
        file_name = "html/" + file_name
    # print(file_name)

    # return current_app.send_static_file(file_name)
    response = make_response(current_app.send_static_file(file_name))
    # 生成一个csrf_token cookie
    csrf_token = generate_csrf()
    response.set_cookie("csrf_token", csrf_token)

    return response




