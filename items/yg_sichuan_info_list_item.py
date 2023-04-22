# -*- coding: utf-8 -*-
"""
Created on 2023-03-31 13:18:21
---------
@summary:
---------
@author: user
"""

from feapder import Item


class YgSichuanInfoListItem(Item):
    """
    This class was generated by feapder
    command: feapder create -i yg_sichuan_info_list
    """

    __table_name__ = "yg_sichuan_info_list"

    def __init__(self, *args, **kwargs):
        # self.id = None
        self.procurecatalogId = None  # 注册备案号
        self.regCerno = None  # 注册备案号
        self.productName = None  # 单件产品名称
        self.regCername = None  # 注册备案产品名称
        self.companyNameSc = None  # 生产企业
        self.companyNameTb = None  # 申报企业
        self.model = None  # 型号
        self.outLookc = None  # 规格
        self.linkageReferencePrice = None  # 联动参考价
        # self.meta_crawl_time = None  # meta 抓取时间
