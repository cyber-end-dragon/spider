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

import pandas as pd
from PyPDF2 import PdfReader
from docx import Document



class HuNanInfoParser(BaseParser):
    """
    湖南省药品监督管理局  hhttp://mpa.hunan.gov.cn/mpa/xxgk/zfxxgknew/c100812/c100827/cpzh/index.html
    """

    def start_requests(self):
        url = "http://mpa.hunan.gov.cn/mpa/xxgk/zfxxgknew/c100812/c100827/cpzh/index.html"
        yield feapder.Request(url=url, callback=self.parse_for_page)

    def parse_for_page(self, request, response):
        
        page_num = int(re.findall("createPageHTML\('paging',(\d+),", response.text)[0])
        base_url = "http://mpa.hunan.gov.cn/mpa/xxgk/zfxxgknew/c100812/c100827/cpzh/index_{}.html"
        # base_url = "http://mpa.hunan.gov.cn/mpa/ylqx/xxgk_new_{}.html"

        yield feapder.Request(url=request.url, callback=self.parse)
        for i in range(2, page_num+1):
            page_url = base_url.format(i)
            yield feapder.Request(url=page_url, callback=self.parse)


    def parse(self, request, response):

        source = "器械召回.湖南省药品监督管理局"
        save_count = 0

        title_contents = response.xpath("//div[@class='main_right_text']//li")

        for title_content in title_contents:

            title = title_content.xpath("./a/span/text()").extract_first()
            url = title_content.xpath("./a/@href").extract_first()
                    
            item = InfoListItem()
            item.url = url
            item.id = get_uuid(item.url, source)
            item.raw = title_content
            item.release_time = title_content.xpath("./a/span/text()").extract_first()
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
    spider = tmp(redis_key="test_HuNanInfoParser", delete_keys=True)
    spider.add_parser(HuNanInfoParser)

    spider.start()