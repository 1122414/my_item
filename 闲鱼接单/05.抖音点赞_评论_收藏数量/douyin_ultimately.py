import re
import os
import json
import requests
from time import sleep
from DrissionPage import ChromiumPage, ChromiumOptions

current_path = os.path.dirname(__file__)
full_path = os.path.join(current_path, 'test_url.txt')
co = ChromiumOptions().headless(True)
# co.set_argument('--incognito')
# co.set_argument('--no-sandbox')
page = ChromiumPage()

url_txt = requests.get('https://xcx.cxsjqy.cn:8093/project/workList/getVideoUrlList',verify=False)
url_json_list = json.loads(url_txt.text)['data']

call_back_url = 'https://xcx.cxsjqy.cn:8093/project/workList/getPyList'
  # pattern = re.compile(r'https://v.douyin.com/\w+')

  # for i in range(len(url_json_list)):
  #   url = url_json_list[i]['url']
  #   url_true = re.findall(pattern, url)
  #   url_list.append(url_true)
  #   user_id.append(url_json_list[i]['userId'])
  #   number_id = url_json_list[i]['numberId']

def get_douyin_data():
  response_data = []
  i = 1
  for url_json in url_json_list:
    # 抖音部分
    dict_data = {}
    pattern = re.compile(r'https://v.douyin.com/\w+')
    true_url = re.findall(pattern, url_json['url'])

    # 看是否是抖音链接
    if true_url:
      page.get(true_url[0])
      page.wait(3)
      try:
        target_big_box = page.ele('.dkgrBha5')
        favrite = target_big_box.child(1).child(1).child(2).text
        comment = target_big_box.child(2).child(1).child(2).text
        collect = target_big_box.child(3).child(2).text
        share = page.ele('.S1XIwUxW').text
        
      except Exception as e:
        # print(e)
        img_span = page.eles('.G0CbEcWs')
        if len(img_span)!= 4:
          # print(f'当前为：{url}，您要观看的视频不存在！错误为\n{e}')
          dict_data['url'] = true_url[0]
          dict_data['favrite'] = None
          dict_data['comment'] = None
          dict_data['collect'] = None
          dict_data['share'] = None
          dict_data['userId'] = url_json['userId']
          dict_data['numberId'] = url_json['numberId']
          response_data.append(dict_data)
          print(f'第{i}条数据')
          i+=1
          continue
        favrite = img_span[0].text
        comment = img_span[1].text
        collect = img_span[2].text
        share = img_span[3].text
        # print(f'当前为：{url}，错误为\n{e}')

    # 快手部分
    else:
      pattern = re.compile(r'https://v.kuaishou.com/\w+')
      true_url = re.findall(pattern, url_json['url'])
      page.get(true_url[0])
      page.wait(3)
      try:
        # 快手分享的视频只有点赞数量
        favrite = page.ele('x://*[@id="app"]/div[1]/section/div/div/div/div[2]/div[1]/div[1]/div[3]/div[1]/div/span[2]').text
        comment = None
        collect = None
        share = None
      except Exception as e:
        # print(e)
        dict_data['url'] = true_url[0]
        dict_data['favrite'] = None
        dict_data['comment'] = None
        dict_data['collect'] = None
        dict_data['share'] = None
        dict_data['userId'] = url_json['userId']
        dict_data['numberId'] = url_json['numberId']
        response_data.append(dict_data)
        print(f'第{i}条数据')
        i+=1
        continue

        # print(f'当前为：{url}，错误为\n{e}')

    # 添加处理数据
    dict_data['url'] = true_url[0]
    dict_data['favrite'] = favrite
    dict_data['comment'] = comment
    dict_data['collect'] = collect
    dict_data['userId'] = url_json['userId']
    dict_data['numberId'] = url_json['numberId']
    if share == '分享':
      dict_data['share'] = 0
    else:
      dict_data['share'] = share
    # print(f'第{i}次{dict_data}')

    response_data.append(dict_data)
    # print(f'第{i}次{response_data}')
    # i += 1
    print(f'第{i}条数据')
    i+=1
  page.quit()
  return response_data

if __name__ == '__main__':
  data = get_douyin_data()
  print(data)
  response = requests.post(call_back_url, json = data, verify=False)
  if response.status_code == 200:
    print('数据上传成功')
  else:
    print('数据上传失败')
# with open(full_path, 'w', encoding='utf-8') as f:
#     f.write(urls.text)

# print(urls.text)