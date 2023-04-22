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


class HeiLongJiangInfoParser(BaseParser):
    """
    黑龙江省药品监督管理局  http://mpa.hlj.gov.cn/mpa/c113667/list.shtml
    """

    def start_requests(self):
        url = "http://mpa.hlj.gov.cn/common/search/18f551ccae6e48caac76b2b71afe044d?_isAgg=true&_isJson=true&_pageSize=15&_template=index&_rangeTimeGte=&_channelName=&page=1"
        yield feapder.Request(url=url, callback=self.parse_for_page)

    def parse_for_page(self, request, response):
        
        total_record = int(response.json["data"]["total"])
        sec_record = int(response.json["data"]["rows"])
        page_num = total_record // sec_record
        if total_record % sec_record:
            page_num += 1

        # page_num = 1
        base_url = "http://mpa.hlj.gov.cn/common/search/18f551ccae6e48caac76b2b71afe044d?_isAgg=true&_isJson=true&_pageSize=15&_template=index&_rangeTimeGte=&_channelName=&page={}"
        for i in range(1, page_num+1):
            page_url = base_url.format(i)
            yield feapder.Request(url=page_url, callback=self.parse)

    def parse(self, request, response):

        source = "器械召回.黑龙江省药品监督管理局"
        save_count = 0
        title_contents = response.json["data"]["results"]

        for title_content in title_contents:

            title = title_content["title"]
            url = "http://mpa.hlj.gov.cn" + title_content["url"]
            if not ("召回" in title):
                continue
            if not ("医疗器械" in title_content["content"]):
                continue

            item = InfoListItem()
            item.url = url
            item.id = get_uuid(item.url, source)
            item.raw = title_content
            item.release_time = re.findall(r'(\d{4}-\d{2}-\d{2})', title_content["publishedTimeStr"])
            item.source = source
            item.title = title

            # print(item)
            yield item

            save_count += 1

        log.info("[{}]扫描到{}条列表".format(source, save_count))
    
    # def parse_content(self, url, word):

    #     resp = feapder.Request(url).get_response()
    #     soup = resp.bs4()
    #     text = soup.get_text()

    #     if word in text:
    #         return True
    #     return False


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
    spider = tmp(redis_key="test_HeiLongJiangInfoParser", delete_keys=True)
    spider.add_parser(HeiLongJiangInfoParser)

    spider.start()