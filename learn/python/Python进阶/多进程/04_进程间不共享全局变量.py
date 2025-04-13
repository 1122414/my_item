import multiprocessing

# 全局变量
my_list = []
def write_data(my_list):
  # 遍历从0到9的整数
  for i in range(10):
    # 将当前整数添加到列表my_list中
    my_list.append(i)
    # 打印当前写入的数据
    print("写入数据：", i)
  # 打印最终列表的内容
  print(my_list)
def read_data(my_list):
  print(my_list)

if __name__ == '__main__':
  # 创建写入数据进程
  write_process = multiprocessing.Process(target=write_data, args=(my_list,))
  read_process = multiprocessing.Process(target=read_data, args=(my_list,))
  # 创建读取数据进程
  write_process.start()
  read_process.start()
  # 等待写入数据进程结束
  write_process.join()
  # 等待读取数据进程结束
  read_process.join()