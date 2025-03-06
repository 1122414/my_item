import os
import re
import time
def extract_numbers(s):
    return [int(num) for num in re.findall(r'\d+', s)]
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
with open(log_file_name, 'r', encoding='utf-8') as f:
  lines = f.readlines()

aim_log = ''
for i in reversed(lines):
  if "目前是第" in i:
    aim_log = i.split(' ')
    break

numbers = extract_numbers(aim_log[2])
print(numbers)

want_page = int(numbers[0])
start_thread = int(numbers[1])

print(type(want_page))
print(type(start_thread))
print(want_page, start_thread)