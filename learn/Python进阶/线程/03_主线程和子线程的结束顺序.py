import time
import threading
# 工作函数
def work():
  for i in range(5):
    print("子线程正在工作", i)
    time.sleep(0.2)

if __name__ == '__main__':
  # 创建子线程
  work_thread = threading.Thread(target=work)
  # 启动子线程
  work_thread.start()

  time.sleep(1)
  print("主线程结束")