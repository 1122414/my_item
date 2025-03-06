# from DrissionPage import SessionPage
import re
import json
import requests
from os import path
from time import sleep
from flask import Flask,request,jsonify
from gevent import pywsgi
from DrissionPage import ChromiumPage, ChromiumOptions


co = ChromiumOptions().headless(True)
co.set_argument('--incognito')
co.set_argument('--no-sandbox')
page = ChromiumPage(co)
app = Flask(__name__)
# 指定外网访问的路径和方式
@app.route('/get_data', methods=['POST'])
def get_data():
  response_data = []
  
  # url = request.args.get('url','No Name Provided')
  data = request.get_json()
  # print(f'当前传入的数据是：{data}')
  # array_data = data if isinstance(data, list) else []
  # print(array_data)
  # i = 0
  # print(f'当前传入的数组文件是：{array_data}')
  # print(data['links'])
  # print(data['links'][1])
  # print(data['links'][1]['url'])
  # i = 0
  for url in data['links']:
    print(url['url'])
    pattern = re.compile(r'https://v.douyin.com/\w+')
    url_true = re.findall(pattern, url['url'])
    print(f'当前url为：{url_true}')
    print(f'当前url为：{url_true[0]}')
    page.get(url_true[0])
    page.wait(2)

    try:
      favrite = page.ele('.M7M0nmSI aKy92uTH Y7dISI5p').text
      comment = page.ele('.SfwAcdr1 JrV13Yco').text
      collect = page.ele('.JQCocDWm NT67BHnx').text
      share = page.ele('.MQXEGdYW').text
      # print('当前为视频链接')
    except Exception as e:
      img_span = page.eles('.G0CbEcWs')
      if len(img_span)!= 4:
        # print(f'当前为：{url}，您要观看的视频不存在！错误为\n{e}')
        return []
      favrite = img_span[0].text
      comment = img_span[1].text
      collect = img_span[2].text
      share = img_span[3].text
      # print(f'当前为：{url}，错误为\n{e}')
    dict_data = {}
    dict_data['url'] = url_true[0]
    dict_data['favrite'] = favrite
    dict_data['comment'] = comment
    dict_data['collect'] = collect
    dict_data['userId'] = url['userId']
    dict_data['numberId'] = url['numberId']
    if share == '分享':
      dict_data['share'] = 0
    else:
      dict_data['share'] = share
    # print(f'第{i}次{dict_data}')

    response_data.append(dict_data)
    # print(f'第{i}次{response_data}')
    # i += 1
  page.quit()
  return response_data

app.run(debug=True,port=3380,host='0.0.0.0')
if __name__ == '__main__':
  server = pywsgi.WSGIServer(('0.0.0.0', 3380), app)
  server.serve_forever()