# 在进行评论时 发现其下拉滚动视频 保留前现后三条 注意这点即可
import re
import os
import json
import tkinter as tk
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

def sent_comment():
  key_word = name_va.get()
  comment_content = comment_va.get()
  page.get(f'https://www.douyin.com/search/{key_word}?type=video')
  # 设置cookies
  full_path = os.path.join(current_path, 'douyin_cookies.json')
  with open(full_path, 'r', encoding='utf-8') as f:
    data_array = json.load(f)
  page.set.cookies(data_array)
  # 等待
  page.wait(30)
  page.ele('x://*[@id="douyin-header"]/div[1]/header/div/div/div[1]/div/div[2]/div/div/input').clear()
  page.actions.click('x://*[@id="douyin-header"]/div[1]/header/div/div/div[1]/div/div[2]/div/div/input').input(key_word)

  # 定位点击第一个视频
  page.ele('x://*[@id="search-content-area"]/div/div[1]/div[2]/div[2]/ul/li[1]').click()
  page.wait(3)
  video_div_list = page.eles('x://*[@id="slidelist"]/div[1]/div[1]/div')

  for j in range(len(video_div_list)):
    # 暂停视频
    # ele = page.ele('x://*[@id="sliderVideo"]/div[1]/div[1]/div/div[1]/div[2]/div[6]/div[1]/div[1]/div[1]/div')
    # //*[@id="sliderVideo"]/div[1]/div[1]/div/div[1]/div[1]/div/div/div[2]
    # page.actions.move_to(ele_or_loc=ele).click()
    # page.actions.move_to(ele_or_loc=ele).move(offset_x=-300).click(by_js=True)
    
    # 点击评论按钮
    if j==0:
      page.ele('x://*[@id="sliderVideo"]/div[1]/div[1]/div/div[1]/div[2]/div[3]').click()
      page.wait(3)

    # 点击评论框
    page.ele('x://*[@id="merge-all-comment-container"]/div/div[4]/div[2]/div/div[1]').click()
    page.wait(5)

    # 输入评论内容
    page.ele('x://*[@id="merge-all-comment-container"]/div/div[4]/div[2]/div/div[1]').input(comment_content)
    page.wait(5)

    # 点击发送
    try:
      page.ele('x://*[@id="merge-all-comment-container"]/div/div[4]/div[2]/div/div[2]/div/span[4]').click()
      print(f'{key_word}关键字：第{j+1}个视频评论成功')
    except Exception as e:
      print(e)
      continue

    page.wait(5)
    # 点击到下一个视频 等待加载
    # //*[@id="sliderVideo"]/div[1]/div[1]/div/div[1]/div[1]/div/div/div[2]

    if j==0:
      page.ele('x://*[@id="sliderVideo"]/div[1]/div[1]/div/div[1]/div[1]/div/div/div[2]').click()
    else:
      try:
        video_div_list[j].ele('.xgplayer-playswitch-next').click()
      except Exception as e:
        print(e)
    # page.ele('x://*[@id="sliderVideo"]/div[1]/div[1]/div/div[1]/div[1]/div/div/div[2]').click()

    # page.actions.move_to(ele_or_loc=ele).move(offset_x=-100).scroll(delta_y=150)
    # print(page.tab_ids)
    page.wait(5)

  tkinter.messagebox.showinfo("提示：","发送完成！")

# 创建页面
root = tk.Tk()
# 设置标题
root.title("抖音评论发送器")
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

comment_va = tk.StringVar()
# 设置文本
tk.Label(search_frame, text="评论内容：",font=('微软雅黑',10)).pack(side=tk.LEFT,padx=10)
# 设置输入框
tk.Entry(search_frame, relief=tk.FLAT, textvariable=comment_va,font=('微软雅黑',10), width=30).pack(side=tk.LEFT,padx=10)

# 设置按钮域
button_frame = tk.Frame(root)
button_frame.pack(pady=20)

# 设置搜索按钮
tk.Button(button_frame, text="开始发送评论", relief=tk.FLAT, bg='#88e2d6',font=('微软雅黑',10), width=10, command=sent_comment).pack(side=tk.LEFT,padx=10)

# 展示界面
root.mainloop()