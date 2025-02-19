import os
import csv
import copy
import random
import chardet
import argparse

# 检测编码并读取文件
current_dir = os.path.abspath(os.path.dirname(__file__))
error_set = set()

def detect_encoding():
    file_path = os.path.join(current_dir, 'user_words_data.csv')
    try:
      with open(file_path, "rb") as f:
          raw_data = f.read(10000)  # 读取前10000字节用于检测
          if not raw_data:
            raise ValueError("文件为空")
          return chardet.detect(raw_data)["encoding"]
    except FileExistsError:
       raise FileExistsError(f"{file_path}文件不存在，请检查文件路径")
    
encoding = detect_encoding()
# 加载单词
def load_words():
  with open(os.path.join(current_dir, 'user_words_data.csv'), 'r', encoding=encoding) as f:
      return list(csv.reader(f))
  
# 初始化错题集
def error_set_init():
  file_path = os.path.join(current_dir, 'error_set.csv')
  if not os.path.exists(file_path):
     with open(file_path, 'w', encoding=encoding, newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['English Word', 'Chinese Meaning','correct_count','wrong_count'])
  else:
    with open(file_path, 'r+', encoding=encoding)as f:
      reader = csv.reader(f)
      first_line = next(reader)
      if first_line != ['English Word', 'Chinese Meaning','correct_count','wrong_count']:
        writer = csv.writer(f)
        writer.writerow(['English Word', 'Chinese Meaning','correct_count','wrong_count'])
# 增加错题
def add_error(word):
    # 错题集中使用set会好很多
    with open(os.path.join(current_dir, 'error_set.csv'), 'w', encoding=encoding)as f:
      writer = csv.writer(f)
      writer.writerow(word)
  # 单词初始化

words = load_words()[1:]
error_words = []
def save_progress():
  with open(os.path.join(current_dir, 'user_words_data.csv'), 'w', encoding=encoding) as f:
        writer = csv.writer(f)
        writer.writerow(['English Word', 'Chinese Meaning','correct_count','wrong_count'])
        writer.writerows(words)
  pass
def save_error_set():
  with open(os.path.join(current_dir, 'error_set.csv'), 'w', encoding=encoding) as f:
    writer = csv.writer(f)
    writer.writerow(['English Word', 'Chinese Meaning','correct_count','wrong_count'])
    writer.writerows(error_words)
  pass

# 错题复习
def error_quiz():
  with open(os.path.join(current_dir, 'error_set.csv'), 'r', encoding=encoding) as f:
      return list(csv.reader(f))
  
def relearn():
   pass

# 注：quiz
def quiz(input_file, num_words, review_file):
  # 单词计数
  learn_count = 0

  # 错题集初始化
  error_set_init()
  corrections = 0
  while 1:
    learn_count += 1
    # 随机选择一个单词
    now_word_index = random.randint(0, len(words)-1)
    en,cn,correct_count,wrong_count = words[now_word_index]
    correct_count = int(correct_count)
    wrong_count = int(wrong_count)
    if correct_count>=3:
      # 大于等于3删除
      del words[now_word_index]
      continue
    # 输入答案
    answer = input(f"英[{en}]的中文是？：")
    if answer.strip().lower() == cn.strip().lower():
      print("回答正确！\n")
      correct_count += 1
      words[now_word_index][2] = correct_count
    elif answer.strip().lower() == 'exit':
      print(f"您已退出此次练习，本次练习正确率为：{corrections/learn_count*100}%")
      # 覆盖数据库文件（直接覆盖的都是  没有具体记忆
      save_progress()
      save_error_set()
      break
    else:
      print(f"回答错误，正确答案是：{cn}\n")
      # 错一次正确次数则归零
      words[now_word_index][2] = 0
      wrong_count += 1
      words[now_word_index][3] = wrong_count
      if words[now_word_index][3] == 1:
        # 注意 python的等号复制 只是复制地址 代表联动改变
        error_words.append(words[now_word_index])

def main():
  # 配置命令行参数解析器
  parser = argparse.ArgumentParser(
      description='英语单词抽卡程序 - 通过命令行测试你的词汇量',
      formatter_class=argparse.RawTextHelpFormatter
  )
  
  # 添加参数
  parser.add_argument(
      '--input-file',
      type=str,
      default='words.csv',
      help='指定单词库文件路径（默认: words.csv）\n示例: --input-file my_words.csv'
  )
  parser.add_argument(
      '--num-words',
      type=int,
      default=10,
      help='设置每次测试的单词数量（默认: 10）\n示例: --num-words 20'
  )
  parser.add_argument(
      '--review-file',
      type=str,
      default='review.csv',
      help='指定复习文件保存路径（默认: review.csv）\n示例:--review-file errors.csv'
  )
  # 解析参数并运行
  args = parser.parse_args()
  quiz(
      input_file=args.input_file,
      num_words=args.num_words,
      review_file=args.review_file
  )

if __name__ == '__main__':
  main()