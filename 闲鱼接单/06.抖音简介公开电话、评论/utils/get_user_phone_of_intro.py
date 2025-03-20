# 进入主页版本  后面发现不用进入主页  在搜索用户页面就能直接拿到电话号码
import re
import requests
from DrissionPage import ChromiumPage,ChromiumOptions

url = 'https://www.douyin.com/user/MS4wLjABAAAASrtEicbAzjJvFd4RSwVkiQITRSMHwEDZ-9qv8LOOXgw?from_tab_name=main'

co = ChromiumOptions().headless(True)
page = ChromiumPage(co)
page.get(url)
page.wait(3)
print(page.ele('x://*[@id="douyin-right-container"]/div[2]/div/div/div[2]/div[2]/div[2]/div[1]/div[2]').text)
print(page.ele('x://*[@id="douyin-right-container"]/div[2]/div/div/div[2]/div[2]/div[3]/div/div/span').text)
page.actions.hold('x://*[@id="douyin-right-container"]/div[2]/div/div/div[2]/div[2]/div[3]/div/div/span')

need = page.ele('x://*[@id="douyin-right-container"]/div[2]/div/div/div[2]/div[2]/div[3]/div/p')
pattern = re.compile(r'1[3-9]\d{9}')
phone = re.findall(pattern, need.text)
# 获取到简介里的电话号码
print(phone[0])

