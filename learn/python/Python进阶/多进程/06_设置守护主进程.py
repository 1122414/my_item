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
  # 1.设置守护主进程,主进程退出后子进程直接销毁，不再执行子进程中的代码
  work_process.daemon = True
  # 启动子进程
  work_process.start()

  # 延时一秒钟
  time.sleep(1)

  # 2.手动销毁子进程
  work_process.terminate()
  
  print("主进程结束")