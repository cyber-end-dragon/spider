# -*- coding: utf-8 -*-
import sys

if __name__ == "__main__":
    sys.path.append("../../../../")
import feapder
import re
import json
import time
from pprint import pprint
from items.info_list_item import InfoListItem
import feapder
import re
from bs4 import BeautifulSoup
from feapder.utils.tools import get_uuid, get_full_url, parse_url_params
from feapder.utils.log import log
from feapder.utils.webdriver import PlaywrightDriver, InterceptResponse, InterceptRequest
from feapder.utils.tools import parse_url_params
from spiders.base import BaseParser

import copy
from requests_toolbelt import MultipartEncoder

class ShenChaInfoParser(BaseParser):
    """
    国家审查中心  https://www.cfdi.org.cn/cfdi/index?module=A001&m1=10&m2=&nty=A25
    """

    def start_requests(self):
        url = "https://www.cfdi.org.cn/cfdi/index?module=A001&m1=10&m2=&nty=A25"
        yield feapder.Request(url=url, callback=self.parse_for_page)

    def parse_for_page(self, request, response):
        
        nty = re.findall('"nty" value="(.*?)"', response.text)[0]
        name = re.findall('"name" value="(.*?)"', response.text)[0]
        total_pages = re.findall('"total_pages" value="(\d+)"', response.text)[0]
        iTotal_length = re.findall('"iTotal_length" value="(.*?)"', response.text)[0]
        module = re.findall('"module" value="(.*?)"', response.text)[0]
        part = re.findall('"part" value="(.*?)"', response.text)[0]
        m1 = re.findall('"m1" value="(.*?)"', response.text)[0]
        tcode = re.findall('"tcode" value="(.*?)"', response.text)[0]
        m2 = re.findall('"m2" value="(.*?)"', response.text)[0]
        pk = re.findall('"pk" value="(.*?)"', response.text)[0]

        from_data = {
            'nty': nty,
            'name': name,
            'pageNo': '0',
            'total_pages': total_pages,
            'cur_page': '1',
            'iTotal_length': iTotal_length,
            'module': module,
            'part': part,
            'm1': m1,
            'tcode': tcode,
            'm2': m2,
            'pk': pk
            }
        
        headers = {
            'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryZXv3IsqWGWgcsCow',
            'Host': 'www.cfdi.org.cn',
            'Origin': 'https://www.cfdi.org.cn',
            'Referer': 'https://www.cfdi.org.cn/cfdi/index?module=A001&m1=10&m2=&nty=A25',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }

        url = "https://www.cfdi.org.cn/cfdi/index?module=A001&m1=10&m2=&nty=A25"

        for i in range(1, int(total_pages)+1):

            copy_dict = copy.deepcopy(from_data)
            copy_dict["pageNo"] = str(i)
            field = MultipartEncoder(copy_dict)

            copy_headers = copy.deepcopy(headers)
            copy_headers['Content-Type'] = field.content_type
 
            yield feapder.Request(url=url, headers=copy_headers, data=field, callback=self.parse)


    def parse(self, request, response):

        response.encoding="GBK"
        source = "飞行检查.国家审查中心"
        save_count = 0
        filter_word1 = ["医疗器械", "飞行检查"]
        title_contents = response.xpath("//div[@class='page-lst-box']//li")

        for title_content in title_contents:

            title = title_content.xpath("./a/p[@class='content']/text()").extract_first()
            if not(all(ext in title for ext in filter_word1)):
                continue

            item = InfoListItem()
            item.url = title_content.xpath("./a/@href").extract_first()
            item.id = get_uuid(item.url, source)
            item.raw = title_content.get()
            item.release_time = title_content.xpath("./a/p[@class='datatime']/text()").extract_first()
            item.source = source
            item.title = title

            # print(item)
            yield item

            save_count += 1
            

        log.info("[{}]扫描到{}条列表".format(source, save_count))


if __name__ == "__main__":
    tmp = feapder.Spider
    tmp.__custom_setting__ = dict(
        RENDER_DOWNLOADER="feapder.network.downloader.PlaywrightDownloader",
        SPIDER_THREAD_COUNT=1,
        SPIDER_SLEEP_TIME=[0, 2],
        SPIDER_MAX_RETRY_TIMES=3,
        PLAYWRIGHT=dict(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
            # 字符串 或 无参函数，返回值为user_agent
            # proxy=CUSTOM_TUNNEL,  # xxx.xxx.xxx.xxx:xxxx 或 无参函数，返回值为代理地址
            headless=True,  # 是否为无头浏览器
            driver_type="chromium",  # chromium、firefox、webkit
            timeout=10,  # 请求超时时间
            render_time=1,  # 渲染时长，即打开网页等待指定时间后再获取源码
            wait_until="networkidle",  # 等待页面加载完成的事件,可选值："commit", "domcontentloaded", "load", "networkidle"
            use_stealth_js=True,  # 使用stealth.min.js隐藏浏览器特征,
        ),
    )
    spider = tmp(redis_key="test_ShenChaInfoParser", delete_keys=True)
    spider.add_parser(ShenChaInfoParser)

    spider.start()