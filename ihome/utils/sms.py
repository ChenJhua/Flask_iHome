# coding=utf-8
import ConfigParser
from ihome.libs.yuntongxun.CCPRestSDK import REST

accountSid = '8aaf070863399ed9016359ba4fed1500'
# 说明：主账号，登陆云通讯网站后，可在控制台首页中看到开发者主账号ACCOUNT SID。

accountToken = '7fb853c525834e67bc8337d7299673ed'
# 说明：主账号Token，登陆云通讯网站后，可在控制台首页中看到开发者主账号AUTH TOKEN。

appId = '8aaf070863399ed9016359ba50471507'
# 请使用管理控制台中已创建应用的APPID。

serverIP = 'app.cloopen.com'
# 说明：请求地址，生产环境配置成app.cloopen.com。

serverPort = '8883'
# 说明：请求端口 ，生产环境为8883.

softVersion = '2013-12-26'  # 说明：REST API版本号保持不变。


class CCP(object):

    def __new__(cls, *args, **kwargs):
        # 判断cls是否拥有属性_instance,此属性用来保存这个类的唯一对象(单例对象)
        if not hasattr(cls, "_instance"):
            # 创建一个对象
            obj = super(CCP, cls).__new__(cls, *args, **kwargs)
            # 初始化REST SDK
            obj.rest = REST(serverIP, serverPort, softVersion)
            obj.rest.setAccount(accountSid, accountToken)
            obj.rest.setAppId(appId)
            cls._instance = obj

        # 直接返回
        return cls._instance

    # def __init__(self):


    def send_template_sms(self, to, datas, tempId):

        result = self.rest.sendTemplateSMS(to, datas, tempId)
        if result.get("statusCode") == "000000":
            return 1
        else:
            return 0
        # print result
        # for k, v in result.iteritems():
        #     if k == 'templateSMS':
        #         for k, s in v.iteritems():
        #             print '%s:%s' % (k, s)
        #     else:
        #         print '%s:%s' % (k, v)
