import time
import os
import re 
# 获取当前路径
# current_path = os.path.dirname(__file__)
now_day = time.strftime('%Y-%m-%d', time.localtime())
# log_path = os.path.join(current_path, 'log')

def extract_numbers(s):
  return [int(num) for num in re.findall(r'\d+', s)]

log_lsit = os.listdir(r'E:\GitHub\Repositories\my_item\learn\Spider\自己练习\selenium\hack_forums\log')
now_log_index = log_lsit.index(now_day+'.log')
aim_log = log_lsit[now_log_index-1]
aim_log_path = os.path.join(r'E:\GitHub\Repositories\my_item\learn\Spider\自己练习\selenium\hack_forums\log', aim_log)
with open(aim_log_path, 'r', encoding='utf-8') as f:
  lines = f.readlines()

aim_log = ''
for i in reversed(lines):
  if "目前是第" in i:
    aim_log = i.split(' ')
    break
numbers = extract_numbers(aim_log[2])