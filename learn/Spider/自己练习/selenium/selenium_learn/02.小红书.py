# 目前爬取各个帖子的title
from lxml import etree
from time import sleep
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("https://www.xiaohongshu.com/explore")
# 等待页面加载完成
sleep(5)
# 点击协议
driver.find_element(By.XPATH,'//*[@id="app"]/div[1]/div/div[1]/div[3]/div[3]/span/div').click()
# 输入手机号
# driver.find_element(By.XPATH,'//*[@id="app"]/div[1]/div/div[1]/div[3]/div[2]/form/label[1]/input').click()
phone_number = input('请输入手机号： ')
# sleep(10)
driver.find_element(By.XPATH,'//*[@id="app"]/div[1]/div/div[1]/div[3]/div[2]/form/label[1]/input').send_keys(phone_number)
# 发送验证码
driver.find_element(By.XPATH,'//*[@id="app"]/div[1]/div/div[1]/div[3]/div[2]/form/label[2]/span').click()
# 输入验证码
code = input('请输入手机验证码： ')
# sleep(20)
# driver.find_element(By.XPATH,'//*[@id="app"]/div[1]/div/div[1]/div[3]/div[2]/form/label[2]/input').click()
driver.find_element(By.XPATH,'//*[@id="app"]/div[1]/div/div[1]/div[3]/div[2]/form/label[2]/input').send_keys(code)
# 登录
driver.find_element(By.XPATH,'//*[@id="app"]/div[1]/div/div[1]/div[3]/div[2]/form/button').click()

# 小红书网页版 往下滑会上面的内容会变
s_set = set()
for i in range(1,10):
  # 执行JavaScript来下滑页面
  driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
  driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
  sleep(2)
  a_list = driver.find_elements(By.XPATH, "//a[@class='title']/span")
  for a in a_list:
    s_set.add(a.text)

for s in s_set:
    print(s)

input("Press any key to quit...")