# coding=utf-8
import redis


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
