# coding=utf-8
# 此文件定义和房屋相关api接口
from flask import current_app, jsonify

from ihome.models import Area
from ihome.utils.response_code import RET
from . import api


@api.route("/areas")
def get_areas_info():
    """
    获取所有城区信息：
    1. 获取所有城区信息
    2. 组织数据，返回应答
    :return:
    """
    # 1. 获取所有城区信息
    try:
        areas = Area.query.all()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="获取城区信息失败")

    # 2. 组织数据，返回应答
    areas_dict_li = []
    for area in areas:
        areas_dict_li.append(area.to_dict())

    return jsonify(errno=RET.OK, errmsg="OK", data=areas_dict_li)


