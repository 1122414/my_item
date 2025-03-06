import sys
from os import path
import tkinter as tk
import tkinter.messagebox
from time import sleep
from tkinter import ttk
d = path.dirname(__file__)  # 获取当前路径
parent_path = path.dirname(d)  # 获取上一级路径
sys.path.append(parent_path)    # 如果要导入到包在上一级
# print(path.dirname(__file__))
from my_selenium_utils import zhihu_content

def search_zhihu():
  # 打印搜索内容
  search_content = name_va.get()
  zhihu_content.search(search_content)
  zhihu_content.parse_search_page()
  search_result = zhihu_content.question_list

  if len(search_result) == 0:
    tkinter.messagebox.showwarning("警告：","没有找到相关内容！")
    return
  
  # 清空之前内容
  for i in tree_view.get_children():
    tree_view.delete(i)

  # 将搜索结果添加进treeview
  for i in range(len(search_result['question_name'])):
    tree_view.insert('', 'end', values=(i+1,search_result['question_name'][i],search_result['question_url'][i]))

def query_zhihu():
  # 选择问题，并给出问题答案
  num = num_va.get()
  if num=='':
    tkinter.messagebox.showwarning("警告：","请输入要下载的答案序号！从1到100！")

  zhihu_content.select_and_parse_question(num)
  search_result = zhihu_content.question_list

  # 清空之前内容
  for i in tree_view.get_children():
    tree_view.delete(i)
  # 将搜索结果添加进treeview
    
  for i in range(len(search_result['question_answer_author'])):
    tree_view.insert('', 'end', values=(i+1,zhihu_content.question_name_global,zhihu_content.question_url_global,search_result['question_answer_author'][i],search_result['question_answer_content'][i]))

def download_zhihu():
  zhihu_content.download_zhihu_content()
  tkinter.messagebox.showinfo("提示：","下载完成！")


def clear():
# 清空之前的搜索结果
  for i in tree_view.get_children():
    tree_view.delete(i)

# 创建页面
root = tk.Tk()
# 设置标题
root.title("知乎问答爬取器")
# 设置窗口大小
root.geometry("1200x800")
# 设置标签
search_frame = tk.Frame(root)
search_frame.pack(pady=20)
# 设置可变变量
name_va = tk.StringVar()
# 设置文本
tk.Label(search_frame, text="要搜索的内容：",font=('微软雅黑',10)).pack(side=tk.LEFT,padx=10)
# 设置输入框
tk.Entry(search_frame, relief=tk.FLAT, textvariable=name_va,font=('微软雅黑',10), width=30).pack(side=tk.LEFT,padx=10)

# 获取序号
num_va = tk.StringVar()

# 查询下载输入框
download_frame = tk.Frame(root)
download_frame.pack(pady=20)
# 设置文本
tk.Label(download_frame, text="要下载的序号：",font=('微软雅黑',10)).pack(side=tk.LEFT,padx=10)
# 设置输入框
tk.Entry(download_frame,relief=tk.FLAT, textvariable=num_va,font=('微软雅黑',10), width=30).pack(side=tk.LEFT,padx=10)

# 设置按钮域
button_frame = tk.Frame(root)
button_frame.pack(pady=20)

# 设置搜索按钮
tk.Button(button_frame, text="搜索问题", relief=tk.FLAT, bg='#88e2d6',font=('微软雅黑',10), width=10, command=search_zhihu).pack(side=tk.LEFT,padx=10)

# 设置查询答案按钮
tk.Button(button_frame, text="查询答案", relief=tk.FLAT, bg='#88e2d6',font=('微软雅黑',10), width=10, command=query_zhihu).pack(side=tk.LEFT,padx=10)

# 设置下载按钮
tk.Button(button_frame, text="下载答案", relief=tk.FLAT, bg='#88e2d6',font=('微软雅黑',10), width=10, command=download_zhihu).pack(side=tk.LEFT,padx=10)

# 设置清空按钮
tk.Button(button_frame, text="清空内容", relief=tk.FLAT, bg='#88e2d6',font=('微软雅黑',10), width=10, command=clear).pack(side=tk.LEFT,padx=10)

# 设置标签名和中文显示内容
column = ('num','question_name','question_url','question_answer_author','question_content')
column_value = ('序号：','问题名称：','问题链接：','问题答者：','回答内容：')
tree_view = ttk.Treeview(root, height=18, columns=column, show='headings')

# 设置列名
tree_view.column('num',width=50,anchor='center')
tree_view.column('question_name',width=50,anchor='center')
tree_view.column('question_url',width=50,anchor='center')
tree_view.column('question_answer_author',width=50,anchor='center')
tree_view.column('question_content',width=50,anchor='center')

# 设置列名标题
tree_view.heading('num',text='序号：')
tree_view.heading('question_name',text='问题名称：')
tree_view.heading('question_url',text='问题链接：')
tree_view.heading('question_answer_author',text='问题答者：')
tree_view.heading('question_content',text='回答内容：')
tree_view.pack(side=tk.LEFT,fill=tk.BOTH,expand=1)

# 展示界面
root.mainloop()