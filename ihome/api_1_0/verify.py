# coding=utf-8
# 次文件中api用于提供图片验证码和短信验证码
from . import api
from ihome import redis_store
from ihome.utils.captcha import captcha
from ihome.constants import IMAGE_CODE_REDIS_EXPIRES
from flask import make_response, request, jsonify
from ihome.utils.response_code import RET


@api.route("/image_code")
def get_image_code():
    """
    产生图片验证码
    1.接收参数（图片验证码标识）并进行校验
    2.生成图片验证码
    3.再redis中保存图片验证码
    4.返回验证码图片
    """

    # 1.接收参数（图片验证码标识）并进行校验
    image_code_id = request.args.get("cur_id")
    if not image_code_id:
        return jsonify(errno=RET.PARAMERR, errmsg='缺少参数')
    # 2.生成图片验证码
    # 产生图片验证码
    # 文本名称 验证码文本 验证码图片内容
    name, text, content = captcha.captcha.generate_captcha()

    # 3.再redis中保存图片验证码
    # redis_store.set("key", "value", "expires")
    try:
        redis_store.set("imagecode:%s" % image_code_id, text, IMAGE_CODE_REDIS_EXPIRES)
    except Exception as e:
        print e
        return jsonify(error=RET.DBERR, errmsg="保存图片验证码失败")
    # 4.返回验证码图片
    response = make_response(content)
    # 指定返回内容的类型
    response.headers['Content-Type'] = 'image/jpg'

    return response


