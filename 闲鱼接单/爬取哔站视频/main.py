# 2024.8.16 功能优化第一版 其中还有多余语句 
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
from my_selenium_utils import search_and_download_bilibili_video

def search_content():
  # 只能下载一个视频 下载后如果再次点击搜索内容就会爆目标计算机积极拒绝  不下载没事  
  # 已解决 睡醒找到bug，关闭了driver链接

  search_and_download_bilibili_video.pre()
  # 获取用户输入
  keyword = name_va.get()
  search_and_download_bilibili_video.search_video(keyword)

  search_result = search_and_download_bilibili_video.search_result_list

  if len(search_result) == 0:
    tkinter.messagebox.showwarning("警告：","没有找到相关内容！")
    return
  
  # 清空之前内容
  for i in tree_view.get_children():
    tree_view.delete(i)

  # 将搜索结果添加进treeview
  for i in range(len(search_result['title'])):
    tree_view.insert('', 'end', values=(i+1,search_result['title'][i],search_result['url'][i]))

def query_video():
  # 选择视频
  keyword = name_va.get()
  num = num_va.get()
  src = src_va.get()
  if num=='':
    tkinter.messagebox.showwarning("警告：","请输入要下载的视频序号！从1到100！")
  if keyword == search_and_download_bilibili_video.global_keyword:
    print('搜索页面未变')
  else:
    print('搜索页面变更')

  # 选择视频
  search_and_download_bilibili_video.get_need_search_result(num,src)

def download_video():
  # 获取视频信息 开始下载mp4 mp3
  src = src_va.get()
  # 下载
  search_and_download_bilibili_video.action_download(src)

  # 合并视频和音频
  error_session = search_and_download_bilibili_video.merge_video_audio()
  # 关闭浏览器
  # 注意！重复使用不能关闭连接！
  # search_and_download_bilibili_video.close_driver()
  tkinter.messagebox.showinfo(f"提示：,{error_session}")

def clear():
# 清空之前的搜索结果
  for i in tree_view.get_children():
    tree_view.delete(i)

# 创建页面
root = tk.Tk()
# 设置标题
root.title("哔站视频下载器")
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

# 获取序号
src_va = tk.StringVar()

# 要下载的链接
src_frame = tk.Frame(root)
src_frame.pack(pady=20)
# 设置文本
tk.Label(src_frame, text="要下载的链接：",font=('微软雅黑',10)).pack(side=tk.LEFT,padx=10)
# 设置输入框
tk.Entry(src_frame,relief=tk.FLAT, textvariable=src_va,font=('微软雅黑',10), width=30).pack(side=tk.LEFT,padx=10)

# 设置按钮域
button_frame = tk.Frame(root)
button_frame.pack(pady=20)

# 设置搜索按钮
tk.Button(button_frame, text="搜索内容", relief=tk.FLAT, bg='#88e2d6',font=('微软雅黑',10), width=10, command=search_content).pack(side=tk.LEFT,padx=10)

# 设置查询答案按钮
tk.Button(button_frame, text="选择视频", relief=tk.FLAT, bg='#88e2d6',font=('微软雅黑',10), width=10, command=query_video).pack(side=tk.LEFT,padx=10)

# 设置下载按钮
tk.Button(button_frame, text="下载视频", relief=tk.FLAT, bg='#88e2d6',font=('微软雅黑',10), width=10, command=download_video).pack(side=tk.LEFT,padx=10)

# 设置清空按钮
tk.Button(button_frame, text="清空内容", relief=tk.FLAT, bg='#88e2d6',font=('微软雅黑',10), width=10, command=clear).pack(side=tk.LEFT,padx=10)

# 设置标签名和中文显示内容
column = ('num','question_name','question_url','question_answer_author','question_content')
column_value = ('序号：','视频名称：','视频链接：')
tree_view = ttk.Treeview(root, height=18, columns=column, show='headings')

# 设置列名
tree_view.column('num',width=50,anchor='center')
tree_view.column('question_name',width=50,anchor='center')
tree_view.column('question_url',width=50,anchor='center')

# 设置列名标题
tree_view.heading('num',text='序号：')
tree_view.heading('question_name',text='视频名称：')
tree_view.heading('question_url',text='视频链接：')

tree_view.pack(side=tk.LEFT,fill=tk.BOTH,expand=1)

# 展示界面
root.mainloop()