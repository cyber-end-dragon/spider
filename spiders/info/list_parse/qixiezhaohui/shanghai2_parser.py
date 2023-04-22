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
import time
from bs4 import BeautifulSoup
from feapder.utils.tools import get_uuid, get_full_url, parse_url_params
from feapder.utils.log import log
from feapder.utils.webdriver import PlaywrightDriver, InterceptResponse, InterceptRequest
from feapder.utils.tools import parse_url_params
from spiders.base import BaseParser


class ShangHaiInfoParser(BaseParser):
    """
    上海市药品监督管理局  https://yjj.sh.gov.cn/ylqxzdzh/index.html
    """

    def start_requests(self):

        url = "https://qxzh.yjj.sh.gov.cn/openApi/queryRecallPublic"
        yield feapder.Request(url=url, page="1", callback=self.parse_for_page)

    def download_midware(self, request):

        time_stamp = int(time.time()*1000)
        time_date = time.strftime("%Y-%m-%d", time.localtime())

        params = {
                "recall.recallNum": "",
                "recall.enpName": "",
                "recallEvent.passNum": "",
                "recallEvent.productName": "",
                "startDateStr": "2022-1-1",
                "endDateStr": time_date,
                "isAuditPassed": "1",
                "search": "false",
                "nd": time_stamp,
                "rows": "10",
                "page": str(request.page),
                "sidx": "",
                "sord": "desc",
                "totalrows": "2000"
            }

        request.params = params

        return request

    def parse_for_page(self, request, response):
        
        page_num = response.json["total"]
        url = "https://qxzh.yjj.sh.gov.cn/openApi/queryRecallPublic"

        # page_num = 1
        
        for i in range(1, page_num+1):

            yield feapder.Request(url=url, page=i, callback=self.parse)

    def parse(self, request, response):

        source = "器械召回.上海市药品监督管理局"
        save_count = 0
        title_contents = response.json["rows"]

        for title_content in title_contents:

            title = title_content["recall"]["enpName"] + title_content["recallEvent"]["produceName"]

            item = InfoListItem()
            item.url = "https://qxzh.yjj.sh.gov.cn/openApi/recallDetail?recall.recallId=" + title_content["recall"]["recallId"]
            item.id = get_uuid(item.url, source)
            item.raw = json.dumps(title_content)
            item.release_time = title_content["recallEvent"]["reportDate"]
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
    spider = tmp(redis_key="test_ShangHaiInfoParser", delete_keys=True)
    spider.add_parser(ShangHaiInfoParser)

    spider.start()