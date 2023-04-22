import feapder


class InfoParser(feapder.BaseParser):
    """
    注意 这里继承的是BaseParser，而不是Spider
    """
    def start_requests(self):
        yield feapder.Request("https://news.qq.com/")

    def parse(self, request, response):
        title = response.xpath("//title/text()").extract_first()
        print(title)