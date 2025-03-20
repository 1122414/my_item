import re
import os
from DrissionPage import ChromiumPage,ChromiumOptions

current_path = os.path.dirname(os.path.abspath(__file__))
full_path = os.path.join(current_path, 'phone_number.txt')

co = ChromiumOptions()
# co.set_argument('--headless')
co.set_argument('--start-maximized')
page = ChromiumPage(co)

phone_data = []
search_info = ['戏剧用品','戏剧头饰']
phone_num = 0
for i in range(len(search_info)):
  page.get('https://www.douyin.com/root/search/%E6%88%8F%E5%89%A7%E7%94%A8%E5%93%81?type=user')
  page.wait(10)
  page.ele('x://*[@id="douyin-header"]/div[1]/header/div/div/div[1]/div/div[2]/div/div/input').clear()
  # //*[@id="douyin-header"]/div[1]/header/div/div/div[1]/div/div[2]/div/div/input
  page.actions.click('x://*[@id="douyin-header"]/div[1]/header/div/div/div[1]/div/div[2]/div/div/input').input(search_info[i])
  
  page.actions.click('x://*[@id="douyin-header"]/div[1]/header/div/div/div[1]/div/div[2]/div/button')

  # 滚动等待加载元素
  for i in range(10):
    page.wait(5)
    page.scroll.to_bottom()

  # 获取用户列表
  user_intro_list = page.eles('x://*[@id="search-content-area"]/div/div[1]/div[2]/div[3]/ul/li/div/a/p')

  # 准备写入文件
  f = open(full_path, 'a', encoding='utf-8')

  # 遍历用户列表，获取用户简介
  for user_intro in user_intro_list:
    # print(user_intro.text)
    pattern = re.compile(r'1[3-9]\d{9}')
    phone = re.findall(pattern, user_intro.text)
    if phone:
      phone_num += 1
      phone_data.append(phone[0])
      f.write(phone[0] + '\n')
      print(f'获取到第{phone_num}个电话号码：{phone[0]}')
    
f.close()
print(f'共获取到{phone_num}个电话号码')