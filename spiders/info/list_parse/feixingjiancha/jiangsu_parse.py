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
    江苏省药品监督管理局  http://da.jiangsu.gov.cn/col/col84624/index.html
    """

    def start_requests(self):
        url = "http://da.jiangsu.gov.cn/col/col84624/index.html"
        headers = {
            "Host": "da.jiangsu.gov.cn",
            # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
            "Upgrade-Insecure-Requests": "1",
        }
        yield feapder.Request(url=url, callback=self.parse, headers=headers)

    # def parse_for_page(self, request, response):

    #     pass
        
    def parse(self, request, response):

        source = "飞行检查.江苏省药品监督管理局"
        save_count = 0
        filter_word1 = ["医疗器械", "飞行检查"]
        filter_word2 = ["公司", "厂", "飞行检查"]
        filter_word3 = ["停产整改", "暂停生产", "医疗器械"]
        title_contents = re.findall(r"<record><\!\[CDATA\[([\s\S]*?)\]\]><\/record\>", response.text)
        # page_record = int(re.findall("totalRecord:(\d+)", response.text)[0])

        for title_content in title_contents[:45]:
            try:
                title = re.findall(r"<\/b>(.*?)<\/a>", title_content)[0]
                url = re.findall(r'href="(.*?)"', title_content)[0]
            except:
                continue
            if not(all(ext in title for ext in filter_word1)):
                if not(any(ext in title for ext in filter_word2[:2]) and (filter_word2[2] in title)):
                    if not(any(ext in title for ext in filter_word3[:2]) and (filter_word3[2] in title)):
                        continue
                    else:
                        if not self.parse_content(url, "飞行检查"):
                            continue


            item = InfoListItem()
            item.url = url
            item.id = get_uuid(item.url, source)
            item.raw = title_content
            item.release_time = re.findall(r'808080">(.*?)<', title_content)[0]
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
    spider = tmp(redis_key="test_JiangSuInfoParser", delete_keys=True)
    spider.add_parser(JiangSuInfoParser)

    spider.start()