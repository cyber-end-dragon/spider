# -*- coding: utf-8 -*-
"""
Created on 2023-03-30 13:47:00
---------
@summary:
---------
@author: user
"""

import re
import copy
import json
import time

import feapder
from feapder.utils.log import log
from setting import CUSTOM_PROXY
from spiders.base import BaseParser
from items.yg_sichuan_info_list_item import YgSichuanInfoListItem


class SichuanSpdier(BaseParser):

    def start_requests(self):

        url = "https://www.scyxzbcg.cn/hcstd/publicity/getConnectedProductList.html"
        yield feapder.Request(url, callback=self.parse_for_page, page="1")

    def download_midware(self, request):
        request.proxies = CUSTOM_PROXY

        from_data = {
            "procurecatalogType": "10",
            "productName": "",
            "regCerno": "",
            "regCername": "",
            "companyNameTb": "",
            "companyNameSc": "",
            "outLookc": "",
            "model": "",
            "_search": "false",
            "nd": "1680238959627",
            "rows": "100",
            "page": "1",
            "sidx": "",
            "sord": "asc"
        }
        post_data = copy.deepcopy(from_data)
        post_data["nd"] = str(int(time.time()*1000))
        post_data["page"] = request.page
        request.data = post_data

        return request
    
    def parse_for_page(self, request, response):

        total_page = response.json["total"]

        # total_page = 3
        
        base_url = "https://www.scyxzbcg.cn/hcstd/publicity/getConnectedProductList.html"
        for i in range(1, total_page+1):
            yield feapder.Request(base_url, callback=self.parse, page=str(i))



    def parse(self, request, response):

        save_count = 0

        title_contents = response.json["rows"]
        
        for title_content in title_contents:

            item = YgSichuanInfoListItem()
            item.procurecatalogId = title_content["procurecatalogId"]
            item.regCerno = title_content["regCerno"]
            item.productName = title_content["productName"]
            item.regCername = title_content["regCername"]
            item.companyNameSc = title_content["companyNameSc"]
            item.companyNameTb = title_content["companyNameTb"]
            item.model = title_content["model"]
            item.outLookc = title_content["outLookc"]
            item.linkageReferencePrice = title_content["linkageReferencePrice"]

            save_count += 1

            print(item)
            yield item
        log.info("扫描到{}条列表".format(save_count))


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
    spider = tmp(redis_key="test_sichuan", delete_keys=True)
    spider.add_parser(SichuanSpdier)
    
    spider.start()
