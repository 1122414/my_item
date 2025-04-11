import os
import re
import sys
import csv
import time
import json
import random
import pymysql

from os import path
d = path.dirname(__file__)  # 获取当前路径
parent_path = path.dirname(d)  # 获取上一级路径
sys.path.append(parent_path)    # 如果要导入到包在上一级
# print(path.dirname(__file__))
from my_selenium_utils import get_cookie
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains



# Chrome测试版的路径
chrome_testing_path = r"D:\chrome-win64\chrome.exe"
# Chromedriver的路径
chromedriver_path = r"C:\Users\Lenovo\AppData\Local\Programs\Python\Python311\chromedriver.exe"
# 打开浏览器 使之在后台运行
os.chdir(r"D:\chrome-win64")
os.popen(r'start chrome.exe --remote-debugging-port=9527 --user-data-dir="E:\selenium')
# 设置Chrome选项
options = webdriver.ChromeOptions()
options.binary_location = chrome_testing_path
options.add_experimental_option("debuggerAddress", "127.0.0.1:9527")
# 设置WebDriver服务
service = Service(chromedriver_path)
# 创建Chrome WebDriver实例
driver = webdriver.Chrome(service=service, options=options)
# 路径
current_path = os.path.dirname(__file__)

full_path = os.path.join(current_path, 'douyin_cookie.json')

try:
    driver.get('https://www.douyin.com/')
    driver.delete_all_cookies()  # 先删除cookies
    time.sleep(30) # 用于手动登录账号（利用扫码登录），这是人工操作的
    loginCookies = driver.get_cookies()  # 读取登录之后浏览器的cookies
    jsonCookies = json.dumps(loginCookies)  # 将字典数据转成json数据便于保存

    with open(full_path, 'w', encoding='utf-8') as f:  # 写进文本保存
        f.write(jsonCookies)
    print('cookie保存成功！')
except:
    # 关闭浏览器
    driver.close()