# -*- coding: utf-8 -*-
"""
Created on 2023-04-03 13:24:32
---------
@summary:
---------
@author: user
"""
import re

import feapder
from feapder.utils.log import log
from setting import CUSTOM_PROXY
from spiders.base import BaseParser
from items.yg_shandong_info_list_item import YgShandongInfoListItem


class ShandongSpider(BaseParser):
    
    def start_requests(self):
        url = "http://ggzyjyzx.shandong.gov.cn/yxpt/toHcxxpxy.html"
        yield feapder.Request(url, callback=self.parse_for_page)

    def download_midware(self, request):
        request.proxies = CUSTOM_PROXY
        return request

    def parse_for_page(self, request, response):

        total_page = int(re.findall("([\d\s]+?)页", response.text)[0])
        
        # total_page = 3
        base_url = "http://ggzyjyzx.shandong.gov.cn/yxpt/toHcxxpxy.html?goodsName=&companyName=&regCode=&pageNow={}"
        for i in range(1, total_page+1):

            url = base_url.format(i)
            # yield feapder.Request(url, callback=self.parse)


    def parse(self, request, response):

        save_count = 0

        title_contents = response.xpath("//tbody/tr")
        
        for title_content in title_contents:

            td_contents = title_content.xpath("./td")
            item =YgShandongInfoListItem()
            # item.id = td_contents[0].xpath("./text()").extract_first().strip()
            item.device_name = td_contents[1].xpath("./text()").extract_first().strip()
            item.dir1_name = td_contents[2].xpath("./text()").extract_first().strip()
            item.dir2_name  = td_contents[3].xpath("./text()").extract_first().strip()
            item.dir3_name = td_contents[4].xpath("./text()").extract_first().strip()
            item.brand = td_contents[5].xpath("./text()").extract_first().strip()
            item.outLookc = td_contents[6].xpath("./text()").extract_first().strip()
            item.model = td_contents[7].xpath("./text()").extract_first().strip()
            item.manufacturer = td_contents[8].xpath("./text()").extract_first().strip().strip()
            item.regcer_name = td_contents[9].xpath("./text()").extract_first().strip()
            item.price = td_contents[10].xpath("./text()").extract_first().strip()

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
    spider = tmp(redis_key="test_shandong", delete_keys=True)
    spider.add_parser(ShandongSpider)
    
    spider.start()
