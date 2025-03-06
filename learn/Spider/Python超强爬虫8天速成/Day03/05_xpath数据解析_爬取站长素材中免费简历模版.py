# 爬取站长素材免费简历模版
import os
import time
import random
import requests
from lxml import etree

# 站长素材大url
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
}

# url = 'https://sc.chinaz.com/jianli/free_3.html'

current_path = os.path.dirname(__file__)
if not os.path.exists(f'{current_path}\\站长素材免费简历模版'):
    os.mkdir(f'{current_path}\\站长素材免费简历模版')

def get_single_page():
  # 每一页全部url的列表
  for url in url_list:
      # 请求单个网页
      response = requests.get(url, headers=headers)
      response.encoding = 'utf-8'
      page_text = response.text
      tree = etree.HTML(page_text)
      url_single = tree.xpath('//ul[@class="clearfix"]/li[4]/a/@href')

      material_data = requests.get(url_single[0], headers=headers).content
      with open(f'{current_path}\\站长素材免费简历模版\\{single_name_list[url_list.index(url)]}.zip', 'wb') as f:
          f.write(material_data)
          print(f"{single_name_list[url_list.index(url)]}.zip下载完成\n")

for i in range(1, 1000):
  # 随机休眠
  sleep_time = random.randint(1,i%10+3)
  print(f"正在下载第{i}页，休眠{sleep_time}秒\n")
  time.sleep(sleep_time)

  if i == 1:
      url = 'https://sc.chinaz.com/jianli/free.html'
  else:
      url = f'https://sc.chinaz.com/jianli/free_{i}.html'
  response = requests.get(url, headers=headers)
  response.encoding = 'utf-8'
  page_text = response.text
  tree = etree.HTML(page_text)
  url_list = tree.xpath('//div[@id="main"]//a[@class="title_wl"]/@href')
  single_name_list = tree.xpath('//div[@id="main"]//img/@alt')
  print(f"正在解析第{i}页\n")
  get_single_page()
  print(f"第{i}页解析完成\n")
