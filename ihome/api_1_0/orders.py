# coding=utf-8
# 此文件中定义和订单相关api接口
import datetime

from flask import current_app
from flask import request, jsonify

from ihome import db
from ihome.models import House, Order
from ihome.utils.commons import login_required
from ihome.utils.response_code import RET
from . import api


@api.route("/orders", methods=["POST"])
@login_required
def save_order_info():
    """
    创建房屋预订订单：
    1.接收参数(房屋id,起始时间,结束时间)并进行参数验证
    2.根据房屋id查询房屋的信息(如果查不到，说明房屋不存在)
    3.创建一个Order对象并保存订单信息
    4.将订单信息添加进数据库
    5.返回应答，订单创建成功
    :return:
    """
    # 1.接收参数(房屋id,起始时间,结束时间)并进行参数验证
    req_dict = request.json
    house_id = req_dict.get("house_id")
    start_date = req_dict.get("start_date")
    end_date = req_dict.get("end_date")

    if not all([house_id, start_date, end_date]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数不完整")

    try:
        # 处理搜索时间
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        assert start_date < end_date, Exception("搜索起始时间大于结束时间")
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    # 2.根据房屋id查询房屋的信息(如果查不到，说明房屋不存在)
    try:
        house = House.query.get(house_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="查询房屋信息失败")

    if not house:
        return jsonify(errno=RET.NODATA, errmsg="房屋信息未找到")
    # 3.创建一个Order对象并保存订单信息
    order = Order()
    days = (end_date - start_date).days  # timedelat
    order.user_id = g.user_id
    order.house_id = house_id
    order.begin_date = start_date
    order.end_date = end_date
    order.days = days
    order.house_price = house.price
    order.amount = days * house.price

    # 房屋预订量+1
    house.order_count += 1
    # 4.将订单信息添加进数据库
    try:
        db.session.add(order)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="保存订单信息失败")
    # 5.返回应答，订单创建成功
    return jsonify(errno=RET.OK, errmsg="房屋预订成功")





