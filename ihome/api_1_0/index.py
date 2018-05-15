# coding=utf-8
from . import api


# 2.使用蓝图对象注册路由
@api.route("/", methods=["GET", "POST"])
def index():
    # 测试redis
    # redis_store.set("name", "itcast")

    # 测试session存储
    # session["name"] = "itheima"
    return "index"
