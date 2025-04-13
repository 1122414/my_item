import threading
import time
# 编写代码
def coding(num,name):
  for i in range(num):
    print(name)
    print("coding...")
    time.sleep(0.2)

def music(count):
  for i in range(count):
    print("music...")
    time.sleep(0.3)

if __name__ == '__main__':
  # coding()
  # music()
  # 通过进程类创建进程对象
  coding_process = threading.Thread(target=coding,args=(5,"二哈"))
  music_process = threading.Thread(target=music,kwargs={"count":3})
  # 启动进程
  coding_process.start()
  music_process.start()