# 未成功
import os
import time
import requests
from lxml import etree
from hashlib import md5
from PIL import Image
from selenium.webdriver import ActionChains
#!/usr/bin/env python
# coding:utf-8

import requests
from selenium import webdriver
current_path = os.path.dirname(os.path.abspath(__file__))
class Chaojiying_Client(object):
    def __init__(self, username, password, soft_id):
        self.username = username
        password =  password.encode('utf8')
        self.password = md5(password).hexdigest()
        self.soft_id = soft_id
        self.base_params = {
            'user': self.username,
            'pass2': self.password,
            'softid': self.soft_id,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
        }

    def PostPic(self, im, codetype):
        """
        im: 图片字节
        codetype: 题目类型 参考 http://www.chaojiying.com/price.html
        """
        params = {
            'codetype': codetype,
        }
        params.update(self.base_params)
        files = {'userfile': ('ccc.jpg', im)}
        r = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data=params, files=files, headers=self.headers)
        return r.json()

    def PostPic_base64(self, base64_str, codetype):
        """
        im: 图片字节
        codetype: 题目类型 参考 http://www.chaojiying.com/price.html
        """
        params = {
            'codetype': codetype,
            'file_base64':base64_str
        }
        params.update(self.base_params)
        r = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data=params, headers=self.headers)
        return r.json()

    def ReportError(self, im_id):
        """
        im_id:报错题目的图片ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://upload.chaojiying.net/Upload/ReportError.php', data=params, headers=self.headers)
        return r.json()

bro = webdriver.Chrome()
# 注意：12306目前是手机验证码
bro.get('https://kyfw.12306.cn/otn/resources/login.html')
time.sleep(3)
# save screenshot将当前页面进行截图保存
bro.save_screenshot(current_path+'screenshot.jpg')
# 确定验证码图片对应的左上角和右下角的坐标（裁剪的区域就确定）
code_img = bro.find_element_by_xpath('//*[@id="J-loginImg"]')
location = code_img.location
size = code_img.size
left = location['x']
top = location['y']
right = location['x'] + size['width']
bottom = location['y'] + size['height']
# 裁剪验证码图片
i = Image.open(current_path+'screenshot.jpg')
code_img_name = 'code.jpg'
frame = i.crop((left, top, right, bottom))
frame.save(current_path+'code.jpg')

# 验证码识别
chaojiying = Chaojiying_Client('758370266', 'MengShang..', '9004')	
im = open(f'{current_path}\\code.jpg', 'rb').read()
# print (chaojiying.PostPic(im,1004)["pic_str"])

# 移动鼠标
ActionChains(bro).move_by_offset(100, 100).perform()

