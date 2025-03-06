# 爬取每一层的所有回复内容
import os
import re
import time
import random

from datetime import datetime
import requests
from bs4 import BeautifulSoup

# 分析爬取内容
def data_analysis(url,params,headers):
  global response
  response = requests.get(url, params = params,headers=headers)
  soup = BeautifulSoup(response.text, 'html.parser')
  reply_user_list = soup.find_all("a", class_="at j_user_card")
  reply_user_content = soup.find_all("span", class_="lzl_content_main")

  for i in range(len(reply_user_list)):
    print(reply_user_list[i].get_text())
    print(reply_user_content[i].get_text())
    print("-------------------\n")


url = "https://tieba.baidu.com/p/comment"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}
response = 0

'''
# 贴吧tid提取
match = re.search(r'\d+', url)  # 使用正则表达式匹配连续的数字
tid = match.group()  # 获取匹配到的子字符串
# print(sub_str)  
'''

# 时间戳转换
local_time = datetime.now()
t = int(time.time()*1000)
# print(t)

'''
尝试
# timestamp = int(time.mktime(local_time.timetuple()))
# timestamp_ms = datetime.fromtimestamp(timestamp)
# print(timestamp)
# print(timestamp_ms)
'''

params = {
  "tid": 8578212993,
  "pid": 148481934276,
  "pn" : 1,
  "fid": 4536,
  "t " : t,
}

# 第一次查询
data_analysis(url,params,headers)

# 正则查询尾页 有尾页时即总共多少页
pattern = r'<a href=".*?">尾页</a>'
# findall 返回列表
match = re.findall(pattern, response.text)
last_page = int(re.findall('\D(\d+)\D', str(match[0]))[0])
# print(int(last_page[0]))  # 输出：有尾页的情况下，输出尾页页码，没有尾页默认1

# 有大于等于二页的回复,爬取全部
if last_page > 1:
  for i in range(2, last_page + 1):
    sleep_time = i % random.randint(1,10)  # 随机休眠时间
    time.sleep(sleep_time)  # 休眠
    print("正在爬取第{}页".format(i))
    local_time = datetime.now()
    t = int(time.time()*1000)
    # 参数重新设定
    params["pn"] = i
    params["t"] = t
    response = requests.get(url, params = params,headers=headers)
    data_analysis(url,params,headers)


