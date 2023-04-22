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


class FuJianInfoParser(BaseParser):
    """
    福建省药品监督管理局  https://yjj.scjgj.fujian.gov.cn/ylqx/gstg/
    """

    def start_requests(self):
        url = "https://yjj.scjgj.fujian.gov.cn/ylqx/gstg/"
        yield feapder.Request(url=url, callback=self.parse_for_page)

    def parse_for_page(self, request, response):
        
        record_num = int(re.findall("recordCount: '(\d+)'", response.text)[0])
        search_url = "https://yjj.scjgj.fujian.gov.cn/fjdzapp/search"
        # from_data = channelid: 229105
 
        page_num = record_num//75
        if record_num/75 > page_num:
            page_num += 1
        # page_num = 2

        from_data = {
            "channelid": "229105",
            "sortfield": "-docorderpri,-docreltime",
            "classsql": "chnlid=4910",
            "classcol": "publishyear",
            "classnum": "100",
            "classsort": "0",
            "cache": "true",
            "page": "1",
            "prepage": "75"
        }

        for i in range(1, page_num+1):

            post_data = copy.deepcopy(from_data)
            post_data["page"] = str(i)
            yield feapder.Request(url=search_url, data=post_data, callback=self.parse)

    def parse(self, request, response):

        source = "飞行检查.福建省药品监督管理局"
        save_count = 0
        filter_word1 = ["公司", "厂", "飞行检查"]
        filter_word2 = ["医疗器械", "监督检查"]
        title_contents = response.json["data"]

        for title_content in title_contents:

            title = title_content["doctitle"]
            url = title_content["chnldocurl"]
            condj = [any(ext in title for ext in filter_word1[:2]) and (filter_word1[2] in title), all(ext in title for ext in filter_word2)]
            if not condj[0]:
                if not condj[1]:
                    continue
                else:
                    if  not self.parse_content(url, "飞行检查"):
                        continue

            item = InfoListItem()
            item.url = url
            item.id = get_uuid(item.url, source)
            item.raw = title_content
            item.release_time = title_content["docreltime"]
            item.source = source
            item.title = title

            # print(item)
            yield item

            save_count += 1

        log.info("[{}]扫描到{}条列表".format(source, save_count))

    def parse_content(self, url, word):

        resp = feapder.Request(url).get_response()
        soup = resp.bs4()
        text = soup.get_text()

        if word in text:
            return True
        return False


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
    spider = tmp(redis_key="test_FuJianInfoParser", delete_keys=True)
    spider.add_parser(FuJianInfoParser)

    spider.start()