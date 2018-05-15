# coding=utf-8
# 自定义工具类或者工具函数
from werkzeug.routing import BaseConverter


class RegexConvter(BaseConverter):
    """自定义路由转换器类"""
    def __init__(self, url_map, regex):
        super(RegexConvter, self).__init__(url_map)
        # 保存转换器匹配规则
        self.regex = regex

