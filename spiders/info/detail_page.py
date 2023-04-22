# -*- coding: utf-8 -*-
"""
Created on 2023-01-28 10:02:13
---------
@summary:
---------
@author: szb
"""
import sys
if __name__ == "__main__":
    sys.path.append("../..")
import json
import feapder
from feapder import ArgumentParser
from setting import CUSTOM_TUNNEL
from spiders.base import BaseTaskSpider
from feapder.utils.webdriver import WebDriver, PlaywrightDriver
from feapder.utils.log import log
from items.info_detail_item import InfoDetailItem


"""
    详情页爬取
"""



class DetailPage(BaseTaskSpider):
    # 自定义数据库，若项目中有setting.py文件，此自定义可删除
    __custom_setting__ = dict(
        RENDER_DOWNLOADER="feapder.network.downloader.PlaywrightDownloader",
        SPIDER_THREAD_COUNT=10,
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
            use_stealth_js=True,  # 使用stealth.min.js隐藏浏览器特征
        ),
    )

    def start_requests(self, task):
        cols = ["id","union_id", "url", "title", "release_time", "source", "meta"]
        paylaod = {key:getattr(task, key) for key in cols}

        yield feapder.Request(paylaod["url"], item=paylaod, task_id=paylaod["union_id"], render=True)

    def parse(self, request: feapder.Request, response):
        request_item = request.item
        title = request_item["title"]
        title = title.strip(".。").strip()[:10]
        
        driver: PlaywrightDriver = response.browser
        page = driver.page
        page.wait_for_load_state("networkidle")
        log.info("当前代理ip是: {}".format(driver._proxy))

        
        item = InfoDetailItem()
        item.union_id = request_item["union_id"]
        item.raw = page.content()
        item.source = request_item["source"]
        item.url = request.url
        item.meta = {
            "list_meta": request_item
        }
        # 检查下是否正确
        # XXX: list页面过来的title前10个字符一定在raw中??
        # assert title
        # assert title in item.raw, "list页title不在raw中: {} , raw: {}".format(title, item.raw)

        yield item
        # # mysql 需要更新任务状态为做完 即 state=1
        yield self.update_task_batch(request_item["id"])
    
    def failed_request(self, request, response, e):
        yield self.update_task_batch(request.task_id, state=-1)

if __name__ == "__main__":
    pass
    # 用mysql做任务表，需要先建好任务任务表
    # spider = DetailPage(
    #     redis_key="info_detail:dev",  # 分布式爬虫调度信息存储位置
    #     task_table="info_list",  # mysql中的任务表
    #     task_keys=["id", "url", "title", "release_time", "source", "meta"],  # 需要获取任务表里的字段名，可添加多个
    #     task_state="state",  # mysql中任务状态字段
    # )


    # parser = ArgumentParser(description="DetailPage爬虫")

    # parser.add_argument(
    #     "--start_master",
    #     action="store_true",
    #     help="添加任务",
    #     function=spider.start_monitor_task,
    # )
    # parser.add_argument(
    #     "--start_worker", action="store_true", help="启动爬虫", function=spider.start
    # )

    # parser.start()

    # 直接启动
    # spider.start()  # 启动爬虫
    # spider.start_monitor_task() # 添加任务

    # 通过命令行启动
    # python detail_page.py --start_master  # 添加任务
    # python detail_page.py --start_worker  # 启动爬虫