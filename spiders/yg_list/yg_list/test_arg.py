import sys
import feapder
import re
import json
import time
import copy
from bs4 import BeautifulSoup
from feapder.utils.tools import get_uuid, get_full_url, parse_url_params
from feapder.utils.log import log
from feapder.utils.webdriver import PlaywrightDriver, InterceptResponse, InterceptRequest
from spiders.base import BaseParser
from items.yg_anhui_info_list_item import YgAnhuiInfoListItem



class Testparser(BaseParser):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        print(*args)
    def start_requests(self):

        url = "http://www.ahyycg.cn/index/notice.html?id=16"
        print(url)
        # yield feapder.Request(url=url, callback=self.parse_for_page)

    def parse_for_page(self, request, response):

        total_record = int(re.findall(r"总共(.*?)条", response.text)[0])
        total_page = total_record // 41
        if total_page % 41:
            total_page += 1
        page_url = "http://www.ahyycg.cn/index/notice.html?id=16&pageIndex={}"

        # total_page = 2
        for i in range(1, total_page+1):
            url = page_url.format(i)
            yield feapder.Request(url=url, callback=self.parse)



    def parse(self, request, response):
        
        title_contents = response.xpath("//div[@class='message-conten activet']//div[@class='message-item']")

        for title_content in title_contents:

            item = YgAnhuiInfoListItem()
            item.url = "http://www.ahyycg.cn" + re.findall(r"'(.*?)'", title_content.xpath("./@onclick").extract_first())[0]
            item.title = title_content.xpath(".//@title").extract_first()
            item.release_time = title_content.xpath("./div[@class='mi-right']/text()").extract_first()

            yield feapder.Request(url=item.url, callback=self.parse_detail, item=item)
    
    def parse_detail(self, request, response):

        if response.status_code != 200:
            raise Exception("response code not 200") 
        
        request.item.raw = response.text
        request.item.union_id = get_uuid(request.url, request.item.title)

        yield request.item




if __name__ == "__main__":
    from setting import CUSTOM_TUNNEL
    from spiders.base import BaseSpider
    tmp = BaseSpider
    tmp.__custom_setting__ = dict(
        LOG_LEVEL = "DEBUG",
        RENDER_DOWNLOADER="feapder.network.downloader.PlaywrightDownloader",
        SPIDER_THREAD_COUNT=1,
        SPIDER_SLEEP_TIME = [0, 2],
        SPIDER_MAX_RETRY_TIMES = 5,
        PLAYWRIGHT=dict(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",  # 字符串 或 无参函数，返回值为user_agent
            proxy=CUSTOM_TUNNEL,  # xxx.xxx.xxx.xxx:xxxx 或 无参函数，返回值为代理地址
            headless=True,  # 是否为无头浏览器
            driver_type="chromium",  # chromium、firefox、webkit
            timeout=10,  # 请求超时时间
            render_time=1,  # 渲染时长，即打开网页等待指定时间后再获取源码
            wait_until="networkidle",  # 等待页面加载完成的事件,可选值："commit", "domcontentloaded", "load", "networkidle"
            use_stealth_js=True,  # 使用stealth.min.js隐藏浏览器特征,
        ),
    )
    spider = tmp(redis_key="test_Anhui", delete_keys=True)
    spider.add_parser(Testparser)
    
    spider.start()
        