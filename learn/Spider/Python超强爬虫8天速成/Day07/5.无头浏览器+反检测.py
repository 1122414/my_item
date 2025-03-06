from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ChromeOptions
from time import sleep

# 实现无头浏览器 无可视化界面
chrome_options = Options()
chrome_options.add_argument('--headless')  # 无头浏览器
chrome_options.add_argument('--disable-gpu')  # 禁用gpu加速
chrome_options.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在的报错

# 无头浏览器 phantomJs bro = webdriver.PhantomJS()
# 如何实现让selenium规避被检测到的风险
options = ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-automation'])

# 实现反反爬虫机制
bro = webdriver.Chrome(chrome_options=chrome_options,options=options)
bro.get('https://www.bilibili.com/')

print(bro.title)
sleep(3)
bro.quit()