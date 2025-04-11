import os
import re
import time
# 获取当前路径
current_path = os.path.dirname(__file__)
log_path = os.path.join(current_path,'../', 'log')
now_day = time.strftime('%Y-%m-%d', time.localtime())
# 日志文件名
log_file_name = os.path.join(log_path, f'{now_day}.log')
# 正则匹配数字
def extract_numbers(s):
    return [int(num) for num in re.findall(r'\d+', s)]
def get_page_number():
  # 每天第一次运行把前一次的最后一条数据放进去
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

  log_lsit = os.listdir(log_path)
  # aim_log_index = get_aim_log_index(log_lsit)
  # aim_log = log_lsit[aim_log_index]
  # aim_log_path = os.path.join(log_path, aim_log)

  aim_log = open_and_read_log()
  # if aim_log == 0:
  #   aim_log = open_and_read_log(aim_log_path)

  numbers = extract_numbers(aim_log[2])
  return numbers

if __name__ == '__main__':
  print(get_page_number())