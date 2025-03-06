import os
import sys 
from os import path
import tkinter as tk
import tkinter.messagebox
from time import sleep
from tkinter import ttk

d = path.dirname(__file__)  # 获取当前路径
parent_path = path.dirname(d)  # 获取上一级路径
sys.path.append(parent_path)    # 如果要导入到包在上一级
# print(sys.path)

from my_selenium_utils import search_my_novel

def clear():
# 清空之前的搜索结果
  for i in tree_view.get_children():
    tree_view.delete(i)

def show():
  novel_name = name_va.get()
  search_my_novel.search_book(novel_name=novel_name)
  search_result = search_my_novel.search_dict
  if len(search_result)==0:
    tkinter.messagebox.showwarning("警告：","没有找到相关小说！")
    return
  # 清空之前的搜索结果
  for i in tree_view.get_children():
    tree_view.delete(i)
  # 将搜索结果添加进treeview
  for i in range(len(search_result['book_name'])):
    tree_view.insert('',i,values=(i+1,search_result['book_author'][i],search_result['book_name'][i],search_result['book_url'][i]))

def download():
  book_num = num_va.get()
  if book_num=='':
    tkinter.messagebox.showwarning("警告：","请输入要下载的小说序号！从1到100！")
    return
  search_my_novel.find_name(book_num)
  # 下载十章
  for i in range(10):
    sleep(3)
    search_my_novel.download_chapter(i+1,search_my_novel.dict_name['book_chapter_head'][i])
  tkinter.messagebox.showinfo("提示：","下载完成！")
  

# 创建界面
root = tk.Tk()
# 设置标题
root.title("小说下载器")
# 设置窗口大小
root.geometry("800x400")
# # 设置窗口背景色
# root.config(bg="white")
# 设置标签
search_frame = tk.Frame(root)
search_frame.pack(pady=20)
# 设置可变变量
name_va = tk.StringVar()
# 设置文本
tk.Label(search_frame,text="书名 作者",font=('微软雅黑',10)).pack(side=tk.LEFT,padx=10)
# 设置输入框
tk.Entry(search_frame, relief=tk.FLAT, textvariable=name_va, width=30).pack(side=tk.LEFT)

# 序号获取
num_va = tk.StringVar()

# 查询下载输入框
download_frame = tk.Frame(root)
download_frame.pack(pady=20)
# 设置文本
tk.Label(download_frame,text="小说 序号",font=('微软雅黑',10)).pack(side=tk.LEFT,padx=10)
# 设置输入框
tk.Entry(download_frame, relief=tk.FLAT, textvariable=num_va,width=30).pack(side=tk.LEFT)

# 按钮设置
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

# 设置查询按钮
tk.Button(button_frame, text="查询", relief=tk.FLAT, bg='#88e2d6',font=('微软雅黑',10), width=10, command=show).pack(side=tk.LEFT,padx=10)
# 设置下载按钮
tk.Button(button_frame, text="下载", relief=tk.FLAT, bg='#88e2d6',font=('微软雅黑',10), width=10, command=download).pack(side=tk.LEFT,padx=10)
# 设置清空按钮
tk.Button(button_frame, text="清空", relief=tk.FLAT, bg='#88e2d6',font=('微软雅黑',10), width=10, command=clear).pack(side=tk.LEFT,padx=10)

# 设置标签名和中文显示内容
column = ('num','writer','name','noverl_url')
column_value = ("序号","作者","书名","书url")
tree_view = ttk.Treeview(root,height=18,show='headings',columns=column)

# 设置列名
tree_view.column('num',width=50,anchor='center')
tree_view.column('writer',width=100,anchor='center')
tree_view.column('name',width=200,anchor='center')
tree_view.column('noverl_url',width=400,anchor='center')
# 设置列名标题
tree_view.heading('num',text='序号')
tree_view.heading('writer',text='作者')
tree_view.heading('name',text='书名')
tree_view.heading('noverl_url',text='书url')
tree_view.pack(side=tk.LEFT,fill=tk.BOTH,expand=1)

# 展示界面 
root.mainloop()