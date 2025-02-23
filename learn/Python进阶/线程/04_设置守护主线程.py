import threading
import time

# 工作函数
def work():
  for i in range(10):
    print("子进程正在工作:", i)
    time.sleep(0.2)

if __name__ == '__main__':
  # 创建子线程
  # 1.设置守护主进程,主进程退出后子进程直接销毁，不再执行子进程中的代码
  work_thread = threading.Thread(target=work,daemon=True)
  # work_thread = threading.Thread(target=work)
  # 启动子进程
  work_thread.start()
  # 2.方法设置
  # work_thread.setDaemon(True)# 已弃用
  # 延时一秒钟
  time.sleep(1)
  print("主进程结束")