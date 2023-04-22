# -*- coding: utf-8 -*-
"""
Created on 2022-06-06 16:10:37
---------
@summary: 爬虫入口
---------
@author: nic
"""

from feapder import ArgumentParser
from feapder.utils.log import log



def do_crawl_info_list(crawl_info_list):
    """
    爬取资讯类信息
    """
    from spiders.info.list_page import ListPage
    ListPage.get_instance(crawl_info_list, redis_key="info_list", delete_keys=True).start()

def crawl_info_detail_master():
    """
    爬取资讯类信息master
    """
    from spiders.info.detail_page import DetailPage
    DetailPage(
        redis_key="info_detail2",  # 分布式爬虫调度信息存储位置
        task_table="info_list",  # mysql中的任务表
        task_keys=["union_id", "url", "title", "release_time", "source", "meta"],  # 需要获取任务表里的字段名，可添加多个
        task_state="state",  # mysql中任务状态字段    
        keep_alive=True
    ).start_monitor_task()

def crawl_info_detail_worker():
    """
    爬取资讯类信息worker
    """
    from spiders.info.detail_page import DetailPage
    DetailPage(
        redis_key="info_detail2",  # 分布式爬虫调度信息存储位置
        task_table="info_list",  # mysql中的任务表
        task_keys=["union_id", "url", "title", "release_time", "source", "meta"],  # 需要获取任务表里的字段名，可添加多个
        task_state="state",  # mysql中任务状态字段    
        keep_alive=True
    ).start()

def crawl_yg_list():
    """
    爬取阳光挂网价
    """
    from spiders.yg_list.list_page import ListPage
    ListPage.get_instance(redis_key="yg_list", delete_keys=True).start()
    
if __name__ == "__main__":
    parser = ArgumentParser(description="szb爬虫")


    parser.add_argument(
        "--crawl_info_list", help="""
        爬取资讯类列表数据:
        3 ==> 飞行检查
        4 ==> 器械召回
        """, function=do_crawl_info_list
    )

    parser.add_argument(
        "--crawl_info_detail_master",  help="""
        爬取资讯类详情数据
        """, action="store_true", function=crawl_info_detail_master
    )

    parser.add_argument(
        "--crawl_info_detail_worker",  help="""
        爬取资讯类详情数据
        """, action="store_true", function=crawl_info_detail_worker
    )

    parser.add_argument(
        "--crawl_yg_list", help="""
        爬虫各省阳光挂网价
        """, action="store_true", function=crawl_yg_list
    )

    parser.start()


