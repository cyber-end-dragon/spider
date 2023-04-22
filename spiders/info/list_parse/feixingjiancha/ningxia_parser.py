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
import pandas as pd
from PyPDF2 import PdfReader
import zipfile
from docx import Document


class NingXiaInfoParser(BaseParser):
    """
    宁夏回族自治区药品监督管理局  http://nxyjj.nx.gov.cn/ylqx/jdjc_37870/
    """

    def start_requests(self):
        url = "http://nxyjj.nx.gov.cn/ylqx/jdjc_37870/"
        yield feapder.Request(url=url, callback=self.parse)

    # def parse_for_page(self, request, response):
        
    #     page_num = int(re.findall("createPageHTML\((\d+),", response.text)[0])
    #     base_url = "https://amr.hainan.gov.cn/himpa/xxgk/jdjc/index_{}.html"

    #     yield feapder.Request(url=request.url, callback=self.parse)
    #     for i in range(1, page_num):
    #         page_url = base_url.format(i)
    #         yield feapder.Request(url=page_url, callback=self.parse)


    def parse(self, request, response):

        # print(response.text)

        source = "飞行检查.宁夏回族自治区药品监督管理局"
        save_count = 0
        filter_word1 = ["医疗器械", "飞行检查"]
        filter_word2 = ["医疗器械", "监督检查"]
        title_contents = response.xpath("//ul[@class='news-ul']/li")

        for title_content in title_contents:

            title = title_content.xpath("./a/text()").extract_first()
            url = title_content.xpath("./a/@href").extract_first()

            condj = [all(ext in title for ext in filter_word1), all(ext in title for ext in filter_word2)]
            if not condj[0]:
                if not condj[1]:
                    continue
                else:
                    resp = feapder.Request(url).get_response()
                    file_urls = resp.xpath('//a[@appendix="true"]/@href')
                    result = []
                    for file_url in file_urls:
                        result.append(self.parse_file(file_url.extract(), "飞行检查"))
                    if not any(result):
                        continue

            item = InfoListItem()
            item.url = url
            item.id = get_uuid(item.url, source)
            item.raw = title_content.get()
            item.release_time = re.findall(r"(\d{4}-\d{2}-\d{2})", title_content.xpath("./span/text()").extract_first())[0]
            item.source = source
            item.title = title

            yield item

            save_count += 1

        log.info("[{}]扫描到{}条列表".format(source, save_count))

    def parse_file(self, url, word):
        
        file_content = requests.get(url).content
        file_ext = re.findall(r"\.(\w+?)$", url)[0]
        fb = BytesIO(file_content)
        
        if file_ext == "pdf":
            try:
                pdf = PdfReader(fb)
            except:
                return False
            for i in range(len(pdf.pages)):
                page = pdf.pages[i].extract_text()
                if word in page:
                    return True
            return False
        
        elif file_ext == "docx":
            try:
                zip_file = zipfile.ZipFile(fb)
            except:
                return False
            docx_content = zip_file.read("word/document.xml").decode("utf-8")
            if word in docx_content:
                return True
            return False
        
        elif file_ext == "doc" or file_ext == "wps":

            word_format = "<" + "H"*len(word)
            word_byte = struct.pack(word_format, *[ord(i) for i in word])
            if word_byte in file_content:
                return True
            return False
        
        elif file_ext == "xls" or file_ext == "xlsx":
            try:
                df = pd.read_excel(fb)
            except:
                return False
            for r in range(df.shape[0]):
                for c in range(df.shape[1]):
                    if word in str(df.iloc[r,c]):
                        return True
            return False
        else:
            print("%s无符合的格式" % url)


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
    spider = tmp(redis_key="test_NingXiaInfoParser", delete_keys=True)
    spider.add_parser(NingXiaInfoParser)

    spider.start()