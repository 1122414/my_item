# 深度优先  而不是广度优先
# 功能以函数方式集合在main中

# 不是哥们  这里为什么直接运行会在打开一个空白浏览器，但是一步步调试不会
# 分文件写着六个模块  Hack Social Tech Market Money VIP

# 目前数据第31页 2024.10.21 10.40
# 准备2024.10.21写个日志文件、存入一些信息  √  注：日志只记录了 何时403、何时爬取何帖、何页面  再记录下退出时有多少条数据
# 2024.10.24  如果遇到403错误 等待30分钟 重启浏览器
import os
import re
import json
import time
import pymysql
import subprocess
from DrissionPage.common import By
from DrissionPage import ChromiumPage,ChromiumOptions

WAIT_TIME = 5

# 链接数据库
conn = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='3306',
            database='torbot',
            # charset='utf-8',  内容中有表情得用utf8mb4
            charset='utf8mb4',
        )
cursor = conn.cursor()
#region Description 折叠注释 初始工作
# 记录数据条数
query = "SELECT COUNT(*) FROM Hack_forum_ultimate"
cursor.execute(query)
now_data_num = cursor.fetchone()[0]

data_num = int(now_data_num + 1)
# 403判断
is_FZT = False
#定义单条json数据
useful_data = {}
useful_data['module'] = ''
useful_data['forum_thead'] = ''
useful_data['forum_thead_url'] = ''
useful_data['forum'] = ''
useful_data['forum_url'] = ''
useful_data['forum_threads'] = ''
useful_data['forum_posts'] = ''
useful_data['forum_last_post_thread'] = ''
useful_data['forum_last_post_time']=''
useful_data['forum_last_post_user']=''
useful_data['thread']=''
useful_data['thread_url']=''
useful_data['thread_user_name']=''
useful_data['thread_replies']=''
useful_data['thread_view']=''
useful_data['thread_last_post_time']=''
useful_data['thread_last_post_user']=''
useful_data['post_id']=''
useful_data['user_url']=''
useful_data['user_name']=''
# useful_data['user_last_seen']=''
# useful_data['user_join_date']=''
useful_data['user_popularity']=''
useful_data['user_credibility']=''
# useful_data['user_contracts_completed']=''
# useful_data['user_open_disputes']=''
useful_data['user_bytes']=''
useful_data['user_threads']=''
useful_data['user_posts']=''
# useful_data['user_quick_loves']=''
# useful_data['user_time_online']=''
useful_data['user_game_xp']=''
useful_data['user_post_content']=''


# 获取当前路径
current_path = os.path.dirname(__file__)

# 创建日志文件夹
now_day = time.strftime('%Y-%m-%d', time.localtime())
log_path = os.path.join(current_path, 'log')
if not os.path.exists(log_path):
    os.makedirs(log_path)
# 日志文件名
log_file_name = os.path.join(log_path, f'{now_day}.log')
# 日志文件
with open(log_file_name, 'a', encoding='utf-8') as f:
  f.write(f'------------------------------\n{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())} 开始运行\n------------------------------\n')

# 命令行打开目标Chrome浏览器
subprocess.Popen('"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9527 --user-data-dir="E:\selenium\AutomationProfile"')

co = ChromiumOptions()
co.set_local_port(9527)
# co.headless()
page = ChromiumPage(addr_or_opts=co)
#endregion

#region Description 函数模块
# 正则匹配数字
def extract_numbers(s):
    return [int(num) for num in re.findall(r'\d+', s)]
def get_page_number():
  '''
  自动获取上一次正常运行时的页数
  注意：需有一个log：格式为目前是第xxx页的第xxx个帖子
  '''
  # 每天第一次运行把之前的最后一条数据放进去
  # 从哪一页退出从哪一页进  设置初始页数
  # region Description 从log里自动读取上次退出的页数

  def open_and_read_log():
    aim_log = ''
    for i in range(len(log_lsit)-1,0,-1):
      now_path = os.path.join(log_path, log_lsit[i])
      with open(now_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
      for i in reversed(lines):
        if "目前是第" in i:
          aim_log = i.split(' ')
          return aim_log
    aim_log = 0
  log_lsit = os.listdir(log_path)
  # aim_log_index = get_aim_log_index(log_lsit)
  # aim_log = log_lsit[aim_log_index]
  # aim_log_path = os.path.join(log_path, aim_log)

  aim_log = open_and_read_log()
  # if aim_log == 0:
  #   aim_log = open_and_read_log(aim_log_path)

  numbers = extract_numbers(aim_log[2])
  return numbers
# 通用
def get_data_num():
  query = "SELECT COUNT(*) FROM Hack_forum_ultimate"
  cursor.execute(query)
  return cursor.fetchone()[0]
# 403 错误
def FZTError():
  print('403 Forbidden！')
  with open(log_file_name, 'a', encoding='utf-8') as f:
    f.write(f'!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}: 403 Forbidden！----------目前已有{get_data_num()}条数据\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n')
  # 关闭所有标签页  退出浏览器
  tab = page.tab_ids
  page.close_tabs(tabs_or_ids = tab)
  is_FZT = True
  return is_FZT

def get_forum_skin_data(tbody_tr_list):
  # 注：此处tbody的第二个tr开始才是论坛内容，第一个是表头
  try:
    for i in range(1,len(tbody_tr_list)):
      td_list = tbody_tr_list[i].eles('x:.//td')
      useful_data['forum'] = td_list[1].ele('x:.//div[@class="td-foat-left mobile-link"]/strong/a').text
      useful_data['forum_url'] = td_list[1].ele('x:.//div[@class="td-foat-left mobile-link"]/strong/a').attr('href')
      
      useful_data['forum_threads'] = td_list[2].text
      useful_data['forum_posts'] = td_list[3].text
      
      useful_data['forum_last_post_thread'] = td_list[4].ele('x:.//a[1]').text
      useful_data['forum_last_post_time'] = td_list[4].ele('x:.//span[@class="smart-time"]').attr('title')
      useful_data['forum_last_post_user'] = td_list[4].ele('x:.//a[2]/span').text
  except Exception as e:
    print(e,'150行')

def get_post_per_page(start_thread):
  try:
    # 打印目前是第几页
    # x://*[@id="content"]/div/div[4]/div/span[@class="pagination_current"]
    now_page = page.ele('x://*[@id="content"]/div/div[5]/div/span').text
    print(f'目前是第{now_page}页')
    
    # 更新forum_url
    useful_data['forum_url'] = page.url
    
    # 出现403 Forbidden！  开摆！   目前没有找到解决Ngnix反爬的方法  2024.10.16
    # 2024.10.20  一直刷新会出现验证页面，但是验证过后还是403，暂时放弃
    # region Description  403 Forbidden 2024.10.20 暂时放弃
    # while 1:
    #   if page.ele('text=403 Forbidden'):
    #     print('403 Forbidden！')
    #     page.refresh()
    #     page.wait(5)
    #   else:
    #     break
    # endregion

    if page.ele('text=403 Forbidden'):
      FZTError()
      return

    global data_num
    # region Description点击want_page次下一页  即让他从什么地方开始  当然也可以直接get请求网页  此处按需更改
    # want_page = 3
    # page.get(f'https://hackforums.net/forumdisplay.php?fid=2&page={want_page}')
    # for i in range(0,want_page):
    #   if page.ele('text=Next »'):
    #     page.ele('text=Next »').click(by_js=False)
    #   else:
    #     break
    #   except Exception as e:
    #     print(e,"最后一页！")
    # endregion
    
    # 获取每页全部帖子
    thread_list = page.eles('x://*[@id="content"]/div/table[2]/tbody/tr[@class="inline_row"]')
    # 此处可更改从第几个帖子开始  可能前面帖子拿过了
    # 在函数外设值一个变量  start_thread ，开始是设值数字  后面结束此页之后要归零 只有第一次进入需要使用此变量
    # for i in range(start_thread,len(thread_list)) 
    for i in range(start_thread,len(thread_list)):
      # 打印是第几页的第几个帖子
      # print(f'目前是第{now_page}页的第{i+1}个帖子')
      
      # 存入日志文件
      with open(log_file_name, 'a', encoding='utf-8') as f:
        f.write(f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}: 目前是第{now_page}页的第{i+1}个帖子\n')
      
      # region Description  403 Forbidden 2024.10.20 暂时放弃
      # 403就不停刷新
      # while 1:
      #   if page.ele('text=403 Forbidden'):
      #     print('403 Forbidden！')
      #     page.refresh()
      #     page.wait(5)
      #   else:
      #     break
      # endregion

      if page.ele('text=403 Forbidden'):
        FZTError()
        return

      try:
        thread_list = page.eles('x://*[@id="content"]/div/table[2]/tbody/tr[@class="inline_row"]')
        try:
          useful_data['thread'] = thread_list[i].ele('x:.//div[@class="mobile-link-truncate"]/span').text
        except Exception as e:
          useful_data['thread'] = ''
        # 拼接
        try:
          useful_data['thread_url'] = 'https://hackforums.net/' + thread_list[i].ele('x:.//div[@class="mobile-link-truncate"]//a').attr('href')
        except Exception as e:
          useful_data['thread_url'] = ''

        try:
          useful_data['thread_user_name'] = thread_list[i].ele('x:.//div[@class="author largetext"]/a/span').text
        except Exception as e:
          useful_data['thread_user_name'] = ''
          
        try:
          useful_data['thread_replies'] = thread_list[i].ele('x:.//td[3]/a').text
        except Exception as e:
          useful_data['thread_replies'] = ''
          
        try:
          useful_data['thread_view'] = thread_list[i].ele('x:.//td[4]/span[@class="mobile-hide"]').text
        except Exception as e:
          useful_data['thread_view'] = ''
          
        try:
          useful_data['thread_last_post_time'] = thread_list[i].ele('x:.//span[@class="smart-time"]').attr('title')
        except Exception as e:
          useful_data['thread_last_post_time'] = thread_list[i].ele('x:.//span[@class="lastpost smalltext"]').text
        # try:
        try:
          useful_data['thread_last_post_user'] = thread_list[i].ele('x:.//div[@class="mobile-link last-poster mobile-remove"]//span').text
        except Exception as e:
          useful_data['thread_last_post_user'] = ''
        # except Exception as e:
        #   useful_data['thread_last_post_user'] = thread_list[i].ele('x:.//div[@class="mobile-link last-poster mobile-remove"]/a[2]').text
      except Exception as e:
        print(e,"获取帖子相关信息时出现错误！167行")
      # 点击进入帖子
      try:
        thread_list[i].ele('x:.//div[@class="mobile-link-truncate"]//a').click() 
        page.wait(WAIT_TIME)
      except Exception as e:
        print(e,'进入帖子失败！173行')
        # 失败则进入下一个帖子
        continue

      # 获取全部帖子信息
      # 先获取帖子有几页回复
      try:
        try:
          page.ele('x://div[@class="pagination"]')
          page_num = int(page.eles('x://*[@id="content"]/div/div[4]/div/a')[-2].text)
        except Exception as e:
          page_num = 1
        
        # 循环获取该帖子内每一页回复
        # 计时开始，超过25分钟就强制退出到post页面
        start_time = time.time()
        while 1:
          if page.ele('text=403 Forbidden'):
            FZTError()
            return 
          posts = page.ele('#posts')
          post_list = posts.eles('x:.//div[@class="post classic  clear"]')
          
          # 获取回复人信息和回复内容
          for i in range(len(post_list)):
            # 获取帖子id
            try:
              useful_data['post_id'] = post_list[i].attr('id')
            except Exception as e:
              useful_data['post_id'] = 000000
            try:
              useful_data['user_url'] = post_list[i].ele('x:.//div[@class="post_author scaleimages"]//div[@class="author_information"]//span/a').attr('href')
            except Exception as e:
              useful_data['user_url'] = ''
            try:
              useful_data['user_name'] = post_list[i].ele('x:.//div[@class="post_author scaleimages"]//div[@class="author_information"]//span//a').text
            except Exception as e:
              useful_data['user_name'] = ''
            
            # 获取用户信息，直接在posts页面就能拿到一些
            # 注意：此处用户信息可能会有少量错误 不再修改
            user_data_lists = post_list[i].eles('x:.//div[@class="author_statistics"]/div[@class="author_wrapper"]/div[@class="author_row"]')
            try:
              useful_data['user_posts']=user_data_lists[0].text
            except Exception as e:
              useful_data['user_posts']=''
            try:
              useful_data['user_threads']=user_data_lists[1].text
            except Exception as e:
              useful_data['user_threads']=''
            try:
              useful_data['user_credibility']=user_data_lists[2].text
            except Exception as e:
              useful_data['user_credibility']=''
            try:
              useful_data['user_popularity']=user_data_lists[3].text
            except Exception as e:
              useful_data['user_popularity']=''
            try:
              useful_data['user_bytes']=user_data_lists[4].text
            except Exception as e:
              useful_data['user_bytes']=''
            try:
              useful_data['user_game_xp']=user_data_lists[5].text
            except Exception as e:
              useful_data['user_game_xp']=''
            #region Description  考虑到进退网页时间成本等，目前这块不需要
            # # 进入用户主页
            # useful_data['user_url'] = post_list[i].ele('x:.//div[@class="post_author scaleimages"]//div[@class="author_information"]//span/a').click()
            # page.wait(3)

            # try:
            #   # 进主页抓取用户信息
            #   # useful_data['user_last_seen'] = post_list[i].ele('x:.//div[@class="author largetext"]/span[2]').text
            #   pro_adv_content_info = page.ele('x://div[@class="pro-adv-content-info"]')
            #   info_list = pro_adv_content_info.eles('x:.//div[@class="pro-adv-card"]/div')
              
            #   # 直接拿到全部文字信息
            #   useful_data['user_join_date'] = info_list[5].text
            #   useful_data['user_popularity'] = info_list[6].text
            #   useful_data['user_credibility'] = info_list[7].text
            #   useful_data['user_contracts_completed'] = info_list[8].text
            #   useful_data['user_open_disputes'] = info_list[9].text
            #   useful_data['user_bytes'] = info_list[10].text
            #   useful_data['user_threads'] = info_list[11].text
            #   useful_data['user_posts'] = info_list[12].text
            #   useful_data['user_quick_loves'] = info_list[13].text
            #   useful_data['user_time_online'] = info_list[14].text
            # except Exception as e:
            #   print(e,"获取用户信息时出现错误！")
            
            # # 返回上一页
            # page.back()
            # page.wait(3)
            #endregion

            # 获取回复信息
            useful_data['user_post_content'] = post_list[i].ele('x:.//div[@class="post_body scaleimages"]').text
            page.wait(WAIT_TIME)
            # 写入数据库
            try:
                sql = "INSERT INTO Hack_forum_ultimate(id,module,forum_thead,forum_thead_url,forum,forum_url,forum_threads,forum_posts,forum_last_post_thread,forum_last_post_time,forum_last_post_user,thread,thread_url,thread_user_name,thread_replies,thread_view,thread_last_post_time,thread_last_post_user,post_id,user_url,user_name,user_popularity,user_credibility,user_bytes,user_threads,user_posts,user_game_xp,user_post_content) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s)"
                val = (data_num,useful_data['module'],useful_data['forum_thead'],useful_data['forum_thead_url'],useful_data['forum'],useful_data['forum_url'],useful_data['forum_threads'],useful_data['forum_posts'],useful_data['forum_last_post_thread'],useful_data['forum_last_post_time'],useful_data['forum_last_post_user'],useful_data['thread'],useful_data['thread_url'],useful_data['thread_user_name'],useful_data['thread_replies'],useful_data['thread_view'],useful_data['thread_last_post_time'],useful_data['thread_last_post_user'],useful_data['post_id'],useful_data['user_url'],useful_data['user_name'],useful_data['user_popularity'],useful_data['user_credibility'],useful_data['user_bytes'],useful_data['user_threads'],useful_data['user_posts'],useful_data['user_game_xp'],useful_data['user_post_content'])
                cursor.execute(sql, val)
                conn.commit()
                data_num += 1
            except Exception as e:
                print(f"Error: {e}，277行")
                
          # region Description 点击下一页 
          # 点击下一页 必须点击内容包含next的元素 即最后一个元素(不一定nnd)
          # if num < page_num-1:
          #   try:
          #     # page.ele('x://div[@class="pagination"]')
          #     # page.eles('x://*[@id="content"]/div/div[4]/div/a')[-1].click()
          #     page.ele('text=Next »').click(by_js=False)
          #     page.wait(5)
          #   except Exception as e:
          #     print(e,"点击帖子内posts下一页时出现错误！")
          # endregion
          
          # 翻页准备
          try:
            # 看是否有下一页
            if page.ele('text=Next »'):
              page.ele('text=Next »').click(by_js=False)
            else:
              break
          except Exception as e:
            print(e,"最后一页！299行")
            break
          end_time = time.time()
          run_time = end_time - start_time
          # 强制退出
          if end_time - start_time > 1500:
            break
            
        # 返回post页面
        page.get(useful_data['forum_url'])
        page.wait(WAIT_TIME)
        
      except Exception as e:
        # 返回post页面
        try:
          page.get(useful_data['forum_url'])
        except Exception as e:
          print(e,"返回post页面时出现错误！408行")
        page.wait(WAIT_TIME)
        print(e,"获取帖子相关回复时出现错误！315行")
  except Exception as e:
    print(e,"获取帖子相关回复时出现错误！416行")
  # start_thread = 0
      
def Hack_module():
  try:
    for k in useful_data:
      useful_data[k] = ''
    useful_data['module'] = 'Hack'
    #  tabmenu_1  tabmenu_45
    tabmenu_1 = page.ele('#tabmenu_1')
    useful_data['forum_thead'] = tabmenu_1.ele('x:.//thead//strong/a').text
    useful_data['forum_thead_url'] = tabmenu_1.ele('x:.//thead//strong/a').attr('href')
    tbody_tr_list = tabmenu_1.eles('x:.//tbody//tr')

    get_forum_skin_data(tbody_tr_list)
    # 获取完表面 深入！
    # 点击论坛链接
    page.ele('x://*[@id="cat_1_e"]/tr[2]/td[2]/div[1]/strong/a').click()
    # 等待跳转
    page.wait(WAIT_TIME)
    # 获取论坛内容
  
    # region Description 方法一： 看论坛有多少页
    # try:
    #   page.ele('x://div[@class="pagination"]')
    #   page_num = int(page.eles('x://*[@id="content"]/div/div[4]/div/a')[-3].text)
    # except Exception as e:
    #   page_num = 1
    # for i in range(page_num):
    #   get_post_per_page()
    #   try:
    #     # page.ele('x://div[@class="pagination"]')
    #     # page.eles('x://*[@id="content"]/div/div[4]/div/a')[-3].click()
    #     page.ele('text=Next »').click(by_js=False)
    #     page.wait(5)
    #   except Exception as e:
    #     print(e,"点击论坛下一页帖子时出现错误！")
    # endregion
    
    numbers = get_page_number()
    want_page = int(numbers[0])
    start_thread = int(numbers[1])

    # want_page = 47
    # start_thread = 0
    # endregion
    
    page.get(f'https://hackforums.net/forumdisplay.php?fid=2&page={want_page}')
    with open(log_file_name, 'a', encoding='utf-8') as f:
      f.write(f'在{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}程序开始时刻: 已有{get_data_num()}条数据\n')
      
    while 1:
      get_post_per_page(start_thread)
      try:
        # 看是否有下一页
        if page.ele('text=Next »'):
          page.ele('text=Next »').click(by_js=False)
        else:
          break
        page.wait(WAIT_TIME)
      except Exception as e:
        print(e,"最后一页！368行")
        break
      start_thread = 0
      
    # 程序结束时存入日志文件
    with open(log_file_name, 'a', encoding='utf-8') as f:
      f.write(f'在{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}时刻: 已有{get_data_num()}条数据\n')
  except Exception as e:
    print(e,'在485行')
  # tabmenu_45 = page.ele('#tabmenu_45')
  # useful_data['forum_thead']
def Social_module():
  useful_data['module'] = 'Social'
#   tabmenu_7
  pass
def Tech_module():
  useful_data['module'] = 'Tech'
#   tabmenu_53 tabmenu_151 tabmenu_88 tabmenu_141 tabmenu_156
  pass
def Market_module():
  useful_data['module'] = 'Market'
  pass
def Money_module():
  useful_data['module'] = 'Money'
#   tabmenu_105
  pass
def VIP_module():
  useful_data['module'] = 'VIP'
#   tabmenu_241
  pass
#endregion

if __name__ == '__main__':
  while 1:
    try:
      # 打开浏览器
      page.get('https://hackforums.net/')
      if page.ele('text=403 Forbidden'):
        FZTError()
        # 403则等待60分钟
        time.sleep(3600)
        page.get('https://hackforums.net/')
        # region Description  403 Forbidden 2024.10.20 暂时放弃
            # while 1:
            #   if page.ele('text=403 Forbidden'):
            #     print('403 Forbidden！')
            #     page.refresh()
            #     page.wait(5)
            #   else:
            #     break
            # endregion
        # 等待
      page.wait(5)
      # 获取主要模块
      module_list = page.eles('x://ul[@class="shadetabs"]/li')
      # 获取主要forum内容
      forum_content_list = page.eles('xpath://div[@class="forum-content"]/div')
      Hack_module()
    except Exception as e:
      print(e,'536主函数内出错')

