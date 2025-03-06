import scrapy
import time
from time import sleep
import random
from anjuke.items import AnjukeItem

# 安居客给IP封了，换了个网站
class FirstSpider(scrapy.Spider):
    # 爬虫文件的名称：就是爬虫源文件的唯一标识
    name = "anjuke"
    # 允许的域名 用来限定star_urls列表中哪些url可以请求发送 一般来说不用
    # allowed_domains = ["www.baidu.com"]
    # 起始URL：该列表中存饭的url会被scrapy自动请求发送
    start_urls = ["https://nanjing.esf.fang.com/house/i31"]

    # 生成一个通用url模版
    url = 'https://nanjing.esf.fang.com/house/i3%d'
    page_num = 1
    # 解析函数：用来解析响应内容，response是爬虫收到的响应对象
    def parse(self, response):
        print(f'正在爬取第{self.page_num}页')
        # print(response)
        # 解析页面内容，提取数据
        title_list = response.xpath('//span[@class="tit_shop"]/text()')
        total_price_list = response.xpath('//span[@class="red"]/b/text()')
        one_area_price_list = response.xpath('//dd[@class="price_right"]/span[2]/text()')
        # 详情有缺失数据 暂不考虑
        # specification_details_list = response.xpath('//p[@class="tel_shop"]/text()')
        # toward_list = response.xpath('//a[@class="link_rk"]/text()')
        # j = 0
        for i in range(len(title_list)):
            title = title_list[i].extract()
            total_price = total_price_list[i].extract()+'万元'
            one_area_price = one_area_price_list[i].extract()
            # if i+j+4<len(specification_details_list):
            #     specification_details = {
            #         '户型：':specification_details_list[i+j].extract(),
            #         '面积：':specification_details_list[i+j+1].extract(),
            #         '楼层：':toward_list[i].extract(),
            #         '朝向：':specification_details_list[i+j+3].extract(),
            #         '时间：':specification_details_list[i+j+4].extract(),
            #     }
            item = AnjukeItem()
            item['title'] = title
            item['total_price'] = total_price
            item['one_area_price'] = one_area_price
            # print(title, total_price, one_area_price)
            yield item
            # j += 4
        if self.page_num <= 5:
            self.page_num += 1
            new_url = format(self.url % self.page_num)
            print(new_url)
            yield scrapy.Request(new_url, callback=self.parse)

        # 随机等待时间
        sleep(random.randint(3, 5))

        pass
