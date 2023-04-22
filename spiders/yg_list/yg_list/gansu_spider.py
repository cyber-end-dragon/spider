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
from items.yg_gansu_info_list_item import YgGansuInfoListItem


class GansuSpdier(BaseParser):

    def start_requests(self):

        url = "http://hcygcg.ylbz.gansu.gov.cn:86/HSNN/CM/BaseDB/Web/Controller/DataPubController/PublicGpartList.HSNN"
        for i in range(1, 4):
        
            yield feapder.Request(url, callback=self.parse_for_page, SYSFLAG=i, page=1)

    def download_midware(self, request):

        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Host": "hcygcg.ylbz.gansu.gov.cn:86",
            "Origin": "http://hcygcg.ylbz.gansu.gov.cn:86",
            "Pragma": "no-cache",
            "Referer": "http://hcygcg.ylbz.gansu.gov.cn:86/BasePublicCodeListAdmin.aspx",
            "X-Requested-With": "XMLHttpRequest"
        }

        params= {
            "GPARTNAME": "",
            "COMNAME": "",
            "REGCARDNM": "",
            "BATCHID": "",
            "GPARTID": "",
            "GPARTMINID": "",
            "CHANGETYPE": "",
            "SYSFLAG": str(request.SYSFLAG),
            "appendFlag": ""
        }

        from_data = {
            "_search": "false",
            "nd": str(int(time.time()*1000)),
            "rows": "500",
            "page": str(request.page),
            "sidx": "",
            "sord": "asc"
        }

        request.headers = headers
        request.params = params
        request.data = from_data
        request.timeout = 100
        request.proxies = CUSTOM_PROXY
        return request
    
    def parse_for_page(self, request, response):

        total_page = response.json["total"]
        # total_page = 2
        
        url = "http://hcygcg.ylbz.gansu.gov.cn:86/HSNN/CM/BaseDB/Web/Controller/DataPubController/PublicGpartList.HSNN"
        for i in range(1, total_page+1):

            yield feapder.Request(url, callback=self.parse, SYSFLAG=request.SYSFLAG, page=i)



    def parse(self, request, response):

        save_count = 0

        title_contents = response.json["rows"]
        
        for title_content in title_contents:

            item = YgGansuInfoListItem()
            item.BATCHID = title_content["BATCHID"]
            item.CHECKSTATUS = title_content["CHECKSTATUS"]
            item.GPARTMINID = title_content["GPARTMINID"]
            item.PRODUCTTYPE = title_content["PRODUCTTYPE"]
            item.LARGECLASSTYPE = title_content["LARGECLASSTYPE"]
            item.GPARTID = title_content["GPARTID"]
            item.GPARTNAME = title_content["GPARTNAME"]
            item.GPARTREGOUTLOOKC = title_content["GPARTREGOUTLOOKC"]
            item.GPARTUNIT = title_content["GPARTUNIT"]
            item.GPARTFACTOR = title_content["GPARTFACTOR"]
            item.COMNAME = title_content["COMNAME"]
            item.SCCOMNAME = title_content["SCCOMNAME"]
            item.QGPRICEINFO = title_content["QGPRICEINFO"]
            item.REMARK = title_content["REMARK"]
            item.append_flag = title_content["appendFlag"]
            item.raw = title_content
            state = int(title_content["CHANGETYPE"])
            if state == 1:
                item.CHANGETYPE = "新审核通过"
            elif state == 2:
                item.CHANGETYPE = "注册证变更"
            elif state == 3:
                item.CHANGETYPE = "注册证延期"
            elif state == 4:
                item.CHANGETYPE = "产品转厂"
            elif state == 5:
                item.CHANGETYPE = "全国价格变更"
            elif state == 6:
                item.CHANGETYPE = "产品信息变更"


            save_count += 1

            # print(item)
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
    spider = tmp(redis_key="test_gansu", delete_keys=True)
    spider.add_parser(GansuSpdier)
    
    spider.start()