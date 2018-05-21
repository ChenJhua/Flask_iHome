# coding=utf-8
# 此文件定义和房屋相关api接口
import json
from flask import current_app, jsonify
from flask import g
from flask import request
from flask import session

from ihome import constants, redis_store
from ihome import db
from ihome.models import Area, House, Facility, HouseImage
from ihome.utils.commons import login_required
from ihome.utils.image_storage import storage_image
from ihome.utils.response_code import RET
from . import api


@api.route("/houses")
def get_house_list():
    """
    搜索房屋的信息
    :return:
    """
    aid = request.args.get("aid")  # 城区id
    # new：最新上线 booking：入住最多  price-inc： 价格低->高  price-des：价格高->低
    sort_key = request.args.get("sk")  # 排序方式,默认按照最新上线排序
    page = request.args.get("p", 1)  # 页码

    try:
        page = int(page)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    try:
        if aid:
            aid = int(aid)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    # 获取所有房屋的信息
    try:
        houses_query = House.query
        # 根据城区id对房屋信息进行过滤
        if aid:
            houses_query = houses_query.filter(House.area_id == aid)  # BaseQuery
        # 对查询结果排序
        if sort_key == "booking":
            # 按照房屋订单数量排序
            houses_query = houses_query.order_by(House.order_count.desc())
        elif sort_key == "price-inc":
            # 价格低->高
            houses_query = houses_query.order_by(House.price)
        elif sort_key == "price-des":
            # 价格高->低
            houses_query = houses_query.order_by(House.price.desc())
        else:
            # 按照最新上线进行排序
            houses_query = houses_query.order_by(House.create_time.desc())

        # 进行分页操作
        paginate = houses_query.paginate(page, constants.HOUSE_LIST_PAGE_CAPACITY, False)

        # 获取搜索结果
        houses = paginate.items
        total_page = paginate.pages  # 分页之后总页数
        current_page = paginate.page  # 当前页码
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="获取房屋信息失败")
    # 组织数据，返回应答
    house_dict_li = []
    for house in houses:
        house_dict_li.append(house.to_basic_dict())

    resp = {
        "houses": house_dict_li,
        "total_page": total_page,
        "current_page": current_page,
    }
    return jsonify(errno=RET.OK, errmsg="OK", data=resp)


@api.route("/house/index")
def get_house_index():
    """
    获取首页展示房屋的信息
    1.获取房屋的信息，按照房屋发布时间进行排序，默认展示前5个
    2.组织数据，返回应答
    :return:
    """
    # 1.获取房屋的信息，按照房屋发布时间进行排序，默认展示前5个
    try:
        houses = House.query.order_by(House.create_time.desc()).limit(constants.HOME_PAGE_MAX_HOUSES).all()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="获取首页房屋信息失败")
    # 2.组织数据，返回应答
    house_dict_li = []
    for house in houses:
        house_dict_li.append(house.to_basic_dict())
    return jsonify(errno=RET.OK, errmsg="OK", data=house_dict_li)


@api.route("/house/<int:house_id>")
def get_house_detail(house_id):
    """
    获取房屋的详情信息
    1.根据房屋id查询房屋信息
    2.组织数据，返回应答
    :param house_id:
    :return:
    """
    # 1.根据房屋id查询房屋信息
    try:
        house = House.query.get(house_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="获取房屋信息失败")

    if not house:
        return jsonify(errno=RET.NODATA, errmsg="房屋信息不存在")

    # 2.组织数据，返回应答
    # 尝试从session中获取user_id
    # 如果用户登录，获取的登录用户的id，如果未登录返回-1
    user_id = session.get("user_id", -1)
    return jsonify(errno=RET.OK, errmsg="OK", data={"house": house.to_full_dict(), "user_id": user_id})


@api.route("/house/image", methods=["POST"])
def save_house_image():
    """
    保存上传房屋图片：
    1.接收房屋id和房屋图片对象
    2.根据房屋id获取房屋信息（如果获取不到，说明房屋不存在）
    3.将房屋的图片上传到七牛云
    4.创建HouseImage对象并保存房屋图片记录
    5. 返回应答， 上传成功
    :return:
    """
    # 1.接收房屋id和房屋图片对象
    house_id = request.form.get("house_id")
    file = request.files.get("house_image")

    if not all([house_id, file]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数不完整")
    # 2.根据房屋id获取房屋信息（如果获取不到，说明房屋不存在）
    try:
        house = House.query.get(house_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="获取房屋信息失败")

    if not house:
        return jsonify(errno=RET.NODATA, errmsg="房屋信息不存在")

    # 3.将房屋的图片上传到七牛云
    try:
        key = storage_image(file.read())
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="上传房屋图片失败")
    # 4.创建HouseImage对象并保存房屋图片记录
    house_image = HouseImage()
    house_image.house_id = house_id
    house_image.url = key

    # 判断房屋是否设置了默认图片
    if not house.index_image_url:
        house.index_image_url = key

    try:
        db.session.add(house_image)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="保存房屋图片信息失败")
    # 5. 返回应答， 上传成功
    img_url = constants.QINIU_DOMIN_PREFIX + key
    return jsonify(errno=RET.OK, errmsg="上传房屋图片成功", data={"img_url": img_url})


@api.route("/houses", methods=["POST"])
@login_required
def save_house_info():
    """
    保存发布房屋的信息：
    1. 接收参数并进行参数校验
    2. 创建House对象并保存房屋的基本信息
    3. 将房屋信息存进数据库
    4. 返回应答，发布房屋信息成功
    :return:
    """
    # 1. 接收参数并进行参数校验
    req_dict = request.json

    title = req_dict.get('title')
    price = req_dict.get('price')
    address = req_dict.get('address')
    area_id = req_dict.get('area_id')
    room_count = req_dict.get('room_count')
    acreage = req_dict.get('acreage')
    unit = req_dict.get('unit')
    capacity = req_dict.get('capacity')
    beds = req_dict.get('beds')
    deposit = req_dict.get('deposit')
    min_days = req_dict.get('min_days')
    max_days = req_dict.get('max_days')

    if not all([title, price, address, area_id, room_count, acreage, unit, capacity, beds, deposit, min_days, max_days]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数不完整')
    try:
        # 数据库中房屋单价和押金 以 分 为单位保存
        price = int(float(price)*100)
        deposit = int(float(deposit)*100)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")
    # 2. 创建House对象并保存房屋的基本信息
    house = House()

    house.user_id = g.user_id
    house.area_id = area_id
    house.title = title
    house.price = price
    house.address = address
    house.room_count = room_count
    house.acreage = acreage
    house.unit = unit
    house.capacity = capacity
    house.beds = beds
    house.deposit = deposit
    house.min_days = min_days
    house.max_days = max_days

    # 获取房屋的设施信息
    facility = req_dict.get("facility")
    if facility:
        # 获取房屋设施的信息
        try:
            facilities = Facility.query.filter(Facility.id.in_(facility)).all()
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(errno=RET.DBERR, errmsg="获取房屋设施失败")
        # 设置房屋设施信息
        house.facilities = facilities

    # 3. 将房屋信息存进数据库
    try:
        db.session.add(house)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="保存房屋信息失败")
    # 4. 返回应答，发布房屋信息成功
    return jsonify(errno=RET.OK, errmsg="发布房屋信息成功", data=house.to_basic_dict())


@api.route("/areas")
def get_areas_info():
    """
    获取所有城区信息：
    1. 获取所有城区信息
    2. 组织数据，返回应答
    :return:
    """
    try:
        # 先尝试从redis缓存中获取缓存的城区信息
        area_str = redis_store.get("areas")
        print("从redis中取")
        # 如果获取到，直接返回，如果获取不到，查询数据库
        if area_str:
            return jsonify(errno=RET.OK, errmsg="OK", data=json.loads(area_str))
    except Exception as e:
        current_app.logger.error(e)

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
    # 缓存城区信息到redis中
    try:
        redis_store.set("areas", json.dumps(areas_dict_li), constants.AREA_INFO_REDIS_EXPIRES)
    except Exception as e:
        current_app.logger.error(e)

    return jsonify(errno=RET.OK, errmsg="OK", data=areas_dict_li)


