# coding=utf-8
# 此文件中定义和用户登录，注册有关的api
from flask import current_app

from ihome import redis_store, db
from ihome.models import User
from ihome.utils.response_code import RET
import re
from . import api
from flask import request, jsonify


@api.route("/users", methods=["POST"])
def register():
    """
    用户注册功能：
    1. 接收参数（手机号，短信验证码，密码）并进行参数校验
    2. 从redis获取短信验证码（如果取不到，说明短信验证码已过期）
    3. 对比短信验证码，如果一致
    4. 创建User对象并保存注册用户的信息
    5. 把注册用户的信息添加进数据库
    6. 返回应答，注册成功
    :return:
    """

    # 1. 接收参数（手机号，短信验证码，密码）并进行参数校验
    req_dict = request.json
    mobile = req_dict.get("mobile")
    sms_code = req_dict.get("sms_code")
    password = req_dict.get("password")

    if not all([mobile, sms_code, password]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数不完整")
    if not re.match(r"^1[356789]\d{9}", mobile):
        return jsonify(errno=RET.PARAMERR, errmsg="手机号格式不正确")

    # 2. 从redis获取短信验证码（如果取不到，说明短信验证码已过期）
    try:
        real_sms_code = redis_store.get("smscode:%s" % mobile)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="获取短信验证码失败")
    if not real_sms_code:
        return jsonify(errno=RET.NODATA, errmsg="短信验证码已过期")
    # 3. 对比短信验证码，如果一致
    if real_sms_code != sms_code:
        return jsonify(errno=RET.DATAERR, errmsg="短信验证码错误")
    # 4. 创建User对象并保存注册用户的信息
    user = User()
    user.mobile = mobile
    user.name = mobile
    # todo:注册密码的加密

    # 5. 把注册用户的信息添加进数据库
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="保存注册用户信息失败")
    # 6. 返回应答，注册成功
    return jsonify(errno=RET.OK, errmsg="注册成功")