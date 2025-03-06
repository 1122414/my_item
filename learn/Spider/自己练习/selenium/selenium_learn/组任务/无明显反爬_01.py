# http://rznvg5sjacavz5kpshrq4urm75xzruha6iiyuggidnioo5ztvwdfroyd.onion/
# 可以使用！配置好的Tor浏览器

import os
import time
import json
import pymysql
import subprocess
from selenium import webdriver
from lxml import etree
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from DrissionPage.common import from_selenium
from DrissionPage import ChromiumPage,ChromiumOptions
# 连接数据库
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='3306',
    database='python_spider',
    charset='utf8'
)
cur = conn.cursor()
current_path = os.path.dirname(os.path.abspath(__file__))
subprocess.Popen('"E:\Tor_Browser\Browser\\firefox.exe" --marionette --marionette-port 2828')
subprocess.Popen('geckodriver.exe --connect-existing --marionette-port 2828')
# 创建一个新的Firefox选项对象
options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")
# options.add_experimental_option('excludeSwitches', ['enable-automation'])  
# 连接到已经存在的Firefox实例
driver = webdriver.Remote(command_executor="http://localhost:4444", options=options)
# 等到tor网络加载
time.sleep(10)
# 访问目标网页
# driver.get('http://rznvg5sjacavz5kpshrq4urm75xzruha6iiyuggidnioo5ztvwdfroyd.onion/')
# time.sleep(10)

goods_info_list = []
goods_info = {}
def get_shop_data():
  # 自动清空一下数据
  cur.execute('truncate table 01_goods_list')
  full_path = os.path.join(current_path,f'01_goods_list.json')
  with open(full_path,'w',encoding='utf-8') as fp:
    fp.write('')
  # 切换到商店页面
  # 商品总数
  num = 0
  # 获取全部商品div
  # 获取总共有多少页
  all_page = int(driver.find_element(By.XPATH,'/html/body/div[1]/div[3]/div/div/div[13]/a[4]').get_attribute('href').split('-')[1])
  # 一页的数据
  for j in range(1,all_page+1):
    # 9无图  无12
    #  切换页面
    driver.get(f'http://rznvg5sjacavz5kpshrq4urm75xzruha6iiyuggidnioo5ztvwdfroyd.onion/catalog/1-{j}')
    time.sleep(10)
    goods_list = driver.find_elements(By.XPATH,'//div[@class="component"]/div')
    for i in range(1,len(goods_list)-1):
      # 数据初始化
      # true_web_url = ''
      goods_info['rating'] = ''
      goods_info['name'] = ''
      goods_info['img_url'] = ''
      goods_info['description'] = ''
      goods_info['price'] = ''
      goods_info['contacts'] = ''
      goods_info['tags'] = ''
      goods_info['web'] = ''
      try:
        # print(goods_list[i].find_element(By.XPATH,"./div[1]"))
        # print(goods_list[i].find_element(By.XPATH,"./div[1]/a"))
        # print(goods_list[i].find_element(By.XPATH,"./div[1]/a/img").get_attribute('src'))
        try:
          goods_info['rating']=goods_list[i].find_element(By.XPATH,".//div[@class='pull-right']/span").get_attribute('title')
        except Exception as e:
          print(f'错误发生在第{j}页的第{i}条数据,缺少rating')

        try:
          goods_info['name']=goods_list[i].find_element(By.XPATH,".//div[@class='media-body']/h3/a").text
        except Exception as e:
          print(f'错误发生在第{j}页的第{i}条数据,缺少name')

        # 存在图片不存在的情况
        try:
          goods_info['img_url']=goods_list[i].find_element(By.XPATH,"./div[@class='col-md-4 media-gird']/a/img").get_attribute('src')
        except Exception as e:
          goods_info['img_url']=None
          print(f'错误发生在第{j}页的第{i}条数据,缺少img')

        try:
          goods_info['description']=goods_list[i].find_element(By.XPATH,".//div[@class='media-description']/ul/li[1]").text
        except Exception as e:
          goods_info['description']=None
          print(f'错误发生在第{j}页的第{i}条数据,缺少description')

        # 存在price不存在的情况
        try:
          # 看Price是否存在 存在则添加
          goods_info['price']=goods_list[i].find_element(By.XPATH,".//div[@class='media-description']/ul/li/strong[contains(text(),'Price')]/parent::li").text
        except Exception as e:
          goods_info['price']=None
          print(f'错误发生在第{j}页的第{i}条数据,缺少Price')

        # 存在Contacts不存在的情况
        try:
          # 看Contacts是否存在 存在则添加
          goods_info['contacts']=goods_list[i].find_element(By.XPATH,".//div[@class='media-description']/ul/li/strong[contains(text(),'Contacts')]/parent::li").text
        except Exception as e:
          goods_info['contacts']=None
          print(f'错误发生在第{j}页的第{i}条数据,缺少contacts')

        # 存在Tags不存在的情况
        try:
          # 看Tags是否存在 存在则添加
          goods_info['tags'] = goods_list[i].find_element(By.XPATH,".//div[@class='media-description']/ul/li/strong[contains(text(),'Tags')]/parent::li").text
          # parent::
          # 存在则添加
          # goods_info['tags']=goods_list[i].find_element(By.XPATH,".//div[@class='media-description']/ul/li[5]").text
        except Exception as e:
          goods_info['tags']=None
          print(f'错误发生在第{j}页的第{i}条数据,缺少tags')

        # 新页面的xpath  /html/body/div[1]/div[3]/div/div/p[1]/a[2]
        # 点击web蹦出来一个新页面标签  等待几秒后跳转页面
        # 切换标签页
        try:
          # 有web字段
          goods_list[i].find_element(By.XPATH,".//div[@class='media-description']/ul/li/a[contains(text(),'Web')]").click()
          time.sleep(3)
          
          # 切换标签页句柄
          try:
            driver.switch_to.window(driver.window_handles[1])
          except Exception as e:
            print(f'错误发生在第{j}页的第{i}条数据,切换标签页失败')

          # 获取真正链接页面
          try:
            time.sleep(10)
            goods_info['web'] = driver.find_element(By.XPATH,"/html/body/div[1]/div[3]/div/div/p[1]/a[2]").text
          # 页面可能没有
          except Exception as e:
            goods_info['web'] = 'File not found'

          # 有web时，才关闭当前新打开的标签页  有坑
          driver.close()

          # 尝试切回初始页面
          try:
            driver.switch_to.window(driver.window_handles[0])
          except Exception as e:
            print(f'错误发生在第{j}页的第{i}条数据,driver回到初始页面失败')
        except Exception as e:
          goods_info['web']=None
          print(f'错误发生在第{j}页的第{i}条数据,缺少web')

        # 获取真正的web链接
        # /html/body/div[1]/div[3]/div/div/p[1]/a[2]
        time.sleep(3)

        num+=1

        # print(goods_info)
        # 存入json文件
        goods_info_list.append(goods_info)
        full_path = os.path.join(current_path,f'01_goods_list.json')
        with open(full_path,'a',encoding='utf-8') as fp:
          json.dump(goods_info,fp,ensure_ascii=False)
          fp.write('\n')

        # 存入数据库
        cur.execute('insert into 01_goods_list(id,rating,name,img_url,description,price,contacts,tags,web) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)',(int(num),goods_info['rating'],goods_info['name'],goods_info['img_url'],goods_info['description'],goods_info['price'],goods_info['contacts'],goods_info['tags'],goods_info['web']))
        conn.commit()

        # 等待
        time.sleep(10)
      except Exception as e:
        print(f'错误发生在第{j}页的第{i}条数据,错误信息:{e}')

    print(f'目前在第1-{j}页面')
    time.sleep(10)
        # goods_info['web'].append('https://'+goods_list[i].find_element(By.XPATH,".//div[@class='media-description']/ul/li[4]/a").get_attribute('href'))
      # except Exception as e:
      #   print(f'错误发生在第{i}次循环,错误信息:{e}')


# 访问商店  /catalog
driver.get('http://rznvg5sjacavz5kpshrq4urm75xzruha6iiyuggidnioo5ztvwdfroyd.onion/catalog')
time.sleep(10)
list_group = driver.find_elements(By.XPATH, '//div[@class="list-group"]/a')
for i in range(len(list_group)):
  list_group[i].click()
  time.sleep(10)
  match i:
    case 0:
      get_shop_data()
      print(goods_info_list)
  
# /actions

# /content/top.html  popular article

print('爬取结束！')