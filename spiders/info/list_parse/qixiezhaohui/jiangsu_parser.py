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


class JiangSuInfoParser(BaseParser):
    """
    江苏省药品监督管理局  http://da.jiangsu.gov.cn/col/col84692/index.html
    """

    def start_requests(self):
        url = "http://da.jiangsu.gov.cn/col/col84692/index.html"
        yield feapder.Request(url=url, callback=self.parse_for_page)

    def parse_for_page(self, request, response):
        
        page_record = int(re.findall(r"totalRecord:(\d+)((?!totalRecord).)*?dataStore", response.text)[0][0])
        sec_record = 45
        page_num = page_record // sec_record
        remain_record = page_record % sec_record
        base_url = "http://da.jiangsu.gov.cn/module/web/jpage/dataproxy.jsp?startrecord={}&endrecord={}&perpage=15"

        headers = {
            # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'Host': 'da.jiangsu.gov.cn',
            'Origin': 'http://da.jiangsu.gov.cn',
            'Referer': 'http://da.jiangsu.gov.cn/col/col84692/index.html?uid=374104&pageNum=1',
        }
        from_data = {
            "col": "15",
            "appid": "1",
            "webid": "18",
            "path": "/",
            "columnid": "84692",
            "sourceContentType": "1",
            "unitid": "374104",
            "webname": "江苏省药品监督管理局",
            "permissiontype": "0"
        }

        # page_num = 1

        for i in range(1, page_num+1):
            page_url = base_url.format((i-1)*sec_record+1, i*sec_record)
            yield feapder.Request(url=page_url, headers=headers, data=from_data, callback=self.parse)

        if remain_record:
            page_url = base_url.format(page_num*sec_record+1, page_record)
            yield feapder.Request(url=page_url, headers=headers, data=from_data, callback=self.parse)


    def parse(self, request, response):

        # print(response.text)

        source = "器械召回.江苏省药品监督管理局"
        save_count = 0
        title_contents = re.findall(r"<record>([\s\S]*?)<\/record>", response.text)


        for title_content in title_contents[:45]:

            title = re.findall(r"<\/b>(.*?)<\/a>", title_content)[0]
            url = re.findall(r'href="(.*?)"', title_content)[0]

            item = InfoListItem()
            item.url = url
            item.id = get_uuid(item.url, source)
            item.raw = title_content
            item.release_time = re.findall(r">(.*?)<\/font>", title_content)[0]
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
    spider = tmp(redis_key="test_JiangSuInfoParser", delete_keys=True)
    spider.add_parser(JiangSuInfoParser)

    spider.start()