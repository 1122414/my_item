import subprocess
import time 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# 命令行打开
subprocess.Popen('"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9527 --user-data-dir="E:\selenium\AutomationProfile"')

options = Options()
options.add_experimental_option('debuggerAddress','127.0.0.1:9527')

time.sleep(3)
# 打开浏览器
driver = webdriver.Chrome(options=options)

# 访问网页
driver.get("http://mmd32xdcmzrdlpoapkpf43dxig5iufbpkkl76qnijgzadythu55fvkqd.onion/")

input()