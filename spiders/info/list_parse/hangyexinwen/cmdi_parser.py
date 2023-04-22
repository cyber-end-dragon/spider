# -*- coding: utf-8 -*-
import sys
if __name__ == "__main__":
    sys.path.append("../../../../")
import feapder
import re
import requests
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

from io import BytesIO
import struct
import zipfile
import pandas as pd
from PyPDF2 import PdfReader

class CmdiInfoParser(BaseParser):
    """
    中国医疗器械信息网  https://www.cmdi.org.cn/zx_4/xyzl/
    """

    def start_requests(self):
        url = "https://www.cmdi.org.cn/zx_4/xyzl/"
        yield feapder.Request(url=url, callback=self.parse_for_page)

    def parse_for_page(self, request, response):

        page_num = int(re.findall(r"countPage = (\d+)", response.text)[0])
        base_url = "https://www.cmdi.org.cn/zx_4/xyzl/index_{}.html"

        page_num = 2
        for i in range(page_num):

            page_url = base_url.format(i)
            if i == 0:
                page_url = "https://www.cmdi.org.cn/zx_4/xyzl/index.html"
            yield feapder.Request(url=page_url, callback=self.parse)




    def parse(self, request, response):

        source = "行业新闻.中国医疗器械信息网"
        save_count = 0
        title_contents = response.xpath("//ul[@class='rightList']/li")

        for title_content in title_contents:

            item = InfoListItem()
            item.title = title_content.xpath("./a/text()").extract_first().strip()
            item.url = title_content.xpath("./a/@href").extract_first()
            item.raw = title_content.get()
            item.release_time = title_content.xpath("./span/text()").extract_first()
            item.source = source

            print(item)
            # yield item

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
    spider = tmp(redis_key="test_CmdiInfoParser", delete_keys=True)
    spider.add_parser(CmdiInfoParser)

    spider.start()