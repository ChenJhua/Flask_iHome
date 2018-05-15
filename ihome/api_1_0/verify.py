# coding=utf-8
# 次文件中api用于提供图片验证码和短信验证码
from . import api
from ihome.utils.captcha import captcha
from flask import make_response


@api.route("/image_code")
def get_image_code():
    """产生图片验证码"""
    # 产生图片验证码
    # 文本名称 验证码文本 验证码图片内容
    name, text, content = captcha.generate_captcha()
    response = make_response(content)
    # 指定返回内容的类型
    response.headers["Content-Type"] = "image/jpg"

    return content


