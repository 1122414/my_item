# 根据head里的meta charset="gbk"
# 或者
# import chardet
# encoding = chardet.detect(response.content)['encoding']
import os
import time
import random
import requests
from lxml import etree

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

def single_page():
  for i in range(len(img_list)):
    img_src = 'https://pic.netbian.com'+img_list[i]
    img_name = img_name_list[i]
    # 注意此处文件名称要符合规范  类似*.jpg这种不能出现
    img_name = img_name.replace('*','_')
    img_path = os.path.join(current_dir,'4k图片\\', img_name+'.jpg')
    img_data = requests.get(url=img_src,headers=headers).content

    # 下载图片
    print('正在下载第{}张图片：{}'.format(i+1, img_name))
    with open(img_path,'wb') as f:
      f.write(img_data)

if not os.path.exists('4k图片'):
  os.mkdir('4k图片')

# 循环下载
for i in range(1,100):
  # 随机休眠
  sleep_time = random.randint(1,i%10+3)
  print(f"正在下载第{i}页，休眠{sleep_time}秒\n")
  time.sleep(sleep_time)

  # i=1时，url为https://pic.netbian.com/4kmeinv/
  if i == 1:
    url = 'https://pic.netbian.com/4kmeinv/'
  else:
    url = f'https://pic.netbian.com/4kmeinv/index_{i}.html'
  response = requests.get(url, headers=headers)
  response.encoding = 'gbk'
  page_text = response.text

  if page_text == '':
    print(f"下载完成！共{i}页")
    break

  # 解析xpath数据
  tree = etree.HTML(page_text)
  img_list = tree.xpath('//ul[@class="clearfix"]//img/@src')
  img_name_list = tree.xpath('//ul[@class="clearfix"]//b/text()')

  current_dir = os.path.dirname(__file__)

  single_page()

print("下载完成！")