from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains

bro = webdriver.Chrome()
bro.get("https://qzone.qq.com/")

# 定位密码登录
# 坑 在ifram里！
bro.switch_to.frame('login_frame')
login_type = bro.find_element(By.ID,'switcher_plogin')
login_type.click()

# 定位输入用户名密码
input_user_name = bro.find_element(By.ID, 'u')
input_user_name.send_keys('758370266')
input_password = bro.find_element(By.ID, 'p')
input_password.send_keys('MengShang..')

# 点击登录
login_button = bro.find_element(By.ID, 'login_button')
login_button.click()

# 注：现在QQ空间需要图片验证码+熟悉环境登录

input()