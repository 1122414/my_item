# 未成功
import os
import requests
from lxml import etree

#!/usr/bin/env python
# coding:utf-8

import requests
from hashlib import md5

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

url = 'https://www.gushiwen.cn/user/login.aspx?from=http://www.gushiwen.cn/user/collect.aspx'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
}
session = requests.Session()
current_path = os.path.dirname(__file__)
page_text = session.get(url, headers=headers).text
tree = etree.HTML(page_text)
code_img_src = 'https://so.gushiwen.org'+tree.xpath('//*[@id="imgCode"]/@src')[0]
img_data = session.get(code_img_src, headers=headers).content
with open(f'{current_path}\\code.jpg', 'wb') as f:
    f.write(img_data)

# 验证码识别
chaojiying = Chaojiying_Client('758370266', 'MengShang..', '937141')	
im = open(f'{current_path}\\code.jpg', 'rb').read()
# print (chaojiying.PostPic(im,1004))
# 以上返回json串{'err_no': 0, 'err_str': 'OK', 'pic_id': '1258419080933660001', 'pic_str': 'orkt', 'md5': '422921e3ae5449d23e46f67ad32ce943'}
# print("图片验证码为：")
print (chaojiying.PostPic(im,1004)["pic_str"])
# print(f"图片验证码为：{chaojiying.PostPic(im,1004)["pic_str"]}")
# 模拟登录

login_url = 'https://www.gushiwen.cn/user/login.aspx?from=http://www.gushiwen.cn/user/collect.aspx'
params = {
    # 应该是反爬机制 每次都变化
  '__VIEWSTATE': 'r0LkjtOExk8obijL61/Zo/48TBhru78f0gutupF/QlGT7LnxjnzDmwlzCK3KjSz9JiJ/sMAR4IsxENr6JIZeI38oCIoIJaqojqm1I/Jc6oVaiqnzT/lAo94LspdY2hrEyXLkIO67Yj5m7c8t8Z2FJd0EGQU=',
  '__VIEWSTATEGENERATOR': 'C93BE1AE',
  'from': 'http://www.gushiwen.cn/user/collect.aspx',
  'email': '758370266@qq.com',
  'pwd': 'MengShang..',
  # code对应的即验证码
  'code': chaojiying.PostPic(im,1004)["pic_str"],
  'denglu': '登录'
}

# cookie登录
# 使用session进行post请求
login_response = session.post(login_url, data=params, headers=headers)
# 爬取当前用户个人主页对应页面数据
detail_url = 'https://www.gushiwen.cn/user/collect.aspx'
# 使用携带cookie的session进行get请求
detail_page_text = session.get(detail_url, headers=headers).text

with open(f'{current_path}\\login_response.html', 'w', encoding='utf-8') as f:
    f.write(detail_page_text)