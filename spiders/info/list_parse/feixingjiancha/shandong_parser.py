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



class ShanDongInfoParser(BaseParser):
    """
    山东省药品监督管理局  http://mpa.shandong.gov.cn/col/col308865/index.html
    """

    def start_requests(self):
        url = "http://mpa.shandong.gov.cn/col/col308865/index.html"
        yield feapder.Request(url=url, callback=self.parse_for_page)

    def parse_for_page(self, request, response):
        
        page_record = int(re.findall("totalRecord:(\d+)", response.text)[0])
        sec_record = 48
        page_num = page_record // sec_record
        remain_record = page_record % sec_record
        base_url = "http://mpa.shandong.gov.cn/module/web/jpage/dataproxy.jsp?startrecord={}&endrecord={}&perpage=16&unitid=613378&webid=412&path=http://mpa.shandong.gov.cn/&webname=%E5%B1%B1%E4%B8%9C%E7%9C%81%E8%8D%AF%E5%93%81%E7%9B%91%E7%9D%A3%E7%AE%A1%E7%90%86%E5%B1%80&col=1&columnid=308865&sourceContentType=1&permissiontype=0"

        headers = {
            # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'Host': 'mpa.shandong.gov.cn',
            'Origin': 'http://mpa.shandong.gov.cn',
            'Referer': 'http://mpa.shandong.gov.cn/col/col308865/index.html?uid=613378&pageNum=3',
        }
        from_data = {
            "col": "1",
            "webid": "412",
            "path": "http://mpa.shandong.gov.cn/",
            "columnid": "308865",
            "sourceContentType": "1",
            "unitid": "613378",
            "webname": "山东省药品监督管理局",
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

        source = "飞行检查.山东省药品监督管理局"
        save_count = 0
        filter_word1 = ["医疗器械", "监督检查"]
        # filter_word2 = ["公司", "厂"]
        # filter_word3 = ["停产整改", "暂停生产"]
        title_contents = re.findall(r"<record>([\s\S]*?)<\/record>", response.text)

        for title_content in title_contents[:48]:

            title = re.findall(r'title="(.*?)"', title_content)[0]
            url = re.findall(r'href="(.*?)"', title_content)[0]
            if not(all(ext in title for ext in filter_word1)):
                continue
            
            resp = requests.get(url)
            file_urls = re.findall(r'(http:\/\/mpa\.shandong\.gov\.cn\/module\/download\/downfile\.jsp.*?)"', resp.text) #附件下载地址
            result = []
            for file_url in file_urls:
                result.append(self.parse_file(file_url, "飞行检查"))            
            if not(any(result)):
                continue
                    
            item = InfoListItem()
            item.url = url
            item.id = get_uuid(item.url, source)
            item.raw = title_content
            item.release_time = re.findall(r"<span>(.*?)</span>", title_content)[0]
            item.source = source
            item.title = title

            # print(item)
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
    spider = tmp(redis_key="test_ShanDongInfoParser", delete_keys=True)
    spider.add_parser(ShanDongInfoParser)

    spider.start()