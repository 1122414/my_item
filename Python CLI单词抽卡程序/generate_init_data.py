# 使用Faker库生成虚拟数据
import os
import csv
from faker import Faker
import random

now_path = os.path.abspath(os.path.dirname(__file__))  # 获取当前路径
# 初始化Faker
fake = Faker()
fake_cn = Faker('zh_CN')  # 中文数据生成
# 单词列表
word_list = []

def generate_word_list(num):
  for i in range(num):
    # 生成英文单词（确保唯一）
    try:
      en_word = fake.unique.word().capitalize()
    except Exception as e:
      # 生成了重复单词，重新生成
      en_word = fake.word().capitalize()+'repeat_word'
    # 生成中文单词（确保唯一）
    ran = random.random()
    # 注意：fake.bs()只能生成英文单词，fake_cn.word()和fake_cn.sentence()可以生成中文
    cn_meaning = fake_cn.word() if ran > 0.3 else fake_cn.sentence()
    word_list.append([en_word, cn_meaning])
  return word_list

def init_word_list(word_list):
  csv_path = os.path.join(now_path, 'words.csv')  # 保存路径
  with open (csv_path,'w',newline='',encoding='utf-8') as f:
    # csv.writer 是专门用来写csv文件的
    writer = csv.writer(f)
    writer.writerow(['English Word', 'Chinese Meaning'])
    writer.writerows(word_list)

def init_user_data(word_list):
  user_data_path = os.path.join(now_path, 'user_words_data.csv')  # 保存用户单词信息
  with open (user_data_path,'w',newline='',encoding='utf-8') as f:
    # csv.writer 是专门用来写csv文件的
    writer = csv.writer(f)
    writer.writerow(['English Word', 'Chinese Meaning','correct_count','wrong_count'])
    writer.writerows([[en_word, cn_meaning, 0, 0] for en_word, cn_meaning in word_list])

if __name__ == '__main__':
  word_list = generate_word_list(1000)
  init_word_list(word_list)
  init_user_data(word_list)
  print('生成1000个单词成功！')