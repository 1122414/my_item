import threading
# 全局
g_num = 0

# 对g_num进行加1操作
def add_num():
  # 上锁
  mutex.acquire()
  for i in range(1000000):
    global g_num
    g_num += 1
  print("g_num:",g_num)

# 对g_num进行加1操作
def add_num1():
  # 上锁
  mutex.acquire()
  for i in range(1000000):
    global g_num
    g_num += 1
  print("g_num:",g_num)

if __name__ == '__main__':
  # 创建锁
  mutex = threading.Lock()

  # 创建线程
  add_num_thread = threading.Thread(target=add_num)
  add_num1_thread = threading.Thread(target=add_num1)

  add_num_thread.start()
  add_num1_thread.start()

