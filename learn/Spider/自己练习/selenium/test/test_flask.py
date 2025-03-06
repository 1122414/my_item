# from DrissionPage import SessionPage
from os import path
from time import sleep
from flask import Flask
from DrissionPage import ChromiumPage
from DrissionPage import ChromiumPage, ChromiumOptions

dict_data = {}
co = ChromiumOptions().headless()
page = ChromiumPage(co)

app = Flask(__name__)
# 指定外网访问的路径和方式
@app.route('/douyin_favrite_port')

def douyin_favrite_port():
  return 'hello'

app.run()


input()