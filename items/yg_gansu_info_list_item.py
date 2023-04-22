# -*- coding: utf-8 -*-
"""
Created on 2023-04-03 15:24:42
---------
@summary:
---------
@author: user
"""

from feapder import Item


class YgGansuInfoListItem(Item):
    """
    This class was generated by feapder
    command: feapder create -i yg_gansu_info_list
    """

    __table_name__ = "yg_gansu_info_list"

    def __init__(self, *args, **kwargs):
        # self.id = None
        self.CHANGETYPE = None  # 变更类型
        self.BATCHID = None  # 批次
        self.CHECKSTATUS = None  # 审核状态
        self.GPARTMINID = None  # code编号
        self.PRODUCTTYPE = None  # 目录分类
        self.LARGECLASSTYPE = None  # 目录大类
        self.GPARTID = None  # 组件编号
        self.GPARTNAME = None  # 产品名称
        self.REGCARDNM = None  # 注册证编号
        self.GPARTREGOUTLOOKC = None  # 注册证包装规模
        self.GPARTUNIT = None  # 最小销售单
        self.GPARTFACTOR = None  # 最小包装数
        self.COMNAME = None  # 投标企业
        self.SCCOMNAME = None  # 生产企业
        self.QGPRICEINFO = None  # 全国参考价
        self.REMARK = None  # 备注
        self.append_flag = None  # 是否补充
        self.raw = None  # list页item的原始数据
        # self.meta_crawl_time = None  # meta 抓取时间