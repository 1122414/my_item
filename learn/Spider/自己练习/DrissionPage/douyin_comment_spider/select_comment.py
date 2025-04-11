import os
import re
import json
import time
import whisper
import requests
import pandas as pd
import subprocess
import pymysql
import torch
import random
from datetime import datetime
from DrissionPage import ChromiumPage,ChromiumOptions
from DrissionPage.common import By
from DrissionPage.common import Keys

WAIT_TIME = 10
CRAWL_NUM = 1000
current_path = os.path.dirname(os.path.abspath(__file__))
INPUT_KEYS = 'AI造谣明星输十亿'

# 命令行打开
subprocess.Popen('"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9527 --user-data-dir="E:\selenium\AutomationProfile"')
co = ChromiumOptions().set_local_port(9527)
# co.incognito()  # 匿名模式
# co.headless()  # 无头模式
page = ChromiumPage(addr_or_opts=co)

current_datetime = datetime.now()      # 获取当前日期和时间
current_date = current_datetime.date() # 提取日期部分
# print(current_date)  # 输出：YYYY-MM-DD

headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
  'referer':'https://www.douyin.com/'
}

def after_search_click0():
  '''搜索过内容之后，点击视频专栏，点击第一个视频'''
  # 点击视频专栏  
  page.ele('x://*[@id="search-content-area"]/div/div[1]/div[1]/div[1]/div/div/span[2]').click()
  page.wait(WAIT_TIME)
  # //*[@id="search-result-container"]/div[2]/ul
  # 点击第一个视频
  video_list = page.eles('x://*[@id="search-result-container"]/div[2]/ul/li')
  video_list[0].click()
  page.wait(3)

def sanitize_filename(filename):
    '''解决title不合规情况'''
    # 定义不合规字符的正则表达式
    invalid_chars_regex = r'[\"<>:"/\\|?*\n\r\x00-\x1F,]'
    # 替换不合规字符为空格
    if invalid_chars_regex == '?':
       sanitized_filename = re.sub(invalid_chars_regex, '？', filename)
       return sanitized_filename
    sanitized_filename = re.sub(invalid_chars_regex, ' ', filename)
    return sanitized_filename

def close_tab_and_scroll(now_tab,now_video):
  '''关闭当前标签页并滚动页面'''
  page.wait(3)
  page.close_tabs(now_tab)
  scroll(now_video)

def write2csv(file_path,data):
  '''当保存视频失败时将数据写入csv文件'''
  header = not os.path.exists(file_path)  # 判断文件是否存在
  pd.DataFrame([data]).to_csv(file_path, mode='a', header=header, index=False)
  print(f'文件信息写入成功')

def extract_http_links(text):
  '''正则匹配http/https链接（支持含路径、参数的复杂URL）'''
  pattern = r'https?://[^\s"\'<>]+'
  return re.findall(pattern, text)

def convert_wan_to_number(text):
  '''匹配含“万”的数值（如3.6万）和普通数字（如2000）'''
  pattern = r'(\d+\.?\d*)\s*万?'
  
  def replace_match(match):
      num_str = match.group(1)
      unit = match.group(0).strip()[-1] if '万' in match.group(0) else None
      
      # 若含“万”则乘以10000，否则直接转为整数
      num = float(num_str)
      if unit == '万':
          return str(int(num * 10000))  # 转换为整数避免小数点
      else:
          return str(int(num))  # 普通数字保持原值
      
  try:
    text = re.findall(r'\d+\.?\d*万', text)[0]
  except Exception as e:
    pass
  
  # 替换逻辑（保留原字符串中的非数字部分）
  converted_text = re.sub(
      pattern,
      replace_match,
      text
  )

  try:
    converted_text = int(converted_text)
  except Exception as e:
    converted_text = 0
    
  return int(converted_text)

def scroll(now_video):
  '''下滑动作'''
  now_video.ele('x://div[@data-e2e="video-switch-next-arrow"]').click()
  page.wait(WAIT_TIME)

def get_data():
  '''获取点赞、评论、收藏、转发、视频地址'''
  dir_path = os.path.join(current_path,'data')
  if not os.path.exists(dir_path):
    os.mkdir(dir_path)

  file_path = os.path.join(current_path,'data', f'douyin_data{current_date}_{INPUT_KEYS}.csv')
  data = {
    'title': '',
    'u_name':'',
    'publish_time':'',
    'favirate': 0,
    'comment': 0,
    'collect': 0,
    'transmit': 0,
    'url':'',
    'text':''
  }
  # 视频列表
  # //*[@id="sliderVideo"]/div[1]/div[1]/div/div[1]/div[2]/div[6]/div[2]/div/div/div/button[2]/div
  # 想爬取的条数
  for i in range(CRAWL_NUM):
    # 这两个字段可能没有  所以每次清空
    data['text']  =''
    data['url'] = ''
    data['video_url'] = ''
    # 点击暂停
    page.actions.key_down(Keys.SPACE)

    video_list = page.eles('x://*[@id="douyin-right-container"]/div[4]/div[4]/div/div/div/div')
    try:
      data_list = video_list[i].eles('x://*[@id="sliderVideo"]/div[1]/div[1]/div/div[1]/div[2]/div')
    except Exception as e:
      print(f'{INPUT_KEYS},关键字最后一个视频')

    favirate_number = convert_wan_to_number(data_list[1].text)
    comment_number = convert_wan_to_number(data_list[2].text)
    collect_number = convert_wan_to_number(data_list[3].text)
    transmit_number = convert_wan_to_number(data_list[5].text)
    # 权重公式：点赞*0.9+评论*2+收藏*1.8+转发*1.5
    # weight = round(favirate_number*0.9+comment_number*2+collect_number*1.8+transmit_number*1.5,2)
    print(f'第{i}个的comment数量为：{comment_number}')
    if comment_number >= 50:
      data['favirate']=favirate_number
      data['comment']=comment_number
      data['collect']=collect_number
      data['transmit']=transmit_number
      data['title']=video_list[i].ele('x://*[@id="video-info-wrap"]/div[1]/div/div[2]/div/div[1]').text
      data['u_name']=video_list[i].ele('x://*[@id="video-info-wrap"]/div[1]/div[1]/div[1]').text
      data['publish_time']=video_list[i].ele('x://*[@id="video-info-wrap"]/div[1]/div[1]/div[2]').text

      # print(data['title'][0:20]+'.mp4')
      if (data['title'][0:20]+'.mp4') in os.listdir(os.path.join(current_path,'video_data')):
          page.wait(WAIT_TIME)
          scroll(video_list[i])
          print('该视频已存在')
          continue
      # for file_name in os.listdir('learn\Spider\自己练习\DrissionPage\孙总\video_data'):
      #   if file_name == (data['title']+'.mp4'):
          
      #     is_have = 1
      #     break
      # 悬浮一下才会出现url内容
      try:
        data_list[5].hover()
      except Exception as e:
        print(f'悬浮失败，错误原因：{e}')
      page.wait(3)

      # 获取可打开抖音网页视频url用于验证
      try:
        url_data = video_list[i].ele('x://*[@id="sliderVideo"]/div[1]/div[1]/div/div[1]/div[2]/div[6]/div[2]/div/div/div/button[2]/div/div[1]/div/img').attr('alt')
        data['url']=extract_http_links(url_data)[0]
      except Exception as e:
        print(f'获取url失败，错误原因：{e}')
        page.wait(WAIT_TIME)
        scroll(video_list[i])
        continue
      # data
      print(data)
      write2csv(file_path, data)
    else:
      print(f'第{i}个视频权重小于2000，跳过')
      page.wait(3)
    scroll(video_list[i])
  print('爬取完成')
def spider():
  # 进入抖音并搜索保研字段
  page.get('https://www.douyin.com/')
  # 怕要验证
  page.wait(WAIT_TIME)
  # 搜索内容
  page.ele('x://*[@id="douyin-header"]/div[1]/header/div/div/div[1]/div/div[2]/div/div[1]/input').input(INPUT_KEYS)
  page.wait(WAIT_TIME)
  page.ele('x://*[@id="douyin-header"]/div[1]/header/div/div/div[1]/div/div[2]/div/button').click()
  page.wait(WAIT_TIME)

  after_search_click0()
  # 获取数据
  get_data()

if __name__ == '__main__':
  # 添加CUDA优化配置
  torch.backends.cudnn.benchmark = True
  torch.set_float32_matmul_precision('high')
  spider()
  