import re
import os
import json
import time
import tkinter as tk
import tkinter.messagebox
from tkinter import ttk
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

def clear():
# 清空之前的搜索结果
  for i in tree_view.get_children():
    tree_view.delete(i)

def get_douyin_data():
  response_data = []
  i = 1

  # # 清空之前内容
  # for i in tree_view.get_children():
  #   tree_view.delete(i)

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
    tree_view.insert('', 'end', values=(dict_data['url'],dict_data['favrite'],dict_data['comment'],dict_data['collect'],dict_data['share'],dict_data['userId'],dict_data['numberId']))

    tree_view.update()
    time.sleep(1)
  page.quit()


  # # 清空之前内容
  # for i in tree_view.get_children():
  #   tree_view.delete(i)

  # # 将搜索结果添加进treeview
  # for i in range(len(response_data)):
  #   tree_view.insert('', 'end', values=(i+1,response_data[i]['url'],response_data[i]['favrite'],response_data[i]['comment'],response_data[i]['collect'],response_data[i]['share'],response_data[i]['userId'],response_data[i]['numberId']))

  # 上传数据
  response = requests.post(call_back_url, json = response_data, verify=False)
  if response.status_code == 200:
    print('数据上传成功')
  else:
    print('数据上传失败')
  # return response_data

# 创建页面
root = tk.Tk()
# 设置标题
root.title("抖音点赞等数据爬取器")
# 设置窗口大小
root.geometry("1200x800")
# 设置标签
search_frame = tk.Frame(root)
search_frame.pack(pady=20)
# 设置可变变量
name_va = tk.StringVar()
# 设置文本
# tk.Label(search_frame, text="搜索关键字：",font=('微软雅黑',10)).pack(side=tk.LEFT,padx=10)
# 设置输入框
# tk.Entry(search_frame, relief=tk.FLAT, textvariable=name_va,font=('微软雅黑',10), width=30).pack(side=tk.LEFT,padx=10)

# 设置按钮域
button_frame = tk.Frame(root)
button_frame.pack(pady=20)

# 设置爬取按钮
tk.Button(button_frame, text="开始爬取", relief=tk.FLAT, bg='#88e2d6',font=('微软雅黑',10), width=10, command=get_douyin_data).pack(side=tk.LEFT,padx=10)

# 设置清空按钮
tk.Button(button_frame, text="清空内容", relief=tk.FLAT, bg='#88e2d6',font=('微软雅黑',10), width=10, command=clear).pack(side=tk.LEFT,padx=10)

# 设置标签名和中文显示内容
column = ('url','favrite','comment','collect','share','userId','numberId')
column_value = ('链接：','点赞：','评论：','收藏：','分享：','用户ID：','数目ID：')
tree_view = ttk.Treeview(root, height=18, columns=column, show='headings')

# 设置列名
tree_view.column('url',width=50,anchor='center')
tree_view.column('favrite',width=50,anchor='center')
tree_view.column('comment',width=50,anchor='center')
tree_view.column('collect',width=50,anchor='center')
tree_view.column('share',width=50,anchor='center')
tree_view.column('userId',width=50,anchor='center')
tree_view.column('numberId',width=50,anchor='center')


# 设置列名标题
tree_view.heading('url',text='链接：')
tree_view.heading('favrite',text='点赞：')
tree_view.heading('comment',text='评论：')
tree_view.heading('collect',text='收藏：')
tree_view.heading('share',text='分享：')
tree_view.heading('userId',text='用户ID：')
tree_view.heading('numberId',text='数目ID：')

tree_view.pack(side=tk.LEFT,fill=tk.BOTH,expand=1)

# 展示界面
root.mainloop()

# if __name__ == '__main__':
  # data = get_douyin_data()
  # print(data)
  
# with open(full_path, 'w', encoding='utf-8') as f:
#     f.write(urls.text)

# print(urls.text)