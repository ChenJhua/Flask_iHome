# coding=utf-8
from flask import current_app

from . import api
from ihome import redis_store
import logging


# 2.使用蓝图对象注册路由
@api.route("/", methods=["GET", "POST"])
def index():
    # 测试redis
    redis_store.set("name", "itcast")

    # 测试session存储
    # session["name"] = "itheima"

    # 测试日志功能
    # logging.fatal("Fatal Message")
    # logging.error("Error Message")
    # logging.warning("Warning Message")
    # logging.info("Info Message")
    # logging.debug("Debug Message")

    # current_app.logger.fatal("Fatal Message")
    # current_app.logger.error("Error Message")
    # current_app.logger.warning("Warning Message")
    # current_app.logger.info("Info Message")
    # current_app.logger.debug("Debug Message")

    return "index"
