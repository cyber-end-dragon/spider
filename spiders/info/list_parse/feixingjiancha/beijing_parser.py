import sys
if __name__ == "__main__":
    sys.path.append("../../../../")
import feapder
import re
import json
import time
from pprint import pprint
from bs4 import BeautifulSoup
from feapder.utils.tools import get_uuid, get_full_url, parse_url_params
from items.info_list_item import InfoListItem
from feapder.utils.log import log
from feapder.utils.webdriver import PlaywrightDriver, InterceptResponse, InterceptRequest
from spiders.base import BaseParser

class BeijingInfoParser(BaseParser):
    """
    北京药品监督管理局  http://yjj.beijing.gov.cn/yjj/xxcx/jdjcxx/fxzxjcxx/index.html
    """
    def start_requests(self):
        url = "http://yjj.beijing.gov.cn/yjj/xxcx/jdjcxx/fxzxjcxx/index.html"
        yield feapder.Request(url=url, callback=self.parse_for_page)

    def parse_for_page(self, request, response):

        page_url = response.xpath("//span[@class='page_border']/b/a")[-1].xpath("./@onclick").extract_first()
        page_num = int(response.xpath("//span[@class='page_border']/b/a")[-1].xpath("./text()").extract_first())
        page_url = "http://yjj.beijing.gov.cn" + re.findall(r"'(.*?)'", page_url)[0]

        for i in range(1, page_num + 1):
            page_url = re.sub(r"-(.*?)\.", "-" + str(i)+ ".", page_url)
            # print(page_url)
            yield feapder.Request(page_url, callback=self.parse, priority=i)

    def validate(self, request, response):

        if response.status_code != 200:
            raise Exception("response code not 200") # 重试
        
        
    def parse(self, request, response):

        source = "飞行检查.北京市药品监督管理局"
        save_count = 0
        filter_word1 = ["医疗器械", "飞行检查"]
        filter_word2 = ["公司", "厂", "飞行检查"]
        title_contents = response.xpath("//p[@class='article-title xinwen']")

        for title_content in title_contents:

            title = title_content.xpath("./a/text()").extract_first()
            url = title_content.xpath("./a/@href").extract_first()
            condj = [all(ext in title for ext in filter_word1), any(ext in title for ext in filter_word2[:2]) and (filter_word2[2] in title)]
            if not condj[0]:
                if not condj[1]:
                    continue
                else:
                    if  not self.parse_content(url, "医疗器械"):
                        continue
            
            item = InfoListItem()
            item.url = url
            item.id = get_uuid(item.url, source)
            item.raw = title_content.get()
            item.release_time = title_content.xpath("./span/text()").extract_first()
            item.source = source
            item.title = title

            # yield item
            print(item)

            save_count += 1


        log.info("[{}]扫描到{}条列表".format(source, save_count))

    def parse_content(self, url, word):

        resp = feapder.Request(url).get_response()
        soup = resp.bs4()
        text = soup.get_text()

        if word in text:
            return True
        return False
        


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
    spider = tmp(redis_key="test_beijing", delete_keys=True)
    spider.add_parser(BeijingInfoParser)
    
    spider.start()