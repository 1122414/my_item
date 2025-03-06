# 可以使用！配置好的Tor浏览器
import os
import time
import subprocess
from selenium import webdriver
from lxml import etree
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from DrissionPage.common import from_selenium
from DrissionPage import ChromiumPage,ChromiumOptions

subprocess.Popen('"E:\Tor_Browser\Browser\\firefox.exe"  --marionette --marionette-port 2828')
subprocess.Popen('geckodriver.exe --connect-existing --marionette-port 2828')
# 创建一个新的Firefox选项对象
options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")
# options.add_experimental_option('excludeSwitches', ['enable-automation'])  

# 连接到已经存在的Firefox实例
driver = webdriver.Remote(command_executor="http://localhost:4444", options=options)

time.sleep(10)
driver.execute_cdp_cmd(
    'Page.addScriptToEvaluateOnNewDocument',
    {
        'source':'Object.defineProperty(navigator,"webdriver",{get:()=>undefined})'
    }
)

driver.get('https://hackforums.net/')

time.sleep(60)

print('11111')
# 尝试DP接管自动化
page = from_selenium(driver)

time.sleep(30)
print("Tor Browser is ready!")
page.get("https://hackforums.net/")
# print(driver.title)
time.sleep(300)
driver.quit()