# 广度例子  弃用
# 直接进不去 ip给封了

import os
import json
import subprocess
import pymysql
from DrissionPage import ChromiumPage,ChromiumOptions
from DrissionPage.common import By

# 命令行打开
subprocess.Popen('"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9527 --user-data-dir="E:\selenium\AutomationProfile"')

current_path = os.path.dirname(__file__)
full_path = os.path.join(current_path, 'hackforums_content.html')
co = ChromiumOptions().set_local_port(9527)
page = ChromiumPage(addr_or_opts=co)

conn = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='3306',
            database='torbot',
            charset='utf8'
        )
cursor = conn.cursor()

page.get('https://hackforums.net/')
print(page.title)

# 将网页文件写入本地
with open(full_path, 'w', encoding='utf-8') as f:
    f.write(page.html)


# 获取各个论坛元素
forum_content_list = page.eles('xpath://div[@class="forum-content"]/div')
forum_content_info = {}
forum_content_info['big_block_name'] = []
forum_content_info['big_block_link'] = []
forum_content_info['title'] = []
forum_content_info['link'] = []
forum_content_info['Threads'] = []
forum_content_info['Posts'] = []
forum_content_info['Last_Post'] = {}
forum_content_info['Last_Post']['Author'] = []
forum_content_info['Last_Post']['Time'] = []
forum_content_info['Last_Post']['Content'] = []

# 遍历各个论坛元素，获取标题和链接 共i个大论坛模块 其中每个大模块又包含若干小模块
for i in forum_content_list:
  forum_info_in_i = i.eles('xpath://tr')
  # 第一个tr是论坛名称
  forum_name = forum_info_in_i[0].ele('xpath://strong/a/text()')
  print('大论坛名称：', forum_name)
  forum_link = "https://hackforums.net/"+forum_info_in_i[0].ele('xpath://strong/a/@href')
  print('大论坛链接：', forum_link)
  # 第二个tr是表头，从第三个tr开始才是论坛信息
  for j in range(2,len(forum_info_in_i)):
    title = forum_info_in_i[j].ele('xpath://div[@class="td-foat-left mobile-link"]//a/text()')
    link = "https://hackforums.net/"+forum_info_in_i[j].ele('xpath://div[@class="td-foat-left mobile-link"]//a/@href')
    Threads = forum_info_in_i[j].eles('xpath://td')[2].text
    Posts = forum_info_in_i[j].eles('xpath://td')[3].text
    Last_Post_Content = forum_info_in_i[j].ele('xpath://span[@class="smalltext"]/a[1]/text()')
    Last_Post_Author = forum_info_in_i[j].ele('xpath://span[@class="smalltext"]/a[2]//text()')

    try:
      # 此处有可能不是span 像第一页的Wifi 5G WPA WEP Bluetooth Wireless Hacking
      Last_Post_Time = forum_info_in_i[j].ele('xpath://span[@class="smalltext"]/span/text()') + '--------concrete_time:' +forum_info_in_i[j].ele('xpath://span[@class="smalltext"]/span/@title')
    except Exception as e:
       print(f"Error: {e}")
    forum_content_info['big_block_name'].append(forum_name)
    forum_content_info['big_block_link'].append(forum_link)
    forum_content_info['title'].append(title)
    forum_content_info['link'].append(link)
    forum_content_info['Threads'].append(Threads)
    forum_content_info['Posts'].append(Posts)
    forum_content_info['Last_Post']['Author'].append(Last_Post_Author)
    forum_content_info['Last_Post']['Time'].append(Last_Post_Time)
    forum_content_info['Last_Post']['Content'].append(Last_Post_Content)

    # 写入数据库
    try:
        sql = "INSERT INTO hack_forum(big_block_name, big_block_link, title, link, threads, posts, last_post_author, last_post_time, last_post_content) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (forum_name, forum_link,title, link, Threads, Posts, Last_Post_Author, Last_Post_Time, Last_Post_Content)
        cursor.execute(sql, val)
        conn.commit()
    except Exception as e:
        print(f"Error: {e}")

    print('标题：', title)
    print('链接：', link)
    print('主题数：', Threads)
    print('回复数：', Posts)
    print('最后回复：', Last_Post_Author, Last_Post_Time, Last_Post_Content)
    print('----------------------')

# 保存为json文件
full_path = os.path.join(current_path, 'hackforums_content.json')
with open(full_path, 'w', encoding='utf-8') as f:
    json.dump(forum_content_info, f, ensure_ascii=False, indent=4)

cursor.close()
conn.close()
input()