from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from lxml import etree
# 实例化一个浏览器对象（传入浏览器的驱动）
# executable_path='2024.7哔站爬虫\Python超强爬虫8天速成\Day07\chromedriver-win64\chromedriver.exe'
url = 'https://uland.taobao.com/sem/tbsearch?clk1=03bd86e77690313e0ef4c335594a72eb'
bro = webdriver.Chrome()

# 让浏览器发一个指定url请求
bro.get(url)
# 标签定位
search_input = bro.find_element(By.ID,'q')
# 标签交互
search_input.send_keys('小米')
# 点击搜索按钮
btn = bro.find_element(By.CLASS_NAME,'btn-search')
btn.click()

# 执行一组js程序
bro.execute_script("window.scrollTo(0,document.body.scrollHeight)")


bro.get('https://www.baidu.com')
sleep(2)
# 回退
bro.back()
sleep(2)
# 前进
bro.forward()
sleep(2)

# page_text = bro.page_source
# # 解析页面内容
# tree = etree.HTML(page_text)
# # 打印古诗题目
# title_list = tree.xpath('//div[@class="cont"]//p/a/b')
# for title in title_list:
#     print(title.text)

sleep(5)
bro.quit()
