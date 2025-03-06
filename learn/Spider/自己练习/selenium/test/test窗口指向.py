import os
import time
import random
import pymysql
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC


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

driver.get("https://www.zhihu.com/search?type=content&q=%E7%BD%91%E5%AE%89")

for i in range(5):
  # # 注意：使用变量有一定滞后性
  # # 以下代码本意就是拿到最后一个driver.current_window_handle，即[-1]
  #   # driver当前聚焦的window
  # current_window = driver.current_window_handle  
  #   # 返回当前会话中所有窗口的句柄。
  # all_window=driver.window_handles    
  #   # 打印当前所有窗口的句柄 name
  #   # print("all_window:: ",all_window)  
  # #通过遍历判断要切换的窗口
  # for window in all_window:           
  #   print("window::  ",window)
  #   if window != current_window:
  #     # 将定位焦点切换到指定的窗口，包含所有可切换焦点的选项
  #     driver.switch_to.window(window)    
  # # 获取当前窗口handle name 
  # current_window = driver.current_window_handle
  time.sleep(random.randint(1, 3))
  driver.execute_script("window.scrollTo(window.scrollBy(0,1000));")
  time.sleep(random.randint(1, 3))
  driver.execute_script("window.scrollTo(window.scrollBy(0,-50));")


input()