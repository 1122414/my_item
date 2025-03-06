# 梨视频 对下述url发起请求解析出视频详情页的url和视频的名称
# https://www.pearvideo.com/category_1

import os 
import json
import requests
from lxml import etree
from multiprocessing.dummy import Pool as ThreadPool

url = "https://www.pearvideo.com/category_1"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}

pool = ThreadPool(10)
urls = []
def get_video_url(url):
    # 获取contId
    response = requests.get(url, headers=headers)
    tree = etree.HTML(response.text)
    video_name_list = tree.xpath('//*[@id="listvideoListUl"]/li/div/a/div[2]/text()')
    video_contId_list = tree.xpath('//*[@id="listvideoListUl"]/li/div/a/@href')
    
    # 获取视频真实地址
    for i in range(len(video_name_list)):
      contId = video_contId_list[i][video_contId_list[i].index('_')+1:]
      video_truth_url_from = 'https://www.pearvideo.com/videoStatus.jsp?'
      params={
        'contId': contId,
        'mrd': '0.7211320510890735'
      }
      headers_truth = {
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
      # Referer 防盗链，代表上一个网站，即从哪进入本网站 注意！
      'Referer':'https://www.pearvideo.com/'+contId
      }
      response_truth = requests.get(video_truth_url_from, headers=headers_truth, params=params).json()

      video_truth_url = response_truth['videoInfo']['videos']['srcUrl']
      dic = {
          'name': video_name_list[i],
          'url': video_truth_url
      }
      urls.append(dic)
      print("视频名称:", video_name_list[i])
      print("视频url:", video_truth_url)
      print("------------------------------------------")

current_path = os.path.dirname(__file__)


def get_video_data(dic):
    # 下载视频
    name = dic['name']
    print("开始下载视频:", name)
    url = dic['url']
    full_path = os.path.join(current_path, name)
    response = requests.get(url, headers=headers)
    with open(full_path+'.mp4', 'wb') as f:
        f.write(response.content)
        print("视频下载完成:", name)

get_video_url(url)

# 使用线程池并发请求
pool = ThreadPool(4)
pool.map(get_video_data, urls)

pool.close()
pool.join()


