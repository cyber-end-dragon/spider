# -*- coding: utf-8 -*-
"""
Created on 2023-04-17 14:43:25
---------
@summary:
---------
@author: user
"""

from feapder import Item


class YgHubeiInfoListItem(Item):
    """
    This class was generated by feapder
    command: feapder create -i yg_hubei_info_list
    """

    __table_name__ = "yg_hubei_info_list"

    def __init__(self, *args, **kwargs):
        self.COMNAME = None  # 申报企业
        self.COMNAME_SC = None  # 生产企业
        self.GPARTNAME = None  # 产品名称
        # self.id = None
        # self.meta_crawl_time = None  # meta 抓取时间
        self.PRICE = None  # 挂网价
        self.PROCURECATALOGID = None  # 组件编号
        self.PRODUCTTYPE = None  # 采购类别
        self.raw = None  # list页item的原始数据
        self.REGCARDNM = None  # 注册证编号
        self.SORTNAME = None  # 目录分类
