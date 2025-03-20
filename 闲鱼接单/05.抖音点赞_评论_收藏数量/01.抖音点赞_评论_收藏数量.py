# from DrissionPage import SessionPage
import sys
from os import path
import tkinter as tk
import tkinter.messagebox
from time import sleep
from tkinter import ttk
from DrissionPage import ChromiumPage
from DrissionPage import ChromiumPage, ChromiumOptions
from DrissionPage.common import By

dict_data = {}
co = ChromiumOptions().headless()
page = ChromiumPage(co)

def get_data():
  url = url_va.get()
  page.get(url)
  page.wait(5)

  favrite = page.ele('.M7M0nmSI aKy92uTH Y7dISI5p')
  comment = page.ele('.SfwAcdr1 JrV13Yco')
  collect = page.ele('.JQCocDWm NT67BHnx')
  share = page.ele('.MQXEGdYW')

  dict_data['favrite'] = favrite.text
  dict_data['comment'] = comment.text
  dict_data['collect'] = collect.text
  dict_data['share'] = share.text

  # 清空之前内容
  for i in tree_view.get_children():
    tree_view.delete(i)

  # 将搜索结果添加进treeview
  tree_view.insert('', 'end', values=(dict_data['favrite'],dict_data['comment'],dict_data['collect'],dict_data['share']))

  # print(favrite.text)
  # print(comment.text)
  # print(collect.text)
  # print(share.text)
  page.quit()

def clear():
# 清空之前的搜索结果
  for i in tree_view.get_children():
    tree_view.delete(i)

# 创建页面
root = tk.Tk()
# 设置标题
root.title("抖音点赞、评论、收藏、收藏数量")
# 设置窗口大小
root.geometry("800x600")
# 设置标签
search_frame = tk.Frame(root)
search_frame.pack(pady=20)
# 设置可变变量
url_va = tk.StringVar()
# 设置文本
tk.Label(search_frame, text="搜索网址：",font=('微软雅黑',10)).pack(side=tk.LEFT,padx=10)
# 设置输入框
tk.Entry(search_frame, relief=tk.FLAT, textvariable=url_va,font=('微软雅黑',10), width=30).pack(side=tk.LEFT,padx=10)

# 设置按钮域
button_frame = tk.Frame(root)
button_frame.pack(pady=20)

# 设置搜索按钮
tk.Button(button_frame, text="搜索内容", relief=tk.FLAT, bg='#88e2d6',font=('微软雅黑',10), width=10, command=get_data).pack(side=tk.LEFT,padx=10)

# 设置清空按钮
tk.Button(button_frame, text="清空内容", relief=tk.FLAT, bg='#88e2d6',font=('微软雅黑',10), width=10, command=clear).pack(side=tk.LEFT,padx=10)

# 设置标签名和中文显示内容
column = ('favrite','comment','collect','share')
column_value = ('点赞数：','评论数：','收藏数：','转发数：')
tree_view = ttk.Treeview(root, height=18, columns=column, show='headings')

# 设置列名
tree_view.column('favrite',width=50,anchor='center')
tree_view.column('comment',width=50,anchor='center')
tree_view.column('collect',width=50,anchor='center')
tree_view.column('share',width=50,anchor='center')

# 设置列名标题
tree_view.heading('favrite',text='点赞数：')
tree_view.heading('comment',text='评论数：')
tree_view.heading('collect',text='收藏数')
tree_view.heading('share',text='转发数')

tree_view.pack(side=tk.LEFT,fill=tk.BOTH,expand=1)

# 展示界面
root.mainloop()

input()