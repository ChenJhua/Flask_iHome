# coding=utf-8
import redis
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


class Config(object):
    """配置类"""
    DEBUG = True
    # mysql数据库相关配置
    # 设置数据库的链接地址
    SQLALCHEMY_DATABASE_URI = "mysql://root:mysql@192.168.158.136:3306/ihome_sz08"
    # 关闭追踪数据库的修改
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # redis数据库配置
    REDIS_HOST = "192.168.158.136"
    REDIS_PORT = 6379



app = Flask(__name__)
app.config.from_object(Config)


# 创建SQLAlchemy对象
db = SQLAlchemy(app)
# 创建redis连接对象
redis_store = redis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT)


@app.route("/")
def index():
    # 测试redis
    redis_store.set("name", "itcast")
    return "index"


if __name__ == "__main__":
    app.run()

