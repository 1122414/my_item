import os
import re
import sys
import csv
import time
import json
import random
import pymysql
import requests
from tkinter import ttk
from os import path
# d = path.dirname(__file__)  # 获取当前路径
# parent_path = path.dirname(d)  # 获取上一级路径
# sys.path.append(parent_path)    # 如果要导入到包在上一级
# # print(path.dirname(__file__))
# from my_selenium_utils import get_cookie
from selenium import webdriver
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
options.binary_location = chrome_testing_path
options.add_experimental_option("debuggerAddress", "127.0.0.1:9527")
# 设置WebDriver服务
service = Service(chromedriver_path)
# 创建Chrome WebDriver实例
driver = webdriver.Chrome(service=service, options=options)
# 路径
current_path = os.path.dirname(__file__)

# 基本操作
referer_url = 'https://www.bilibili.com'
headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
    'Referer':referer_url,
    # 'cookie':cookie
}

search_num = 0
global_keyword = ''
search_result_list = {}
search_before_window = 0

def pre():
  # 先加载网站
  driver.get('https://www.bilibili.com/')
  # time.sleep(60)
  # 等待页面加载完成
  time.sleep(random.uniform(1,3))

  with open(r'C:\Users\Lenovo\Desktop\vscode_python\2024.7哔站爬虫\自己练习\selenium\my_selenium_utils\cookie.json', 'r') as f:
      cookie_list = json.loads(f.read())
  # 将cookie添加到浏览器
  for cookie in cookie_list:
      driver.add_cookie(cookie)

def click_input(keyword):
  driver.find_element(By.XPATH,'//*[@id="nav-searchform"]/div[1]/input').send_keys(keyword)
  time.sleep(random.uniform(1,2))
  driver.find_element(By.XPATH,'//*[@id="nav-searchform"]/div[2]').click()
  time.sleep(random.uniform(1,3))

def search_video(keyword):
  global search_num
  search_num += 1
  print(f'搜索第{search_num}次：', keyword)
  time.sleep(random.uniform(3,5))
  # 重置搜索结果列表
  search_result_list['title'] = []
  search_result_list['url'] = []
  # 打开搜索页面 开始搜索
  if search_num == 1:
    driver.get('https://www.bilibili.com/')
    click_input(keyword)
  else:
    try:
      # 转到最新页面
      driver.switch_to.window(driver.window_handles[-1])
      # 先看最新页面是否在视频页面  如果在视频页面可以直接使用上面的搜索框而不用跳转
      click_input(keyword)
    except Exception as e:
      global search_before_window
      driver.switch_to.window(search_before_window)
      driver.get('https://www.bilibili.com/')
      click_input(keyword)
  # global search_before_window
  # search_before_window = driver.current_window_handle
  # driver.switch_to.window(search_before_window)
  
  '''
  # 原搜索代码
  # time.sleep(random.uniform(3,5))
  # driver.find_element(By.XPATH,'//*[@id="nav-searchform"]/div[1]/input').send_keys(keyword)
  # time.sleep(random.uniform(1,2))
  # driver.find_element(By.XPATH,'//*[@id="nav-searchform"]/div[2]').click()
  # time.sleep(random.uniform(1,3))
  '''

  # 更改当前窗口 此功能只需要停留在新出现的搜索页面
  # driver.switch_to.window(driver.window_handles[1])
  driver.switch_to.window(driver.window_handles[-1])
  # 搜索过一次关键字的页面  记录当前窗口
  search_before_window = driver.current_window_handle
  # 目前打开的搜索窗口
  global global_keyword
  if global_keyword != keyword:
    print('搜索页面变更')
  global_keyword = keyword

  # with open (r'C:\Users\Lenovo\Desktop\vscode_python\2024.7哔站爬虫\自己练习\selenium\my_selenium_utils\search_result.html', 'w', newline='', encoding='utf-8') as f:
  #   f.write(driver.page_source)

  # 批量获取搜索结果视频标题
  title_list = driver.find_elements(By.XPATH, '//div[@class="bili-video-card__info--right"]//h3')

  # 批量获取搜索结果视频url
  url_list = driver.find_elements(By.XPATH, '//div[@class="bili-video-card__info--right"]/a')

  # 过滤掉直播视频
  for i in range(len(title_list)):
    # 出现 substring not found 代表无法找到关键字  跳过
    try:
      url_list[i].get_attribute('href').index('live')
      url_list.remove(url_list[i])
      title_list.remove(title_list[i])
    except Exception as e:
      pass
    

  for i in range(len(title_list)):
    title = title_list[i].get_attribute('title')
    url = url_list[i].get_attribute('href')
    search_result_list['title'].append(title)
    search_result_list['url'].append(url)
    # 打印搜索结果
    # print(f"{i+1}.视频标题：", title)
    # print("视频链接：", url,'\n')

  print('搜索结束！')

def get_need_search_result(num):
  # 更改当前窗口 等于-1时  可以在新的搜索结果里继续下载  等于1时 在一开始的搜索结果里下载
  driver.switch_to.window(search_before_window)
  # 获取需要的视频标题和url
  num = int(num)
  need_title = search_result_list['title'][num-1]
  need_url = search_result_list['url'][num-1]

  select_url = need_url[need_url.index('//www'):]
  # 定位并点击链接 进入想要的页面
  element = driver.find_element(By.XPATH,f'//a[@href="{select_url}"]')
  ActionChains(driver).move_to_element(element).click(element).perform()
  
def get_videoInfo(src):
  if src!= '':
    driver.get(src)
  # 在搜索后，已经进入视频页面
  # driver.get(url)
  # 等待页面加载完成
  time.sleep(random.uniform(3,5))
  # 更改当前窗口
  driver.switch_to.window(driver.window_handles[-1])
  # 获取页面源码 以便正则
  bilibili = driver.page_source
  # 标题
  title = driver.find_element(By.XPATH, '//*[@id="viewbox_report"]/div[1]/div/h1')

  # 正则提取视频url
  info = re.findall('window.__playinfo__=(.*?)</script>', bilibili)[0]
  # print(info)

  json_data = json.loads(info)
  # print(json_data)

  video_base_url = json_data['data']['dash']['video'][0]['base_url']
  audio_base_url = json_data['data']['dash']['audio'][0]['base_url']

  return title.text, video_base_url, audio_base_url

def sanitize_filename(filename):
    # 定义不合规字符的正则表达式
    invalid_chars_regex = r'[\"*<>?\\|/:,]'
    # 替换不合规字符为空格
    if invalid_chars_regex == '?':
       sanitized_filename = re.sub(invalid_chars_regex, '？', filename)
       return sanitized_filename
    sanitized_filename = re.sub(invalid_chars_regex, ' ', filename)
    return sanitized_filename

def donwload_video(url, file_name):
  global video_name
  # 规范化文件名
  # file_name = sanitize_filename(file_name)
  # 尝试获取内容
  # full_path = os.path.join(current_path, '哔站', video_name, file_name)

  # 应客户需求更改下载位置
  full_path = os.path.join('D:\哔站视频', video_name, file_name)

  # 下载文件
  try:
    response = requests.get(url, headers=headers, stream=True)
    # 写入文件
    with open(full_path, 'wb') as f:
      f.write(response.content)
    print(f'{file_name} 下载完成')
  except Exception as e:
    print(f'{file_name} 下载失败\n',e)

def action_download(src):

  # 获取视频先关信息
  video_info =  get_videoInfo(src)

  # 下载视频相关文件
  global video_name
  video_name = video_info[0]
  # 规范化文件名
  video_name = sanitize_filename(video_name)

  video = video_info[1]
  audio = video_info[2]

  full_path = os.path.join('D:\哔站视频', video_name)
  # 创建文件夹
  if not os.path.exists(full_path):
    os.makedirs(full_path)
  # 下载视频和音频
  donwload_video(video, f'{video_name}.mp4')
  time.sleep(random.uniform(1,3))
  donwload_video(audio, f'{video_name}.mp3')
  time.sleep(random.uniform(1,3))

def merge_video_audio():
  global video_name
  title = video_name
  root_path = f'D:\哔站视频\{video_name}'
  MP3_file = root_path + f'\{video_name}.mp3'
  MP4_file = root_path + f'\{video_name}.mp4'
  # 合并视频和音频
  try:
    video_clip = VideoFileClip(MP4_file)
    audio_clip = AudioFileClip(MP3_file)
    final_clip = video_clip.set_audio(audio_clip)
    final_clip.write_videofile(root_path + f'\{video_name}合并.mp4', codec='libx264', audio_codec='aac')
    print(f'{title} 合并完成')
    # 删除临时文件
    # os.remove(MP4_file)
    # os.remove(MP3_file)
  except Exception as e:
    return e
    print(f'{title} 合并失败\n',e)

def close_driver():
  driver.quit()
  pass

if __name__ == '__main__':
  
  pre()
  
  # 测试版
  # keyword = input('请输入关键字')
  # search_video(keyword)
  
  # 开始搜索
  search_video()

  # 点击需要的结果
  get_need_search_result()

  # 需要下载的视频链接
  # need_download_url = search_result_list['url'][num-1]

  # 合并视频和音频
  merge_video_audio()

  # 关闭浏览器
  close_driver()

  input('请输入更多...')