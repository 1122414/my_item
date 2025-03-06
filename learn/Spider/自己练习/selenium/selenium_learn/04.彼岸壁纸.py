import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By


headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
}

def download_image(image_url_list, image_title_list):
  for i in range(len(image_title_list)):
  # print(image_title_list[i].tag_name)
  # 下面这两个属性有时候取不到，有时候能取到不知道什么情况
  # print(image_title_list[i].text)
  # print(image_title_list[i].accessible_name)
  # image_title = image_title_list[i].text
    image_title = image_title_list[i].get_attribute('innerHTML')
    image_url = image_url_list[i].get_attribute('src')

    # 下载图片
    full_path = os.path.join(current_path,'images',f"{image_title}.jpg")
    response = requests.get(image_url, headers=headers)
    with open(full_path, "wb") as f:
      f.write(response.content)
      print(f"{image_title}.jpg 下载完成")
      time.sleep(1)
    # print(image_title)
    # print(image_url)

# 实例化对象
driver = webdriver.Chrome()

# 访问网页
driver.get("https://pic.netbian.com/4kmeinv/")

current_path=os.path.dirname(__file__)
full_path = os.path.join(current_path,'images')
# 创建images文件夹
if not os.path.exists(os.path.join(current_path,'images')):
  os.mkdir(os.path.join(current_path,'images'))

for i in range(10):
  # 定位
  image_title_list = driver.find_elements(By.XPATH,'//ul[@class="clearfix"]/li/a/b')
  image_url_list = driver.find_elements(By.XPATH,'//ul[@class="clearfix"]/li/a/img')
  # 下载
  download_image(image_url_list, image_title_list)
  print(f"第{i+1}页下载完成")
  time.sleep(1)
  # 翻页
  driver.find_element(By.XPATH,'//*[@id="main"]/div[4]/a[9]').click()