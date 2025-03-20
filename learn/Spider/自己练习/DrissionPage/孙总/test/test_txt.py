import os
current_path = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_path,'../', '保研关键词.txt')
with open (file_path,'r',encoding='utf-8') as f:
  for line in f.readlines():
    data = line.strip()
    print(data)
