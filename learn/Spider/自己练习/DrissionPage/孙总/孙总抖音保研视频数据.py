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

file_path = os.path.join(current_path, '保研关键词.txt')
random_key = []
with open (file_path,'r',encoding='utf-8') as f:
  for line in f.readlines():
    random_key.append(line.strip())

INPUT_KEYS = random_key[random.randint(0,len(random_key)-1)]
# INPUT_KEYS = '保研群面攻略'
print(f'当前关键词：{INPUT_KEYS}')

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
  'referer':''
  # 'a': '6383',
  # 'ch': '26',
  # 'cr': '3',
  # 'dr': '0',
  # 'lr': 'all',
  # 'cd': '0|0|0|3',
  # 'cv': '1',
  # 'br': '341',
  # 'bt': '341',
  # 'cs': '2',
  # 'ds': '3',
  # 'ft': 't2zLrtjjM95MxrKqoZmCE1RSYV58UMDtGsvHchyq8_45a',
  # 'mime_type': 'video_mp4',
  # 'qs': '15',
  # 'rc': 'NTg4Zjs3OjdkO2dpZjs0NEBpamQ7N3k5cjg1djMzNGkzM0BjYl5gYDNfXi4xY2JfLWIxYSM1aC4uMmRrYDRgLS1kLS9zcw==',
  # 'btag': '80000e00028000',
  # 'dy_q': '1742389319',
  # 'l': '20250319210159C1262529F0A7F12302CC',
  # '__vid': '7425915358181133579'
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
    invalid_chars_regex = r'[\"*<>?\\|/:,]'
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

def extract_audio_from_videos(input_path, output_folder, file_name):
    """
    从指定文件夹中的视频文件提取音频，保存为相同文件名的音频文件。
    
    :param input_folder: 输入视频文件所在的文件夹路径。
    :param output_folder: 输出音频文件保存的文件夹路径。
    """
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # 检查是否为视频文件（可根据需要扩展）
    if input_path.endswith(('.mp4', '.avi', '.mov', '.mkv')):
        # 输出文件路径
        output_file_name = os.path.splitext(file_name)[0] + ".wav"
        output_file_path = os.path.join(output_folder, output_file_name)
        
        # 使用 ffmpeg 提取音频
        try:
            print(f"正在处理: {file_name}")
            # 在 extract_audio_from_videos 函数中优化ffmpeg命令
            command = [
                "ffmpeg",
                "-i", input_path,
                "-ar", "16000",        # 采样率统一为16kHz
                "-ac", "1",            # 单声道
                "-af", "highpass=f=300,lowpass=f=3000",  # 过滤高低频噪声
                output_file_path
            ]
            subprocess.run(command, check=True)
            print(f"提取成功: {output_file_path}")
            return output_file_path
        except subprocess.CalledProcessError as e:
            print(f"提取失败: {file_name}，错误信息: {e}")
    print("所有文件处理完成！")

def get_text(save_path, text_title, model_size="large-v3"):
  '''解析获取文案'''
  """
    使用 Whisper 模型识别文件夹中的音频文件，并输出字幕文件到指定文件夹。

    :param input_folder: 输入音频文件所在的文件夹路径。
    :param output_folder: 输出字幕文件保存的文件夹路径。
    :param model_size: Whisper 模型大小 (如 "tiny", "base", "small", "medium", "large")。
  """
    # 先从视频提取音频
  audio_dir = os.path.join(current_path, 'data' ,'audio_data')
  if not os.path.exists(audio_dir):
      os.makedirs(audio_dir)
  
  audio_address =extract_audio_from_videos(save_path, audio_dir, text_title)

  # 加载 Whisper 模型
  print(f"加载 Whisper 模型: {model_size}...")
  model = whisper.load_model(model_size)

  start_time = time.time()
  # 检查是否为音频文件
  if audio_address.endswith(('.wav', '.mp3', '.m4a', '.flac')):
      print(f"正在处理: {audio_address}")
      try:
          # 识别音频内容
          result = model.transcribe(
            audio_address, 
            language="zh",        # 明确指定中文
            fp16=True,           # CPU用户关闭FP16
            initial_prompt="以下是关于大学保研的对话,请帮我生成对应的文案",  # 上下文提示
            temperature=0.2,      # 降低随机性
            beam_size=5,           # 增强解码稳定性
            word_timestamps=True,  # 启用词语级时间戳
            condition_on_previous_text=False  # 防止错误累积
          )
          return result["text"]
      except Exception as e:
          print(f"处理失败: {audio_address}，错误信息: {e}")
  print("所有文件处理完成！")
  end_time = time.time()
  print(f"处理完成，耗时: {end_time - start_time:.2f}秒")

def get_video_data(response,data):
  '''保存视频'''
  text_title = sanitize_filename(data['title'][0:20])
  save_path = os.path.join(current_path,'video_data', f'{text_title}.mp4')
  with open(save_path, 'wb') as f:
    # 分块写入
    try:
      with open(save_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192, decode_unicode=False):
          if chunk:
            f.write(chunk)
      
      # 完整性校验
      if os.path.getsize(save_path) < 1024 * 100:  # 小于100KB视为无效
        raise ValueError("文件过小可能不完整")
      
      print(f"视频下载完成：{save_path}")
      # 开始解析提取文案
      data['text'] = get_text(save_path, text_title)
    except Exception as e:
      print(f"视频下载失败：{save_path}，错误信息：{e}")

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
    'video_url': '',
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
      new_input_key=random_key[random.randint(0,len(random_key)-1)]
      page.ele('x://*[@id="douyin-right-container"]/div[4]/div[2]/div[1]/div/div/input').input(new_input_key)
      file_path = os.path.join(current_path,'data', f'douyin_data{current_date}_{new_input_key}.csv')
      page.wait(WAIT_TIME)
      page.ele('x://*[@id="douyin-right-container"]/div[4]/div[2]/div[1]/div/button').click()
      page.wait(WAIT_TIME)
      i = 0
      after_search_click0()
      video_list = page.eles('x://*[@id="douyin-right-container"]/div[4]/div[4]/div/div/div/div')
      print(f'跳转到{new_input_key}关键字')
      

    favirate_number = convert_wan_to_number(data_list[1].text)
    comment_number = convert_wan_to_number(data_list[2].text)
    collect_number = convert_wan_to_number(data_list[3].text)
    transmit_number = convert_wan_to_number(data_list[5].text)
    # 权重公式：点赞*0.9+评论*2+收藏*1.8+转发*1.5
    weight = round(favirate_number*0.9+comment_number*2+collect_number*1.8+transmit_number*1.5,2)
    print(f'第{i}个的权重为：{weight}')
    if weight >= 2000:
      data['favirate']=favirate_number
      data['comment']=comment_number
      data['collect']=collect_number
      data['transmit']=transmit_number
      data['title']=video_list[i].ele('x://*[@id="video-info-wrap"]/div[1]/div[2]/div/div[1]/span//span').text
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

      # 获取可下载视频url（注意：有些视频是不能去下载的）
      try:
        # 跳转到新页面
        new_page = page.new_tab(data['url'])
        page.wait(3)
        # 点击暂停
        new_page.actions.key_down(Keys.SPACE)
        # new_page = page.new_tab('https://v.douyin.com/OHUQczya840/')
        # 确认为新页面window
        # print(page.ele('x://*[@id="douyin-right-container"]/div[2]/div/div/div[1]/div[3]/div/div[2]/div[2]/span').text)
        now_tab = page.get_tab()
        video_data_url = new_page.ele('x://*[@id="douyin-right-container"]/div[2]/div/div/div[1]/div[2]/div/xg-video-container/video/source[1]').attr('src')
        data['video_url'] = video_data_url
      except Exception as e:
        print(f'第{i}个视频无法下载，错误原因：{e}，没有下载地址')
        write2csv(file_path, data)
        close_tab_and_scroll(now_tab,video_list[i])
        continue

      # 保存视频
      headers['referer'] = video_data_url
      response = requests.get(url=video_data_url, headers=headers, stream=True)
      if response.status_code == 200:
        get_video_data(response,data)
      else:
        print(f"请求失败，状态码：{response.status_code}，video_data_url为：{video_data_url}")
        write2csv(file_path, data)
        close_tab_and_scroll(now_tab,video_list[i])
        continue

      page.close_tabs(now_tab)

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
  