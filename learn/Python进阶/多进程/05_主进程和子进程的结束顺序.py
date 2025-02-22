import multiprocessing
import time

# 工作函数
def work():
  for i in range(10):
    print("子进程正在工作:", i)
    time.sleep(0.2)

if __name__ == '__main__':
  # 创建子进程
  work_process = multiprocessing.Process(target=work)
  # 启动子进程
  work_process.start()

  # 延时一秒钟
  time.sleep(1)
  print("主进程结束")