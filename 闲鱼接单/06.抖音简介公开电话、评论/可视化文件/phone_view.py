import re
import os
import json
import tkinter as tk
import datetime
import tkinter.messagebox
from tkinter import ttk
from DrissionPage import ChromiumPage,ChromiumOptions

# current_path = os.path.dirname(os.path.abspath(__file__))
# full_path = os.path.join(current_path, 'phone_number.txt')

current_path = os.path.dirname(os.path.abspath(__file__))

co = ChromiumOptions()
# co.set_argument('--headless')
co.set_argument('--start-maximized')
page = ChromiumPage(co)

def clear():
# 清空之前的搜索结果
  for i in tree_view.get_children():
    tree_view.delete(i)

def get_phone_number():
  
  key_word = name_va.get()
  phone_data = []
  # search_info = ['戏剧用品','戏剧头饰']
  phone_num = 0
  # for i in range(len(search_info)):

  # 清空输入并搜索关键字
  page.get('https://www.douyin.com/root/search/%E6%88%8F%E5%89%A7%E7%94%A8%E5%93%81?type=user')
  
  # 设置cookies
  full_path = os.path.join(current_path, 'douyin_cookies.json')
  with open(full_path, 'r', encoding='utf-8') as f:
    data_array = json.load(f)
  page.set.cookies(data_array)

  # 有可能触发验证码
  page.wait(30)
  # //*[@id="douyin-header"]/div[1]/header/div[1]/div/div[1]/div/div[2]/div/div/input
  page.ele('x://*[@id="douyin-header"]/div[1]/header/div[1]/div/div[1]/div/div[2]/div/div/input').clear()
  # //*[@id="douyin-header"]/div[1]/header/div/div/div[1]/div/div[2]/div/div/input
  page.actions.click('x://*[@id="douyin-header"]/div[1]/header/div[1]/div/div[1]/div/div[2]/div/div/input').input(key_word)
  page.actions.click('x://*[@id="douyin-header"]/div[1]/header/div[1]/div/div[1]/div/div[2]/div/button')

  # 滚动等待加载元素
  for i in range(50):
    page.wait(10)
    page.scroll.to_bottom()
    try:
      page.ele('.shrAJJLa').click()
      break
    except:
      pass
  # 获取用户列表
    # //*[@id="search-content-area"]/div/div[1]/div[2]/div[3]/ul/li[98]/div/a/p
  user_intro_list = page.eles('x://*[@id="search-content-area"]/div/div[1]/div[2]/div[3]/ul/li/div/a/p')
  # 准备写入文件  数据在D:\phone\phone_{keyword}.txt  不同关键字不同电话号码文件
  full_path = f'D:\phone\phone_{key_word}.txt'
  # 记录获取电话号码的时间
  theTime = datetime.datetime.now()
  f = open(full_path, 'a', encoding='utf-8')
  f.write(str(theTime) + '\n')
  
  # 遍历用户列表，获取用户简介
  for user_intro in user_intro_list:
    # print(user_intro.text)
    pattern = re.compile(r'1[3-9]\d{9}')
    phone = re.findall(pattern, user_intro.text)
    if phone:
      for i in range(len(phone)):
        phone_num += 1
        phone_data.append(phone[i])
        f.write(phone[0] + '\n')
        print(f'获取到第{phone_num}个电话号码：{phone[i]}')
        # 添加并更新
        tree_view.insert('', 'end', values=(phone_num, phone[i]))
        tree_view.update()
      
  f.close()
  print(f'\n共获取到{phone_num}个电话号码')
  tree_view.insert('','end',values=('',f'共获取到{phone_num}个电话号码'))
  tree_view.update()
  # tkinter.messagebox.showinfo("提示：",f'{key_word}关键字共找到{phone_num}个电话号码')

# 创建页面
root = tk.Tk()
# 设置标题
root.title("抖音公开电话号码爬取器")
# 设置窗口大小
root.geometry("800x400")
# 设置标签
search_frame = tk.Frame(root)
search_frame.pack(pady=20)
# 设置可变变量
name_va = tk.StringVar()
# 设置文本
tk.Label(search_frame, text="搜索关键字：",font=('微软雅黑',10)).pack(side=tk.LEFT,padx=10)
# 设置输入框
tk.Entry(search_frame, relief=tk.FLAT, textvariable=name_va,font=('微软雅黑',10), width=30).pack(side=tk.LEFT,padx=10)

# 设置按钮域
button_frame = tk.Frame(root)
button_frame.pack(pady=20)

# 设置搜索按钮
tk.Button(button_frame, text="开始爬取", relief=tk.FLAT, bg='#88e2d6',font=('微软雅黑',10), width=10, command=get_phone_number).pack(side=tk.LEFT,padx=10)

# 设置清空按钮
tk.Button(button_frame, text="清空内容", relief=tk.FLAT, bg='#88e2d6',font=('微软雅黑',10), width=10, command=clear).pack(side=tk.LEFT,padx=10)

# 设置标签名和中文显示内容
column = ('id','phone')
column_value = ('序号','电话号码')
tree_view = ttk.Treeview(root, height=18, columns=column, show='headings')

# 设置列名
tree_view.column('id', width=50, anchor='center')
tree_view.column('phone', width=150, anchor='center')


# 设置列名标题
tree_view.heading('id',text='序号')
tree_view.heading('phone',text='电话号码：')

tree_view.pack(side=tk.LEFT,fill=tk.BOTH,expand=1)

# 展示界面
root.mainloop()