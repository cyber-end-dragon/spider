from spiders.base import BaseSpider


class ListPage(BaseSpider):

    __instance__ = None

    @classmethod
    def get_instance(cls, *args, **kwargs):
        # XXX 多线程下不安全，但是当前场景没这个需求
        if cls.__instance__ is None:
            cls.__instance__ = cls(*args, **kwargs)

        from .yg_list.shaanxi_parser import Shaanxiparser
        from .yg_list.anhui_parser import Anhuiparser
        from .yg_list.hubei_parser import Hubeiparser
        from .yg_list.gansu_spider import GansuSpdier
        from .yg_list.hainan_spider import HainanSpdier
        from .yg_list.liaoning_spdier import LiaoningSpdier
        from .yg_list.shandong_spider import ShandongSpider
        from .yg_list.sichuan_spider import SichuanSpdier
        from .yg_list.test_arg import Testparser

        cls.__instance__.add_parser(Shaanxiparser)
        cls.__instance__.add_parser(Anhuiparser)
        cls.__instance__.add_parser(GansuSpdier)
        cls.__instance__.add_parser(HainanSpdier)
        cls.__instance__.add_parser(LiaoningSpdier)
        cls.__instance__.add_parser(ShandongSpider)
        cls.__instance__.add_parser(SichuanSpdier)
        cls.__instance__.add_parser(Hubeiparser)
        # cls.__instance__.add_parser(Testparser)

        return cls.__instance__

if __name__ == "__main__":
    ListPage(redis_key="xxx:xxx", delete_keys=True).start()