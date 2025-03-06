import os
import random

import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from lxml import etree
from scrapy import Request



class BossSpider(scrapy.Spider):
    
    name = "boss"
    # allowed_domains = ["www.xxx.com"]
    start_urls = ["https://www.zhipin.com/web/geek/job?city=101190100&position=100109&page=1"]

    bro = webdriver.Chrome()
    bro.get(start_urls[0])
    sleep(random.randint(1, 3))
    
    page_num = 1
    url = f"https://www.zhipin.com/web/geek/job?city=101190100&position=100109&page={page_num}"
    current_path = os.path.dirname(__file__)
    full_path = os.path.join(current_path, "boss.html")
    def parse(self, response):
        with open(self.full_path, "wb") as f:
            f.write(response.body)
        print(f"正在爬取第{self.page_num}页")
        title_list = response.xpath("//div[@class='job-title clearfix']/span/text()")
        salary_list = response.xpath("//div[@class='job-info clearfix']/span/text()")
        experience_list = response.xpath("//div[@class='job-info clearfix']/ul/text()")

        print(f"职位名称：{title_list}")
        print(f"薪资：{salary_list}")
        print(f"经验：{experience_list}")

        # for i in range(1,10):
        #     print(f'正在爬取第：{i}页')

        pass
