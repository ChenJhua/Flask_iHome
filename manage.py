# coding=utf-8
import redis
from flask import Flask, session
from flask.ext.migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from flask_script import Manager


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
    SECRET_KEY = "1231KJ!@#!@#!#!&$%!@^%#!@^$!@^$!(^$*(!@*(&#)!*&)&"

    # session存储配置，设置session信息存储到redis数据库中
    SESSION_TYPE = "redis"
    # 设置session存储到那个redis数据库中
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    # 开启session签名，加密
    # SESSION_USE_SIGNER = True
    # 设置session过期时间
    PERMANENT_SESSION_LIFETIME = 86400 * 2


app = Flask(__name__)
app.config.from_object(Config)


# 创建SQLAlchemy对象
db = SQLAlchemy(app)
# 创建redis连接对象
redis_store = redis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT)
# 开启CSRF保护
# 只做保护校验：至于生成csrf_token cookie还有请求时携带csrf_token需要自己来完成
CSRFProtect(app)

# session信息存储
Session(app)

# 创建Manager管理对象
manager = Manager(app)
Migrate(app, db)
# 添加迁移命令
manager.add_command("db", MigrateCommand)


@app.route("/", methods=["GET", "POST"])
def index():
    # 测试redis
    # redis_store.set("name", "itcast")

    # 测试session存储
    session["name"] = "itheima"
    return "index"


if __name__ == "__main__":
    manager.run()

