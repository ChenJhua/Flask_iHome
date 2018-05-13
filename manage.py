# coding=utf-8
import redis
from flask import Flask, session
from flask.ext.migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from flask_script import Manager
from config import Config


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

