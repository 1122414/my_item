# from DrissionPage import SessionPage
# 我草 这玩意能绕过cloudflare验证
from DrissionPage import ChromiumPage
from DrissionPage.common import By

page = ChromiumPage()
# page = SessionPage()
# 至少这个网站行
# page.get('https://www.brownsfashion.com/')
page.wait(30)

favrite = page.ele('.M7M0nmSI aKy92uTH Y7dISI5p')
comment = page.ele('.SfwAcdr1 JrV13Yco')
collect = page.ele('.JQCocDWm NT67BHnx')
share = page.ele('.MQXEGdYW')

print(favrite.text)
print(comment.text)
print(collect.text)
print(share.text)

input()