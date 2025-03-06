from selenium import webdriver
from lxml import etree
# 实例化一个浏览器对象（传入浏览器的驱动）
# executable_path='2024.7哔站爬虫\Python超强爬虫8天速成\Day07\chromedriver-win64\chromedriver.exe'
url = 'https://www.gushiwen.cn/'
bro = webdriver.Chrome()

# 让浏览器发一个指定url请求
bro.get(url)
page_text = bro.page_source
# 解析页面内容
tree = etree.HTML(page_text)
# 打印古诗题目
title_list = tree.xpath('//div[@class="cont"]//p/a/b')
for title in title_list:
    print(title.text)

input()