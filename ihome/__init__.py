# coding=utf-8
import redis
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from config import config_dict


# 工厂方法
def create_app(config_name):
    app = Flask(__name__)
    config_cls = config_dict[config_name]
    app.config.from_object(config_cls)

    # 创建SQLAlchemy对象
    db = SQLAlchemy(app)
    # 创建redis连接对象
    redis_store = redis.StrictRedis(host=config_cls.REDIS_HOST, port=config_cls.REDIS_PORT)
    # 开启CSRF保护
    # 只做保护校验：至于生成csrf_token cookie还有请求时携带csrf_token需要自己来完成
    CSRFProtect(app)

    # session信息存储
    Session(app)

    return app



