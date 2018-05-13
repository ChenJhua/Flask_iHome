# coding=utf-8
import redis
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
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



