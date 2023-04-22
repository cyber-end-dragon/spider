# -*- coding: utf-8 -*-
"""
Created on 2023-01-28 10:02:01
---------
@summary:main --crawl_info_list <index>
---------
@author: szb
"""

from setting import CUSTOM_TUNNEL
from spiders.base import BaseSpider


class ListPage(BaseSpider):

    __instance__ = None

    @classmethod
    def get_instance(cls, list_type, *args, **kwargs):
        # XXX 多线程下不安全，但是当前场景没这个需求
        if cls.__instance__ is None:
            cls.__instance__ = cls(*args, **kwargs)
  
        if int(list_type) in [3]:
            # 飞行检查
            from .list_parse.feixingjiancha.anhui_parser import AnHuiInfoParser as feixingjiancha_anhui_parser
            from .list_parse.feixingjiancha.beijing_parser import BeijingInfoParser as feixingjiancha_beijing_parser
            from .list_parse.feixingjiancha.chongqing_parser import ChongQingInfoParser as feixingjiancha_chongqing_parser
            from .list_parse.feixingjiancha.fujian_parser import FuJianInfoParser as feixingjiancha_fujian_parser
            # from .list_parse.feixingjiancha.gansu_parser import GanSuInfoParser
            from .list_parse.feixingjiancha.guangdong_parser import GuangDongInfoParser as feixingjiancha_guangdong_parser
            from .list_parse.feixingjiancha.guangxi_parser import GuangXiInfoParser as feixingjiancha_guangxi_parser
            from .list_parse.feixingjiancha.guizhou_parser import GuiZhouInfoParser as feixingjiancha_guizhou_parser
            from .list_parse.feixingjiancha.hainan_parser import HaiNanInfoParser  as feixingjiancha_hainan_parser
            from .list_parse.feixingjiancha.hebei_parser import HeBeiInfoParser as feixingjiancha_hebei_parser
            from .list_parse.feixingjiancha.heilongjiang_parser import HeiLongJiangInfoParser as feixingjiancha_heilongjiang_parser
            from .list_parse.feixingjiancha.henan_parser import HeNanInfoParser as feixingjiancha_henan_parser
            from .list_parse.feixingjiancha.hunan_parser import HuNanInfoParser as feixingjiancha_hunan_parser
            from .list_parse.feixingjiancha.jiangsu_parse import JiangSuInfoParser  as feixingjiancha_jiangsu_parser
            from .list_parse.feixingjiancha.jiangsu2_parser import JiangSu2InfoParser   as feixingjiancha_jiangsu2_parser
            from .list_parse.feixingjiancha.jiangxi_parser import JiangXiInfoParser as feixingjiancha_jiangxi_parser
            from .list_parse.feixingjiancha.liaoning_parser import LiaoNingInfoParser   as feixingjiancha_liaoning_parser
            from .list_parse.feixingjiancha.ningxia_parser import NingXiaInfoParser     as feixingjiancha_ningxia_parser
            from .list_parse.feixingjiancha.nmg_parser import NmgInfoParser as feixingjiancha_nmg_parser
            from .list_parse.feixingjiancha.npma_parser import NmpaInfoParser   as feixingjiancha_npma_parser
            from .list_parse.feixingjiancha.shaanxi_parser import ShaanXiInfoParser as feixingjiancha_shaanxi_parser
            from .list_parse.feixingjiancha.shaanxi2_parser import ShaanXi2InfoParser   as feixingjiancha_shaanxi2_parser
            from .list_parse.feixingjiancha.shandong_parser import ShanDongInfoParser   as feixingjiancha_shandong_parser
            from .list_parse.feixingjiancha.shanghai_parser import ShangHaiInfoParser as feixingjiancha_shanghai_parser
            from .list_parse.feixingjiancha.shanxi_parser import ShanXiInfoParser   as feixingjiancha_shanxi_parser
            from .list_parse.feixingjiancha.shencha_parser import ShenChaInfoParser as feixingjiancha_shencha_parser
            from .list_parse.feixingjiancha.sichuan_parser import SiChuanInfoParser as feixingjiancha_sichuan_parser
            from .list_parse.feixingjiancha.tianjin_parser import TianJinInfoParser as feixingjiancha_tianjin_parser
            from .list_parse.feixingjiancha.yunnan_parser import YunNanInfoParser   as feixingjiancha_yunnan_parser
            from .list_parse.feixingjiancha.yunnan2_parser import YunNan2InfoParser as feixingjiancha_yunnan2_parser
            from .list_parse.feixingjiancha.zhejiang_parser import ZheJiangInfoParser   as feixingjiancha_zhejiang_parser

            cls.__instance__.add_parser(feixingjiancha_anhui_parser)
            cls.__instance__.add_parser(feixingjiancha_beijing_parser)
            cls.__instance__.add_parser(feixingjiancha_chongqing_parser)
            cls.__instance__.add_parser(feixingjiancha_fujian_parser)
            # cls.__instance__.add_parser(GanSuInfoParser)
            cls.__instance__.add_parser(feixingjiancha_guangdong_parser)
            cls.__instance__.add_parser(feixingjiancha_guangxi_parser)
            cls.__instance__.add_parser(feixingjiancha_guizhou_parser)
            cls.__instance__.add_parser(feixingjiancha_hainan_parser)
            cls.__instance__.add_parser(feixingjiancha_hebei_parser)
            cls.__instance__.add_parser(feixingjiancha_heilongjiang_parser)
            cls.__instance__.add_parser(feixingjiancha_henan_parser)
            cls.__instance__.add_parser(feixingjiancha_hunan_parser)
            cls.__instance__.add_parser(feixingjiancha_jiangsu_parser)
            cls.__instance__.add_parser(feixingjiancha_jiangsu2_parser)
            cls.__instance__.add_parser(feixingjiancha_jiangxi_parser)
            cls.__instance__.add_parser(feixingjiancha_liaoning_parser)
            cls.__instance__.add_parser(feixingjiancha_ningxia_parser)
            cls.__instance__.add_parser(feixingjiancha_nmg_parser)
            cls.__instance__.add_parser(feixingjiancha_npma_parser)
            cls.__instance__.add_parser(feixingjiancha_shanxi_parser)
            cls.__instance__.add_parser(feixingjiancha_shaanxi_parser)
            cls.__instance__.add_parser(feixingjiancha_shaanxi2_parser)
            cls.__instance__.add_parser(feixingjiancha_shandong_parser)
            cls.__instance__.add_parser(feixingjiancha_shanghai_parser)
            cls.__instance__.add_parser(feixingjiancha_shencha_parser)
            cls.__instance__.add_parser(feixingjiancha_shanxi_parser)
            cls.__instance__.add_parser(feixingjiancha_sichuan_parser)
            cls.__instance__.add_parser(feixingjiancha_tianjin_parser)
            cls.__instance__.add_parser(feixingjiancha_yunnan_parser)
            cls.__instance__.add_parser(feixingjiancha_yunnan2_parser)
            cls.__instance__.add_parser(feixingjiancha_zhejiang_parser)

        if int(list_type) in [4]:
            # 器械召回'
            from .list_parse.qixiezhaohui.anhui_parser import AnHuiInfoParser as qixiezhaohui_anhui_parser
            from .list_parse.qixiezhaohui.beijiang_parser import BeijingInfoParser as qixiezhaohui_beijing_parser
            from .list_parse.qixiezhaohui.chongqing_parser import ChongQingInfoParser as qixiezhaohui_chongqing_parser
            from .list_parse.qixiezhaohui.fujian_parser import FuJianInfoParser as qixiezhaohui_fujian_parser
            from .list_parse.qixiezhaohui.guangdong_parser import GuangDongInfoParser as qixiezhaohui_guangdong_parser
            from .list_parse.qixiezhaohui.guangxi_parser import GuangXiInfoParser as qixiezhaohui_guangxi_parser
            from .list_parse.qixiezhaohui.guizhou_parser import GuiZhouInfoParser as qixiezhaohui_guizhou_parser
            from .list_parse.qixiezhaohui.hainan_parser import HaiNanInfoParser as qixiezhaohui_hainan_parser
            from .list_parse.qixiezhaohui.hebei_parser import HeBeiInfoParser as qixiezhaohui_hebei_parser
            from .list_parse.qixiezhaohui.heilongjiang_parser import HeiLongJiangInfoParser as qixiehzhaohui_heilongjiang_parser
            from .list_parse.qixiezhaohui.henan_parser import HeNanInfoParser as qixiezhaohui_henan_parser
            from .list_parse.qixiezhaohui.hunan_parser import HuNanInfoParser as qixiezhaohui_hunan_parser
            from .list_parse.qixiezhaohui.jiangsu_parser import JiangSuInfoParser as qixiezhaohui_jiangsu_parser
            from .list_parse.qixiezhaohui.jiangxi_parser import JiangXiInfoParser as qixiezhaohui_jiangxi_parser
            from .list_parse.qixiezhaohui.jilin_parser import JiLinInfoParser as qixiezhaohui_jilin_parser
            from .list_parse.qixiezhaohui.liaoning_parser import LiaoNingInfoParser as qixiezhaohui_liaoning_parser
            from .list_parse.qixiezhaohui.ningxia_parser import NingXiaInfoParser as qixiezhaohui_ningxia_parser
            from .list_parse.qixiezhaohui.nmg_parser import NmgInfoParser as qixiezhaohui_nmg_parser
            from .list_parse.qixiezhaohui.npma_parser import NmpaInfoParser as qixiezhaohui_npma_parser
            from .list_parse.qixiezhaohui.shaanxi_parser import ShaanXiInfoParser as qixiezhaohui_shaanxi_parser
            from .list_parse.qixiezhaohui.shandong_parser import ShanDongInfoParser as qixiezhaohui_shandong_parser
            from .list_parse.qixiezhaohui.shanghai_parser import ShangHaiInfoParser as qixiezhaohui_shanghai_parser
            from .list_parse.qixiezhaohui.shanghai2_parser import ShangHaiInfoParser as qixiezhaohui_shanghai2_parser
            from .list_parse.qixiezhaohui.shanxi_parser import ShanXiInfoParser as qixiezhaohui_shanxi_parser
            from .list_parse.qixiezhaohui.sichuan_parser import SiChuanInfoParser as qixiezhaohui_sichuan_parser
            from .list_parse.qixiezhaohui.tianjin_parser import TianJinInfoParser as qixiezhaohui_tianjin_parser
            from .list_parse.qixiezhaohui.yunnan_parser import YunNanInfoParser as qixiezhaohui_yunnan_parser
            from .list_parse.qixiezhaohui.zhejiang_parser import ZheJiangInfoParser as qixiezhaohui_zhejiang_parser

            cls.__instance__.add_parser(qixiezhaohui_anhui_parser)
            cls.__instance__.add_parser(qixiezhaohui_beijing_parser)
            cls.__instance__.add_parser(qixiezhaohui_chongqing_parser)
            cls.__instance__.add_parser(qixiezhaohui_fujian_parser)
            cls.__instance__.add_parser(qixiezhaohui_guangdong_parser)
            cls.__instance__.add_parser(qixiezhaohui_guangxi_parser)
            cls.__instance__.add_parser(qixiezhaohui_guizhou_parser)
            cls.__instance__.add_parser(qixiezhaohui_hainan_parser)
            cls.__instance__.add_parser(qixiezhaohui_hebei_parser)
            cls.__instance__.add_parser(qixiezhaohui_hainan_parser)
            cls.__instance__.add_parser(qixiezhaohui_henan_parser)
            cls.__instance__.add_parser(qixiehzhaohui_heilongjiang_parser)
            cls.__instance__.add_parser(qixiezhaohui_hunan_parser)
            cls.__instance__.add_parser(qixiezhaohui_jiangsu_parser)
            cls.__instance__.add_parser(qixiezhaohui_jiangxi_parser)
            cls.__instance__.add_parser(qixiezhaohui_jilin_parser)
            cls.__instance__.add_parser(qixiezhaohui_liaoning_parser)
            cls.__instance__.add_parser(qixiezhaohui_ningxia_parser)
            cls.__instance__.add_parser(qixiezhaohui_nmg_parser)
            cls.__instance__.add_parser(qixiezhaohui_npma_parser)
            cls.__instance__.add_parser(qixiezhaohui_shaanxi_parser)
            cls.__instance__.add_parser(qixiezhaohui_shandong_parser)
            cls.__instance__.add_parser(qixiezhaohui_shanghai_parser)
            cls.__instance__.add_parser(qixiezhaohui_shanghai2_parser)
            cls.__instance__.add_parser(qixiezhaohui_shanxi_parser)
            cls.__instance__.add_parser(qixiezhaohui_sichuan_parser)
            cls.__instance__.add_parser(qixiezhaohui_tianjin_parser)
            cls.__instance__.add_parser(qixiezhaohui_yunnan_parser)
            cls.__instance__.add_parser(qixiezhaohui_zhejiang_parser)


        return cls.__instance__

    # 自定义数据库，若项目中有setting.py文件，此自定义可删除
    __custom_setting__ = dict(
        RENDER_DOWNLOADER="feapder.network.downloader.PlaywrightDownloader",
        SPIDER_THREAD_COUNT=1,
        SPIDER_SLEEP_TIME=[0, 2],
        SPIDER_MAX_RETRY_TIMES=5,
        PLAYWRIGHT=dict(
            # 字符串 或 无参函数，返回值为user_agent
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
            proxy=CUSTOM_TUNNEL,  # xxx.xxx.xxx.xxx:xxxx 或 无参函数，返回值为代理地址
            headless=True,  # 是否为无头浏览器
            driver_type="chromium",  # chromium、firefox、webkit
            timeout=10,  # 请求超时时间
            render_time=1,  # 渲染时长，即打开网页等待指定时间后再获取源码
            # 等待页面加载完成的事件,可选值："commit", "domcontentloaded", "load", "networkidle"
            wait_until="networkidle",
            use_stealth_js=True,  # 使用stealth.min.js隐藏浏览器特征
        ),
    )


if __name__ == "__main__":
    ListPage(redis_key="xxx:xxx", delete_keys=True).start()
