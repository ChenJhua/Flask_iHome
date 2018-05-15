# coding=utf-8
from flask import Blueprint
# 1.创建蓝图对象
api = Blueprint("api", __name__)

from . import index, verify
