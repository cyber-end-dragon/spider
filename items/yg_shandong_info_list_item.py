# -*- coding: utf-8 -*-
"""
Created on 2023-04-03 13:23:54
---------
@summary:
---------
@author: user
"""

from feapder import Item


class YgShandongInfoListItem(Item):
    """
    This class was generated by feapder
    command: feapder create -i yg_shandong_info_list
    """

    __table_name__ = "yg_shandong_info_list"

    def __init__(self, *args, **kwargs):
        # self.id = None
        self.device_name = None  # 产品名称
        self.dir1_name = None  # 一级目录
        self.dir2_name = None  # 二级目录
        self.dir3_name = None  # 三级目录
        self.brand = None  # 品牌
        self.outLookc = None  # 规格
        self.model = None  # 型号
        self.manufacturer = None  # 生产企业
        self.regcer_name = None  # 注册证编码
        self.price = None  # 挂网价格
        # self.meta_crawl_time = None  # meta 抓取时间
