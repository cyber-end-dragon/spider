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
from items.yg_shaanxi_info_list_item import YgShaanxiInfoListItem



class Shaanxiparser(BaseParser):

    def start_requests(self):

        url = "http://www.sxsyxcg.com/HomePage/ShowListNew.aspx?CatalogId=3&TzggType=2&type=7"
        yield feapder.Request(url=url, callback=self.parse_for_page)

    def parse_for_page(self, request, response):

        cookie = response.headers["Set-Cookie"].split(";")[0]
        total_page = int(re.findall(r"共(.*?)页", response.text)[0])
        __VIEWSTATE = response.xpath("//input[@id='__VIEWSTATE']/@value").extract_first()
        __VIEWSTATEGENERATOR = response.xpath("//input[@id='____VIEWSTATEGENERATOR']/@value").extract_first()
        __EVENTVALIDATION = response.xpath("//input[@id='__EVENTVALIDATION']/@value").extract_first()

        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "http://www.sxsyxcg.com",
            "Pragma": "no-cache",
            "Referer": "http://www.sxsyxcg.com/HomePage/ShowListNew.aspx?CatalogId=3&TzggType=2&type=7",
            "Upgrade-Insecure-Requests": "1",
            "cookie": cookie,
        }

        data = {
            "__VIEWSTATE": __VIEWSTATE,
            "__VIEWSTATEGENERATOR": __VIEWSTATEGENERATOR,
            "__EVENTTARGET": "pager1",
            "__EVENTARGUMENT": "1",
            "__EVENTVALIDATION": __EVENTVALIDATION,
            "txtTitle": ""
        }

        # total_page = 2
        for i in range(1, total_page+1):
            post_data = copy.deepcopy(data)
            post_data["__EVENTARGUMENT"] = str(i)
            yield feapder.Request(url=request.url, callback=self.parse, headers=headers, data=post_data)

    def parse(self, request, response):
        
        title_contents = response.xpath("//div[@class='els-messagelist els-box-body']//li")

        for title_content in title_contents:

            detail_url = title_content.xpath("./a/@href").extract_first()
            title = title_content.xpath("./a/text()").extract_first()
            release_time = re.findall(r"\d{4}-\d{2}-\d{2}", title)[0]

            yield feapder.Request(url=detail_url, callback=self.parse_detail, title=title)
    
    def parse_detail(self, request, response):

        if response.status_code != 200 or "经检测您的网站未备案" in response.text:
            raise Exception("response code not 200") 
        item = YgShaanxiInfoListItem()

        item.url = request.url
        item.title = request.title
        item.union_id = get_uuid(request.url, request.title)
        item.release_time = re.findall(r"\d{4}-\d{2}-\d{2}", request.title)[0]
        item.raw = response.text

        yield item




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
    spider = tmp(redis_key="test_shaanxi", delete_keys=True)
    spider.add_parser(Shaanxiparser)
    
    spider.start()
        
        