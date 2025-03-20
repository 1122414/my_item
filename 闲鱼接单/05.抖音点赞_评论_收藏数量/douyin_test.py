# from DrissionPage import SessionPage
import re
from os import path
from time import sleep
from flask import Flask
from gevent import pywsgi
from DrissionPage import ChromiumPage, ChromiumOptions

current_path = path.dirname(path.abspath(__file__))
full_path = path.join(current_path, '测试.txt')

with open(full_path, 'r', encoding='utf-8') as f:
  all_txt = f.read()

pattern = re.compile(r'https://v.douyin.com/\w+')
urls = re.findall(pattern, all_txt)

dict_data = {}
# co = ChromiumOptions().headless()
page = ChromiumPage()

def get_data(url):
  print(url)
  page.get(url)
  page.wait(3)
  try:
    root = page.ele('@id=root')
    target_big_box = page.ele('.dkgrBha5')
    # target_big_box = root.child(1).child(4).child(2).child(1).child(1).child(2).child(1).child(3).child(2)
    
    favrite = target_big_box.child(1).child(1).child(2).text
    comment = target_big_box.child(2).child(1).child(2).text
    collect = target_big_box.child(3).child(2).text
    share = target_big_box.child(5).child(1).child(2).text
    # .child(1)
    target_big_box1 = target_big_box.child(1)
    # favrite = 
    # favrite = page.ele('.JSdgvKUi PkJ9Apgu vV5XGmMB').text
    # comment = page.ele('.ZqP4r55R Gy2SpCRI').text
    # collect = page.ele('.J3qBvLDy yRKrLQDB').text
    # share = page.ele('.S1XIwUxW').text
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
    
  
  dict_data['favrite'] = favrite
  dict_data['comment'] = comment
  dict_data['collect'] = collect
  dict_data['share'] = share

  # print(favrite.text)
  # print(comment.text)
  # print(collect.text)
  # print(share.text)
  # page.quit()
  print()
  return dict_data

# app.run(debug=True,port=8080,host='0.0.0.0')

if __name__ == '__main__':
  for i in range(len(urls)):
    print(f'第{i}条：')
    print(get_data(urls[i]))
    sleep(1)
  print(dict_data)
  # get_data('https://v.douyin.com/irg1WMsp')

input()