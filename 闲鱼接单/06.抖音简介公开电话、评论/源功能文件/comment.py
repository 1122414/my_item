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
for i in range(len(search_info)):
  page.get('https://www.douyin.com/search/%E6%88%8F%E5%89%A7%E7%94%A8%E5%93%81?type=video')
  page.wait(30)
  page.ele('x://*[@id="douyin-header"]/div[1]/header/div/div/div[1]/div/div[2]/div/div/input').clear()
  page.actions.click('x://*[@id="douyin-header"]/div[1]/header/div/div/div[1]/div/div[2]/div/div/input').input(search_info[i])
  for j in range(1,1000):
    
    
    # 定位点击第一个视频
    page.ele('x://*[@id="search-content-area"]/div/div[1]/div[2]/div[2]/ul/li[1]').click()
    page.wait(3)

    # 点击评论按钮
    page.ele('x://*[@id="sliderVideo"]/div[1]/div[1]/div/div[1]/div[2]/div[3]').click()
    page.wait(3)

    # 点击评论框
    page.ele('x://*[@id="merge-all-comment-container"]/div/div[4]/div[2]/div/div[1]').click()
    page.wait(2)

    # 输入评论内容
    page.ele('x://*[@id="merge-all-comment-container"]/div/div[4]/div[2]/div/div[1]').input('测试评论')
    page.wait(2)

    # 点击发送
    try:
      page.ele('x://*[@id="merge-all-comment-container"]/div/div[4]/div[2]/div/div[2]/div/span[4]').click()
      print(f'{search_info[i]}个关键字：第{j}个视频评论成功')
    except Exception as e:
      print(e)
      continue

    # 点击到下一个视频 等待加载
    # //*[@id="sliderVideo"]/div[1]/div[1]/div/div[1]/div[1]/div/div/div[2]
    page.ele('x://*[@id="sliderVideo"]/div[1]/div[1]/div/div[1]/div[1]/div/div/div[2]').click()
    page.wait(2)

