import scrapy


class FirstSpider(scrapy.Spider):
    # 爬虫文件的名称：就是爬虫源文件的唯一标识
    name = "first"
    # 允许的域名 用来限定star_urls列表中哪些url可以请求发送 一般来说不用
    # allowed_domains = ["www.baidu.com"]
    # 起始URL：该列表中存饭的url会被scrapy自动请求发送
    start_urls = ["https://www.baidu.com",'https://www.sina.com.cn']
    # 解析函数：用来解析响应内容，response是爬虫收到的响应对象
    def parse(self, response):
        print(response)
        pass
