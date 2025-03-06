import os
import re
import sys
import csv
import time
import json
import random
import pymysql
import requests

from os import path
# d = path.dirname(__file__)  # 获取当前路径
# parent_path = path.dirname(d)  # 获取上一级路径
# sys.path.append(parent_path)    # 如果要导入到包在上一级
# # print(path.dirname(__file__))
# from my_selenium_utils import get_cookie
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from moviepy.editor import *

# Chrome测试版的路径
chrome_testing_path = r"D:\chrome-win64\chrome.exe"
# Chromedriver的路径
chromedriver_path = r"C:\Users\Lenovo\AppData\Local\Programs\Python\Python311\chromedriver.exe"
# 打开浏览器 使之在后台运行
os.chdir(r"D:\chrome-win64")
os.popen(r'start chrome.exe --remote-debugging-port=9527 --user-data-dir="E:\selenium')
# 设置Chrome选项
options = webdriver.ChromeOptions()
# options.add_argument('--headless')
# options.add_argument('--disable-gpu')
# options.add_argument('--no-sandbox')

# options.add_experimental_option('excludeSwitches', ['enable-automation'])

options.binary_location = chrome_testing_path
options.add_experimental_option("debuggerAddress", "127.0.0.1:9527",)
# options.add_experimental_option('excludeSwitches', ['enable-automation'])
# 设置WebDriver服务
service = Service(chromedriver_path)
# 创建Chrome WebDriver实例
driver = webdriver.Chrome(service=service, options=options)
driver.get('https://hackforums.net/')

input('请登录HackForums并点击任意键继续...')