import time
import threading
# 全局变量
my_list = []

# 写入数据
def write_data():
  for i in range(10):
    print("写入数据：", i)
    my_list.append(i)
  print("write",my_list)

def read_data():
  print("read",my_list)

if __name__ == '__main__':
  write_thread = threading.Thread(target=write_data)
  read_thread = threading.Thread(target=read_data)
  write_thread.start()
  time.sleep(1)
  read_thread.start()
  write_thread.join()
  read_thread.join()