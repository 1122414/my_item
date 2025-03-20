import os
import re
import subprocess
from DrissionPage import *
# 获取当前路径
current_path = os.path.dirname(__file__)
# 命令行打开目标Chrome浏览器
subprocess.Popen('"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9527 --user-data-dir="E:\selenium\AutomationProfile"')
co = ChromiumOptions()
co.set_local_port(9527)
# co.headless()
page = ChromiumPage(addr_or_opts=co)

if __name__ == '__main__':
  url = 'https://www.xiaohongshu.com/'
  page.get(url)
  page.ele('x://*[@id="search-input"]').input('alevel')
  page.wait(2)
  page.ele('x://*[@id="global"]/div[1]/header/div[2]/div/div[2]').click()

  note_list = page.eles('x://div[@class="feeds-container"]/section[@class="note-item"]')

  for i in range(len(note_list)):
    try:
      print(note_list[i].ele('x://a[@class="title"]/span').text)
    except Exception as e:
      print(f"获取帖子标题时出现错误：{e}")


  page.wait(60)