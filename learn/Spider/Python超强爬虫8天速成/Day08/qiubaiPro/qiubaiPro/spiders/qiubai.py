import scrapy
from qiubaiPro.items import QiubaiproItem

class QiubaiSpider(scrapy.Spider):
    name = "qiubai"
    # allowed_domains = ["www.xxx.com"]
    start_urls = ["https://nanjing.anjuke.com/sale/"]

    # def parse(self, response):
    #     # 解析：房名、总价、单价、地址、链接
    #     # section[2] 定位到单个div /div[1]/h3为名 /section[1]为具体信息
    #     all_data = []
    #     div_list = response.xpath('//*[@id="esfMain"]/section/section[3]/section[1]/section[2]/div/a/div[2]')
    #     for div in div_list:
    #         name = div.xpath('.//h3/text()')[0].extract()
    #         total_price = div.xpath('.//span[@class="property-price-total-num"]/text()').get()
    #         # 一样的效果
    #         # print(name, total_price)
    #         dic={
    #             'name':name,
    #             'total_price':total_price
    #         }
    #         all_data.append(dic)
    #     return all_data

    def parse(self, response):
    # 解析：房名、总价、单价、地址、链接
    # section[2] 定位到单个div /div[1]/h3为名 /section[1]为具体信息
        div_list = response.xpath('//*[@id="esfMain"]/section/section[3]/section[1]/section[2]/div/a/div[2]')
        for div in div_list:
            name = div.xpath('.//h3/text()').get()
            total_price = div.xpath('.//span[@class="property-price-total-num"]/text()').get()
            
            item = QiubaiproItem()
            item['name'] = name
            item['total_price'] = total_price
            yield item
        pass