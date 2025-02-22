import os
import multiprocessing
import time
# 编写代码
def coding(num,name):
  print("coding父进程编号：",os.getppid())
  print("coding进程编号：",os.getpid())
  for i in range(num):
    print(name)
    print("coding...")
    time.sleep(0.2)

def music(count):
  print("music进程编号：",os.getpid())
  for i in range(count):
    print("music...")
    time.sleep(0.3)

if __name__ == '__main__':
  print("主进程编号：",os.getpid())
  # coding()
  # music()
  # 通过进程类创建进程对象
  coding_process = multiprocessing.Process(target=coding,args=(5,"二哈"))
  music_process = multiprocessing.Process(target=music,kwargs={"count":3})
  # 程序启动：默认有一个主进程  启动子进程
  coding_process.start()
  music_process.start()