import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

# 实例化浏览器对象
driver = webdriver.Chrome()
driver.get('https://www.bg60.cc/')
dict_name = {}
current_path = os.path.dirname(__file__)
# 小说名称
book_id = 0
book_title_w = ''
# 小说搜索结果
search_dict = {}
# 访问网址
def search_book(novel_name):
    '''
      搜索小说
    '''
    # 清空search_dict
    search_dict['book_name'] = []
    search_dict['book_author'] = []
    search_dict['book_intro'] = []
    search_dict['book_url'] = []
    # 点击搜索框
    driver.find_element(By.XPATH,'/html/body/div[4]/div[1]/div[2]/form/input[1]').click()
    # 输入小说名称
    # book_name = input('请输入小说名称：')
    book_name = novel_name
    driver.find_element(By.XPATH,'/html/body/div[4]/div[1]/div[2]/form/input[1]').send_keys(book_name)
    # 点击搜索按钮
    driver.find_element(By.XPATH,'/html/body/div[4]/div[1]/div[2]/form/input[2]').click()
    # 跳转页面 等待加载
    sleep(3)
    # now_url = 'https://www.bg60.cc/s?q='+book_name
    # print(now_url)
    # driver.get(now_url)
    # print(driver)
    # 获取搜索结果
    # 搜索结果的小说名称
    search_book_name_list = driver.find_elements(By.XPATH,'//div[@class="bookbox"]//h4/a')
    # 每一条的作者
    search_book_author_list = driver.find_elements(By.XPATH,'//div[@class="bookbox"]//div[@class="author"]')
    # 每一条的简介
    search_book_intro_list = driver.find_elements(By.XPATH,'//div[@class="bookbox"]//div[@class="uptime"]')
    # 每一条的url
    search_book_url_list = driver.find_elements(By.XPATH,'//div[@class="bookbox"]//h4/a')
    # 将数据添加进字典
    for i in range(len(search_book_name_list)):
      search_dict['book_name'].append(search_book_name_list[i].text)
      search_dict['book_author'].append(search_book_author_list[i].text)
      search_dict['book_intro'].append(search_book_intro_list[i].text)
      search_dict['book_url'].append(search_book_url_list[i].get_attribute("href"))
      # print(search_dict['book_name'][i],'-----',search_dict['book_author'][i],'\n',search_dict['book_intro'][i],'\n',search_dict['book_url'][i])
    # 打印搜索结果
    # print(search_dict)

def find_name(book_num):
    '''
      获取小说名称 作者 章节名称
    '''
    # 输入要下载的小说编号
    # book_num = int(input('请输入要下载的小说编号，编号从1开始，且小于100：'))
    # if book_num > 100 or book_num < 1:
    #     print('编号输入错误，请重新输入！')
    #     return
    # 访问网址 
    url = search_dict['book_url'][int(book_num)-1]
    global book_id
    book_id = url.split('/')[-2]
    driver.get(url)
    book_title = driver.find_elements(By.XPATH,'//div[@class="info"]/h1')
    global book_title_w 
    book_title_w = book_title[0].text
    # 创建小说名称文件夹
    full_path = os.path.join(current_path+'/小说',book_title_w)
    if not os.path.exists(os.path.join(full_path)):
        os.mkdir(os.path.join(full_path))

    book_author = driver.find_elements(By.XPATH,'//div[@class="info"]/div[@class="small"]/span[1]')

    book_chapter_head = driver.find_elements(By.XPATH,'//div[@class="listmain"]/dl//dd/a')

    dict_name['book_title'] = book_title[0].text
    dict_name['book_author'] = book_author[0].text
    dict_name['book_chapter_head'] = []
    for i in range(len(book_chapter_head)):
        dict_name['book_chapter_head'].append(book_chapter_head[i].text)

def download_chapter(i,chapter_name):
    '''
      下载章节
    '''
    global book_id
    # 点击章节
    driver.find_element(By.XPATH,'//a[@href="/book/'+book_id+'/'+str(i)+'.html"]').click()
    # 等待章节加载完成
    sleep(1)
    # 章节内容
    chapter_content = driver.find_element(By.XPATH,'//div[@id="chaptercontent"]').text
    # 保存章节内容
    full_path = os.path.join(current_path+'\小说',book_title_w,chapter_name+'.txt')
    # print(full_path)
    with open(full_path,'w',encoding='utf-8') as f:
        f.write(chapter_content)
    # print(chapter_content)
    # 回退
    driver.back()
    sleep(1)

# book_name = input('请输入小说名称：')
if __name__ == '__main__':
  search_book()
  find_name()

  input()

  # print(current_path)
