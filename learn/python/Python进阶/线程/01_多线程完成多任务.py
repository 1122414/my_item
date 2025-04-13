import time
import threading
# 编写代码
def coding():
  for i in range(10):
    print("正在写代码...")
    time.sleep(0.2)

def music():
  for i in range(10):
    print("正在弹奏音乐...")
    time.sleep(0.2)

if __name__ == '__main__':
  # coding()
  # music()

  # 创建两个线程
  coding_thread = threading.Thread(target=coding)
  music_thread = threading.Thread(target=music)

  # 启动子线程执行任务
  coding_thread.start()
  music_thread.start()

