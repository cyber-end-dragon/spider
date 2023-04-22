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
import base64

import feapder
from feapder.utils.log import log
from setting import CUSTOM_PROXY
from spiders.base import BaseParser
from items.yg_hubei_info_list_item import YgHubeiInfoListItem
from items.yg_hubei_detail_list_item import YgHubeiDetailListItem


class Hubeiparser(BaseParser):

    def start_requests(self):

        base_url = "https://www.hbyxjzcg.cn:8011/HSNN/CM/BaseDB/Web/Controller/GpartController/QueryTradeCatalogGPart.HSNN?REGCARDNM={}&GPARTNAME=&COMNAME="
        for i in range(1):
            reg = base64.b64encode(str(i).encode()).decode()
            url = base_url.format(reg)
            yield feapder.Request(url, callback=self.parse_for_page, page=1)

    def download_midware(self, request):

        headers = {
            "Host": "www.hbyxjzcg.cn:8011",
            "Origin": "https://www.hbyxjzcg.cn:8011",
            "Pragma": "no-cache",
            "Referer": "https://www.hbyxjzcg.cn:8011/Pages/GPART/GpartList.aspx",
            "X-Requested-With": "XMLHttpRequest"
        }

        from_data = {
            "_search": "false",
            "nd": str(int(time.time()*1000)),
            "rows": "30",
            "page": str(request.page),
            "sidx": "",
            "sord": "asc"
        }

        request.headers = headers
        request.data = from_data
        request.timeout = 100
        request.proxies = CUSTOM_PROXY
        return request
    
    def parse_for_page(self, request, response):

        total_page = response.json["total"]
        # print(total_page)
        # total_page = 1
        
        for i in range(1, total_page+1):

            yield feapder.Request(request.url, callback=self.parse, page=i)



    def parse(self, request, response):

        save_count = 0

        title_contents = response.json["rows"]
        
        for title_content in title_contents:

            item = YgHubeiInfoListItem()
            item.PROCURECATALOGID = title_content["PROCURECATALOGID"]
            item.GPARTNAME = title_content["GPARTNAME"]
            item.COMNAME = title_content["COMNAME"]
            item.COMNAME_SC = title_content["COMNAME_SC"]
            item.REGCARDNM = title_content["REGCARDNM"]
            item.SORTNAME = title_content["SORTNAME"]
            item.raw = title_content

            PRODUCTTYPE = title_content["PRODUCTTYPE"]
            if PRODUCTTYPE == "":
                item.PRODUCTTYPE = "带量采购"
            else:
                item.PRODUCTTYPE = "阳光挂网"
            if title_content["MAXPRICE"] != title_content["MINPRICE"]:
                item.PRICE = "%s 至 %s" % (title_content["MINPRICE"], title_content["MAXPRICE"])
            else:
                item.PRICE = title_content["MAXPRICE"]


            base_url = "https://www.hbyxjzcg.cn:8011/HSNN/CM/BaseDB/Web/Controller/GpartMinController/QueryGpartMin_MH.HSNN?GPARTID={}"
            pid = base64.b64encode(title_content["PROCURECATALOGID"].encode()).decode()
            yield feapder.Request(base_url.format(pid), callback=self.parse_detail, page=1, first=True)
            # print(item)
            yield item

            save_count += 1
        log.info("扫描到{}条列表".format(save_count))

    def parse_detail(self, request, response):

        total_page = response.json["total"]

        if  request.first:
            for i in range(2, total_page+1):
                yield feapder.Request(request.url, callback=self.parse_detail, page=i, first=False)

        title_contents = response.json["rows"]

        for title_content in title_contents:

            item = YgHubeiDetailListItem()
            item.GPARTMINID = title_content["GPARTMINID"]
            item.GPARTMINMODEL = title_content["GPARTMINMODEL"]
            item.GPARTMINOUTLOOKC = title_content["GPARTMINOUTLOOKC"]
            item.MEDICALCODE = title_content["MEDICALCODE"]
            item.raw = title_content

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
    spider = tmp(redis_key="test_hubei", delete_keys=True)
    spider.add_parser(Hubeiparser)
    
    spider.start()