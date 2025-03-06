import os
from watermarker.marker import add_mark
# current_path = os.path.dirname(os.path.abspath(__file__))
# full_path = os.path.join(current_path, 'images/')
# print(full_path)
add_mark('2024.7哔站爬虫\Python项目\images\白鹿my回头唯美古风4K美.jpg',mark='好看')

files = os.listdir('2024.7哔站爬虫\自己练习\selenium\my_selenium_utils\images')
# 还有别的属性
for file in files:
  add_mark(f'2024.7哔站爬虫\自己练习\selenium\my_selenium_utils\images\\{file}',mark='好看',opacity=0.5)
  # print(file)
  # add_mark('2024.7哔站爬虫\Python项目\images\\'+file,mark='好看')