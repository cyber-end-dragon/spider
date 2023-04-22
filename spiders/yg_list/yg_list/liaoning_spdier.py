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

import feapder
from feapder.utils.log import log
from setting import CUSTOM_PROXY
from spiders.base import BaseParser
from items.yg_liaoning_info_list_item import YgLiaoningInfoListItem


class LiaoningSpdier(BaseParser):

    def start_requests(self):

        self.url = "https://gs.lnypcg.com.cn/Publicity/BargaInGoodsList.aspx"
        yield feapder.Request(self.url, callback=self.parse_for_page)

    def download_midware(self, request):
        request.proxies = CUSTOM_PROXY
        return request
    
    def parse_for_page(self, request, response):
        total_record = int(re.findall(r"共(.*?)条", response.text)[0])
        total_page = total_record // 50
        if total_record % 50:
            total_page += 1

        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9",
            "cache-control": "no-cache",
            "content-type": "application/x-www-form-urlencoded",
            "cookie": response.headers["Set-Cookie"].split(";")[0],
            "origin": "https://gs.lnypcg.com.cn",
            "pragma": "no-cache",
            "referer": "https://gs.lnypcg.com.cn/Publicity/BargaInGoodsList.aspx",
            "sec-ch-ua": "\"Microsoft Edge\";v=\"111\", \"Not(A:Brand\";v=\"8\", \"Chromium\";v=\"111\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
        }

        __VIEWSTATE = response.xpath("//input[@id='__VIEWSTATE']/@value").extract_first()
        __VIEWSTATEGENERATOR = response.xpath("//input[@id='__VIEWSTATEGENERATOR']/@value").extract_first()
        
        from_data = {
            "__VIEWSTATE": __VIEWSTATE,
            "__VIEWSTATEGENERATOR": __VIEWSTATEGENERATOR,
            "__EVENTTARGET": "AspNetPager1",
            "__EVENTARGUMENT": "1",
            "txtPnameone": "",
            "txtOutlook": "",
            "txtModeltype": "",
            "txtmlid": "",
            "txtCompanyName_SC": "",
            "txtProcureCatalogID": "",
            "AspNetPager1_input": "1",
            "AspNetPager1_pagesize": "50"
        }

        # total_page = 3
        for i in range(1, total_page+1):

            post_data = copy.deepcopy(from_data)
            post_data["__EVENTARGUMENT"] = str(i)
            yield feapder.Request(self.url, callback=self.parse, headers=headers, data=post_data, method="post")



    def parse(self, request, response):

        save_count = 0

        title_contents = response.xpath("//table[@class='mainlist']/tr")
        
        for title_content in title_contents[1:]:

            td_contents = title_content.xpath("./td")
            item = YgLiaoningInfoListItem()
            # item.id = td_contents[0].xpath("./text()").extract_first().strip()
            item.serial_num = td_contents[1].xpath("./text()").extract_first().strip()
            item.type = td_contents[2].xpath("./text()").extract_first().strip()
            item.dir_code = td_contents[3].xpath("./text()").extract_first().strip()
            item.dir_name = td_contents[4].xpath("./text()").extract_first().strip()
            item.device_name = td_contents[5].xpath("./text()").extract_first().strip()
            item.specs = td_contents[6].xpath("./span/text()").extract_first().strip()
            item.model = td_contents[7].xpath("./span/text()").extract_first().strip()
            item.unit = td_contents[8].xpath("./text()").extract_first().strip().strip()
            item.manufacturer = td_contents[9].xpath("./text()").extract_first().strip()
            item.bidder = td_contents[10].xpath("./text()").extract_first().strip()
            item.price = td_contents[11].xpath("./text()").extract_first().strip()

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
    spider = tmp(redis_key="test_liaoning", delete_keys=True)
    spider.add_parser(LiaoningSpdier)
    
    spider.start()
