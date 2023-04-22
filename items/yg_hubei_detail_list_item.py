# -*- coding: utf-8 -*-
"""
Created on 2023-04-17 14:43:37
---------
@summary:
---------
@author: user
"""

from feapder import Item


class YgHubeiDetailListItem(Item):
    """
    This class was generated by feapder
    command: feapder create -i yg_hubei_detail_list
    """

    __table_name__ = "yg_hubei_detail_list"

    def __init__(self, *args, **kwargs):
        self.CODEPRICE = None  # 挂网价
        self.GPARTMINID = None  # CODE编号
        self.GPARTMINMODEL = None  # 产品型号
        self.GPARTMINOUTLOOKC = None  # 产品规格
        # self.id = None
        self.MEDICALCODE = None  # 医保耗材编码
        # self.meta_crawl_time = None  # meta 抓取时间
        self.raw = None  # list页item的原始数据