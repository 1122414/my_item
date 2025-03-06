# import os
# import re
# import sys
# import csv
# import time
# import json
# import random
# import pymysql
# import requests

# from os import path
# # d = path.dirname(__file__)  # 获取当前路径
# # parent_path = path.dirname(d)  # 获取上一级路径
# # sys.path.append(parent_path)    # 如果要导入到包在上一级
# # # print(path.dirname(__file__))
# # from my_selenium_utils import get_cookie
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.action_chains import ActionChains
# from moviepy.editor import *

# # Chrome测试版的路径
# chrome_testing_path = r"D:\chrome-win64\chrome.exe"
# # Chromedriver的路径
# chromedriver_path = r"C:\Users\Lenovo\AppData\Local\Programs\Python\Python311\chromedriver.exe"
# # 打开浏览器 使之在后台运行
# os.chdir(r"D:\chrome-win64")
# os.popen(r'start chrome.exe --remote-debugging-port=9527 --user-data-dir="E:\selenium')
# # 设置Chrome选项
# options = webdriver.ChromeOptions()
# options.binary_location = chrome_testing_path
# options.add_experimental_option("debuggerAddress", "127.0.0.1:9527")
# # 设置WebDriver服务
# service = Service(chromedriver_path)
# # 创建Chrome WebDriver实例
# driver = webdriver.Chrome(service=service, options=options)

# driver.get('https://v.douyin.com/irXHMnm9/')
# input()

import os
import requests
from time import sleep
from lxml import etree
current_path = os.path.dirname(__file__)
full_path = os.path.join(current_path, 'douyin.html')
url = 'https://www.douyin.com/video/7402879652336897330'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36 Edg/99.0.1150.36',
    'referer': 'https://www.douyin.com/',
    'cookie':'douyin.com; bd_ticket_guard_client_web_domain=2; my_rd=2; SEARCH_RESULT_LIST_TYPE=%22single%22; xgplayer_user_id=488001022358; passport_assist_user=CkEBU8nbVFeYdZ9crn01epOMV-tPv7Koj93VtA9pv0cNDEeMCMtmVOHKOj1UmrQ11_iwmZ9FqzYim59mySFvd-QIDhpKCjxr7EXHzkpHhKNG1bqHTPsWNU_1yOHJwnzforqvQNE_vlJOABA0tOzuqOFxGi02tP0wnr-bJiPdFf2r_Y4Qo6rQDRiJr9ZUIAEiAQOZvOMf; n_mh=vHqTHKLfZ3mW9e56odzz4aV-dZ5bqsWFd7LA8i0OVck; uid_tt=654452d4265dd1956387bd5277a2aa0a; uid_tt_ss=654452d4265dd1956387bd5277a2aa0a; sid_tt=0ba1a70b46e5d38ca004a3e36830fe90; sessionid=0ba1a70b46e5d38ca004a3e36830fe90; sessionid_ss=0ba1a70b46e5d38ca004a3e36830fe90; LOGIN_STATUS=1; store-region=cn-js; store-region-src=uid; d_ticket=60c7482873dba155f4ccea534b4500dd866e2; __live_version__=%221.1.1.9998%22; live_use_vvc=%22false%22; xgplayer_device_id=95976811080; ttwid=1%7CndUtxAmeB5PA2twyqGnrbz-fBLkCthoq7vFb8Iy7A9c%7C1714751481%7C8e3e0bced75b80c5a933d226ce4cf06cf999a63255d04a8b01d7611eecb4e260; UIFID_TEMP=29d6bea3e5a6c157a08a212e1912b5e8a78666ece26be56100fa19e58a63a45be7e6ed8c3f74d2eb74ace6d389c06279e7cac69616501ace94bd85956831def45de78abc9d74ae8c7c9df660e5f16b8d; fpk1=U2FsdGVkX19e18xiykjwKT+Rr5fB95+VJkiOoXndlNZOCiStxCQL9+6XyI4FDNfditPjzRNyCncy829o3BKMgg==; fpk2=c92baae71318dc81de51a663df2f8b4f; passport_csrf_token=8fa7ef00ea941d31123a26a220c50b93; passport_csrf_token_default=8fa7ef00ea941d31123a26a220c50b93; UIFID=29d6bea3e5a6c157a08a212e1912b5e8a78666ece26be56100fa19e58a63a45b13cefcc824873aaec8d715c1fff875daf02e1aa4f45dceedd5aec7036fc93ee151f722cbeaee980b29c5ed932aa2fcb01032e7f33557982e12a17ef8957ea25795faa90f3451a8640334c3372a2dddbf7f5f4767ab32f5d32a90ccd4449a94869be30bfd11f5ee8a736c9c492672d7abe21f073e1e64f2864ed8172eaae32d24; s_v_web_id=verify_ly9l2y40_1E6GUYnk_fXJi_4mD1_9L49_XXebVnZL3i5A; dy_swidth=1707; dy_sheight=1067; sid_guard=0ba1a70b46e5d38ca004a3e36830fe90%7C1723894090%7C5184000%7CWed%2C+16-Oct-2024+11%3A28%3A10+GMT; sid_ucp_v1=1.0.0-KGFhZTdhYTVjZjlkN2FlNjc2YzM3YWI3ODk1OTVhNmRjYmQ2MGY5YTIKGwiOqqCZo4y-BxDKkoK2BhjvMSAMOAZA9AdIBBoCbGYiIDBiYTFhNzBiNDZlNWQzOGNhMDA0YTNlMzY4MzBmZTkw; ssid_ucp_v1=1.0.0-KGFhZTdhYTVjZjlkN2FlNjc2YzM3YWI3ODk1OTVhNmRjYmQ2MGY5YTIKGwiOqqCZo4y-BxDKkoK2BhjvMSAMOAZA9AdIBBoCbGYiIDBiYTFhNzBiNDZlNWQzOGNhMDA0YTNlMzY4MzBmZTkw; publish_badge_show_info=%221%2C0%2C0%2C1723894309802%22; download_guide=%223%2F20240817%2F0%22; pwa2=%220%7C0%7C3%7C0%22; csrf_session_id=dbd0db17b37bbf5b53808c1796bc8a6c; douyin.com; device_web_cpu_core=32; device_web_memory_size=8; architecture=amd64; stream_recommend_feed_params=%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A1707%2C%5C%22screen_height%5C%22%3A1067%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A32%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A10%2C%5C%22effective_type%5C%22%3A%5C%224g%5C%22%2C%5C%22round_trip_time%5C%22%3A50%7D%22; strategyABtestKey=%221723980628.515%22; biz_trace_id=dbe9b6eb; volume_info=%7B%22isUserMute%22%3Afalse%2C%22isMute%22%3Atrue%2C%22volume%22%3A0.5%7D; __ac_nonce=066c1e188009380f5946a; __ac_signature=_02B4Z6wo00f01EITw6gAAIDBnmpcHueD8xBCM8cAAHZMb1; FOLLOW_LIVE_POINT_INFO=%22MS4wLjABAAAAK0DbY6_-TaCr91JErhyDehnO7iiFzSmsLir9t2PE4pySfEN-5WzkAwPjGFsohzcK%2F1723996800000%2F0%2F0%2F1723983139962%22; FOLLOW_NUMBER_YELLOW_POINT_INFO=%22MS4wLjABAAAAK0DbY6_-TaCr91JErhyDehnO7iiFzSmsLir9t2PE4pySfEN-5WzkAwPjGFsohzcK%2F1723996800000%2F0%2F1723982539962%2F0%22; home_can_add_dy_2_desktop=%221%22; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtcmVlLXB1YmxpYy1rZXkiOiJCSTlVY1F5NEhzVnlvN0FGSmF2NkdZVWZ6cDNmTTFTWG16Ris0MGFhRHhpSTlrakZ5ekRWTFZDL3A5VU9YTkpTZElqbTFLZGZnLzRGQy84NE0yenZXb2s9IiwiYmQtdGlja2V0LWd1YXJkLXdlYi12ZXJzaW9uIjoxfQ%3D%3D; odin_tt=644d1e786799b0042e0ebc00e0ceb7ff497ba6a6189967a2dd60f283dcd50dda1f400e9dd13f8a1eaf4996683563d300; WallpaperGuide=%7B%22showTime%22%3A1723895922436%2C%22closeTime%22%3A0%2C%22showCount%22%3A1%2C%22cursor1%22%3A35%2C%22cursor2%22%3A0%7D; IsDouyinActive=false; passport_fe_beating_status=false'
}
response = requests.get(url, headers=headers,timeout=10)

with open(full_path, 'wb') as f:
    f.write(response.content)

tree = etree.HTML(response.text)
# 点赞数量
like_num = tree.xpath('//*[@id="douyin-right-container"]/div[2]/div/div/div[1]/div[2]/div/div[2]/div[2]/div[1]/div/div[2]/text()')
# 评论数量
comment_num = tree.xpath('//*[@id="douyin-right-container"]/div[2]/div/div/div[1]/div[2]/div/div[2]/div[2]/div[2]/div/div[2]/text()')
# 收藏数量
collect_num = tree.xpath('//*[@id="douyin-right-container"]/div[2]/div/div/div[1]/div[2]/div/div[2]/div[2]/div[3]/div[2]/text()')
# 转发数量
forward_num = tree.xpath('//*[@id="douyin-right-container"]/div[2]/div/div/div[1]/div[2]/div/div[2]/div[2]/div[5]/div[1]/div[2]/text()')
# 标题
title = tree.xpath('//*[@id="douyin-right-container"]/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div[2]/span/span[2]/span/span/span/span/span/text()')

print(like_num)
print(comment_num)
print(collect_num)
print(forward_num)
print(response.text)
