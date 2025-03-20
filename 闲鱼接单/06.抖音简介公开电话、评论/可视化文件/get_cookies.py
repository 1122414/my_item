import os
import json
from DrissionPage import ChromiumPage,ChromiumOptions

current_path = os.path.dirname(__file__)
full_path = os.path.join(current_path, 'douyin_cookies.json')

page = ChromiumPage()

page.get('https://www.douyin.com/root/search/%E6%88%8F%E5%89%A7%E7%94%A8%E5%93%81?type=user')
page.wait(5)

# 等待登录
page.wait(60)
print(page.cookies())

with open(full_path, 'w', encoding='utf-8') as f:
  f.write(json.dumps(page.cookies(),indent=4, ensure_ascii=False))

full_path = os.path.join(current_path, 'douyin_cookies.json')
with open(full_path, 'r', encoding='utf-8') as f:
  data_array = json.load(f)

# page.set.cookies(data_array)
  
print('cookies写入成功')