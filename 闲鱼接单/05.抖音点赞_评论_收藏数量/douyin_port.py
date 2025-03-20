# from DrissionPage import SessionPage
import re
import json
import requests
from os import path
from time import sleep
from flask import Flask,request,jsonify,redirect
from gevent import pywsgi
from DrissionPage import ChromiumPage, ChromiumOptions


co = ChromiumOptions().headless(True)
co.set_argument('--incognito')
co.set_argument('--no-sandbox')
page = ChromiumPage(co)
app = Flask(__name__)

# 重定向
@app.before_request
def before_request():
    if request.scheme == 'http':
        return redirect(request.url.replace('http://', 'https://', 1))

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
    # print(f'当前url为：{url_true}')
    # print(f'当前url为：{url_true[0]}')
    page.get(url_true[0])
    page.wait(2)

    try:
      print('开始')
      # root = page.ele('@id=root')
      # target_big_box = root.child(1).child(4).child(2).child(1).child(1).child(2).child(1).child(3).child(2)
      # favrite = page.ele('.JSdgvKUi PkJ9Apgu vV5XGmMB').text
      # print(favrite)
      # comment = page.ele('.ZqP4r55R Gy2SpCRI').text
      # print(comment)
      # collect = page.ele('.J3qBvLDy yRKrLQDB').text
      # print(collect)
      # share = page.ele('.S1XIwUxW').text
      # print(share)
      target_big_box = page.ele('.dkgrBha5')
      favrite = target_big_box.child(1).child(1).child(2).text
      print(favrite)
      comment = target_big_box.child(2).child(1).child(2).text
      print(comment)
      collect = target_big_box.child(3).child(2).text
      print(collect)
      share = page.ele('.S1XIwUxW').text
      # share = target_big_box.child(5).child(1).child(2).text
      print(share)
      print('结束')
      # .child(1)
      # target_big_box1 = target_big_box.child(1)
      # favrite = 

      # print('当前为视频链接')
    except Exception as e:
      print(e)
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

app.run(debug=True,port=3380,host='0.0.0.0',ssl_content=('./xcx/xcx.cxsjqy.cn.pen','./xcx/xcx.cxsjqy.cn.key'))
if __name__ == '__main__':
  server = pywsgi.WSGIServer(('0.0.0.0', 3380), app)
  server.serve_forever()