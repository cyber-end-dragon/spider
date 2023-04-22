'''
Author: Paulus
Date: 2023-03-16 10:23:40
LastEditTime: 2023-04-11 20:50:34
LastEditors: Paulus
FilePath: /spiders/base.py
Description: 请输入文件描述
'''
import feapder
from setting import CUSTOM_PROXY


class BaseProxy(object):
    def download_midware(self, request):
        request.proxies = CUSTOM_PROXY
        return request


class BaseAirSpider(BaseProxy, feapder.AirSpider):
    pass


class BaseSpider(BaseProxy, feapder.Spider):
    pass


class BaseTaskSpider(BaseProxy, feapder.TaskSpider):
    pass


class BatchBaseSpider(BaseProxy, feapder.BatchSpider):
    pass


class BaseParser(feapder.BaseParser):
    def download_midware(self, request):
        request.proxies = CUSTOM_PROXY
        return request
