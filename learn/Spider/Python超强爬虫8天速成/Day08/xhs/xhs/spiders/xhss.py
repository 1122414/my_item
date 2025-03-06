import scrapy


class XhssSpider(scrapy.Spider):
    name = "xhss"
    allowed_domains = ["www.xiaohongshu.com"]
    start_urls = ["https://www.xiaohongshu.com/"]

    def parse(self, response):
        pass
