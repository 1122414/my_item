import os
import csv
import time
import random
import pymysql

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains

# Chrome测试版的路径
chrome_testing_path = r"D:\chrome-win64\chrome.exe"
# Chromedriver的路径
chromedriver_path = r"C:\Users\Lenovo\AppData\Local\Programs\Python\Python311\chromedriver.exe"
# 打开浏览器 使之在后台运行
os.chdir(r"D:\chrome-win64")
os.popen(r'start chrome.exe --remote-debugging-port=9527 --user-data-dir="E:\selenium')
# 设置Chrome选项
options = webdriver.ChromeOptions()
options.binary_location = chrome_testing_path
options.add_experimental_option("debuggerAddress", "127.0.0.1:9527")
# 设置WebDriver服务
service = Service(chromedriver_path)
# 创建Chrome WebDriver实例
driver = webdriver.Chrome(service=service, options=options)
# 路径
current_path = os.path.dirname(__file__)
# print(current_path)
# full_path = os.path.join(current_path+'/知乎', 'search_input.txt')
# print(current_path)
# print(full_path)
# 连接数据库
conn = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    password='3306',
    database='python_spider',
    charset='utf8',
)
cur = conn.cursor()
search_content_global = ''
# 注意！此处要先关闭所有的chrome进程，否则无效
# 访问知乎首页
driver.get("https://www.zhihu.com/")

question_list = {}
question_name_global = ''
question_url_global = ''

def login():
  '''
    登录
  '''
  # 需要登录
  try:
    phone_num = input("请输入手机号：")
    driver.find_element(By.XPATH,'//*[@id="root"]/div/main/div/div/div/div/div[2]/div/div[1]/div/div[1]/form/div[2]/div[2]/label/input').send_keys(phone_num)

    # 点击获取验证码 此处可能需要滑动验证码 未写
    driver.find_element(By.XPATH,'//*[@id="root"]/div/main/div/div/div/div/div[2]/div/div[1]/div/div[1]/form/div[3]/button').click()

    code = input("请输入验证码：")
    driver.find_element(By.XPATH,'//*[@id="root"]/div/main/div/div/div/div/div[2]/div/div[1]/div/div[1]/form/div[3]/div/label/input').send_keys(code)

    # 登录
    driver.find_element(By.XPATH,'//*[@id="root"]/div/main/div/div/div/div/div[2]/div/div[1]/div/div[1]/form/button').click()
  except:
    print("已登录！")

def search(search_content):
  '''
    搜索
  '''
  # 输入搜索关键字
  # search_input = input("请输入搜索关键字：")
  global search_content_global
  search_content_global = search_content
  search_input = search_content
  driver.find_element(By.XPATH,'//*[@id="Popover1-toggle"]').click()
  driver.find_element(By.XPATH,'//*[@id="Popover1-toggle"]').send_keys(search_input)
  full_path = os.path.join(current_path + '/知乎', search_input)
  print(full_path)
  if not os.path.exists(full_path):
    os.mkdir(full_path)
  # 点击搜索按钮
  driver.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/header/div[1]/div[1]/div/form/div/div/label/button').click()
  time.sleep(random.uniform(2, 3))

def parse_search_page():
  '''
    解析搜索页面
  '''
  question_list['question_name'] = []
  question_list['question_url'] = []
  for i in range(3):
    # 往下滑动
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(random.uniform(2, 3))
    driver.execute_script("window.scrollTo(window.scrollBy(0,-50));")

  time.sleep(random.uniform(2, 3))
  # 获取问题名称
  question_name_list = driver.find_elements(By.XPATH,'//div[@itemprop="zhihu:question"]//span[@class="Highlight"]')
  question_url_list = driver.find_elements(By.XPATH,'//div[@itemprop="zhihu:question"]//a')
  for i in range(len(question_name_list)):
    question_list['question_name'].append(str(i+1)+'_'+question_name_list[i].text)
    question_list['question_url'].append(question_url_list[i].get_attribute("href"))
  for i in range(len(question_list['question_name'])):
    print(question_list['question_name'][i],'\n',question_list['question_url'][i]) 

def select_and_parse_question(num):
  '''
    选择问题
  '''
  question_list['question_answer_author'] = []
  question_list['question_answer_content'] = []
  
  # question_id = int(input("\n请输入问题ID （从1开始）："))
  question_id = int(num)
  # print(question_list['question_name'])
  # select_name =  question_list['question_name'][question_id].split('_')[1]

  # 全局选择问题名
  global question_name_global
  temp_question_name = question_list['question_name'][question_id-1]
  # question_name = ''
  # 防止建立文件夹时有非法字符
  flag = False
  for i in temp_question_name:
    if i == '<' or i=='>' or i==':' or i=='/' or i=='\'' or i=='|' or i=='*' or i == '?':
      flag = True
      if i == '?':
        question_name = temp_question_name.replace(i,'？')
      else:
        question_name = temp_question_name.replace(i,'')
  if not flag:
    question_name = temp_question_name

  question_name_global = question_name
  print("选择问题是：",question_name,'\n')
  global search_content_global

  # 建立知乎/搜索的问题
  full_path = os.path.join(current_path + '\知乎',search_content_global, question_name)
  print('43行的full_path是：',full_path)

  if not os.path.exists(full_path):
    os.mkdir(full_path)

  # 全局选择链接
  global question_url_global
  question_url = question_list['question_url'][question_id-1]
  question_url_global = question_url

  select_url = question_url[question_url.index('question'):]
  # 定位并点击链接
  element = driver.find_element(By.XPATH,f'//a[@href="/{select_url}"]')
  ActionChains(driver).move_to_element(element).click(element).perform()

  # 等待页面加载完毕
  # uniform 生成下一个实数，范围在2到3之间
  time.sleep(random.uniform(2, 3))
  # # 还是停留在点击搜索页面？ 找到问题所在 selenium点击链接打开新的页面,但是driver指向还是原来的页面
  # full_path = os.path.join(current_path, 'zhihu.html')
  # with open(full_path, 'w', encoding='utf-8') as f:
  #   f.write(driver.page_source)

  # driver当前聚焦的window
  current_window = driver.current_window_handle
  # print(current_window)
  # 指向最新打开的窗口 driver.window_handles获取当前全部窗口
  driver.switch_to.window(driver.window_handles[-1])
  current_window = driver.current_window_handle
  # print(current_window)

  # 点击显示更多
  try:
    driver.find_element(By.XPATH,'//*[@id="root"]/div/main/div/div/div[1]/div[2]/div/div[1]/div[1]/div[6]/div/div/div/button').click
  except:
    print("未发现显示更多按钮")

  # https://www.zhihu.com/question/617195799/answer/3168488571
  driver.find_element(By.XPATH, '//*[@id="root"]/div/main/div/div/div[3]/div[1]/div/div[1]/a').click()

  '''
  try:
    # 在frame内
    # QuestionMainAction ViewAll-QuestionMainAction
    # element = driver.find_elements(By.CLASS_NAME,'QuestionMainAction ViewAll-QuestionMainAction')
    # ActionChains(driver).move_to_element(element[0]).click(element[0]).perform()
    driver.find_element(By.XPATH, '//*[@id="root"]/div/main/div/div/div[3]/div[1]/div/div[1]/a').click()
    print("点击加载更多按钮")
  except:
    print("未发现加载更多按钮")
  '''
  for i in range(3):
    # 往下滑动 +50让它一定到底刷新
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(random.uniform(2, 3))
    # 往上滑动一小段 不然会卡住
    driver.execute_script("window.scrollTo(window.scrollBy(0,-50));")
  time.sleep(random.uniform(2, 3))
  #   time.sleep(random.uniform(2, 3))
  
  # 获取回答作者和内容
  author_name_list = driver.find_elements(By.XPATH,'//span[@class="UserLink AuthorInfo-name"]')
  answer_content_list = driver.find_elements(By.XPATH,'//div[@class="css-376mun"]/span')
  for i in range(len(author_name_list)):
    # 打印结果
    author_name = author_name_list[i].text
    answer_content = answer_content_list[i].text
    # print("\n此回答作者是：",author_name,"\n内容是：\n",answer_content)
    question_list['question_answer_author'].append(author_name)
    question_list['question_answer_content'].append(answer_content)
  # print(question_list)

def download_zhihu_content():
  # 保存到数据库
  for i in range(len(question_list['question_answer_author'])):
    cur.execute('insert into zhihu_question(question_name,question_url,question_answer_author,question_answer_content) values(%s,%s,%s,%s)', (question_name_global,question_url_global,question_list['question_answer_author'][i],question_list['question_answer_content'][i]))
  conn.commit()
  print("\n数据库保存成功！")

  # 保存到csv 目前状态是 建立一个问题名字的文件夹 然后把回答一股脑写进一个csv文件 并没有分开给回答建立单独文件
  full_path = os.path.join(current_path+'/知乎',search_content_global, question_name_global,question_name_global+'.csv')
  with open(full_path, 'w', encoding='utf-8',newline='') as f:
    writer = csv.DictWriter(f, fieldnames=question_list.keys())
    writer.writeheader()
    dict_data = []
    for i in range(len(question_list['question_answer_author'])):
      dict_data.append({'question_name':question_name_global, 'question_url':question_url_global, 'question_answer_author':question_list['question_answer_author'][i], 'question_answer_content':question_list['question_answer_content'][i]})

    for row in dict_data:
        writer.writerow(row)
  print("\ncsv保存成功！")

# for i in range(len(question_name_list)):
#   # 打印结果
#   question_name = question_name_list[i].text
#   question_url = question_url_list[i].get_attribute("href")
#   print(question_name,question_url)

#   # 有时候没有结果？不知道什么情况  答：未加载完成 需等
#   cur.execute('insert into zhihu(question_name,question_url) values(%s,%s)', (question_name,question_url)) 
#   conn.commit()

if __name__ == '__main__':
  # login()
  search('网安')
  parse_search_page()
  select_and_parse_question(12)

  cur.close()
  conn.close()
  print('解析结束！')
  input("\n请等待搜索结果加载完毕，按任意键继续...")