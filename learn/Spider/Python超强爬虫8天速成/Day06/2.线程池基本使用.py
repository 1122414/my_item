# import time
# #使用单线程串行方式执行

# def get_page(str):
#   print("正在下载：",str)
#   time.sleep(2)
#   print("下载完成：",str)

# name_list = ['python','java','c++','javascript']

# star_time = time.time()

# for i in range(len(name_list)):
#   get_page(name_list[i])

# end_time = time.time()
# print('%d second' %(end_time-star_time))



import time
from multiprocessing.dummy import Pool as ThreadPool
# 使用线程池方式执行
# 适当使用

star_time = time.time()

def get_page(str):
  print("正在下载：",str)
  time.sleep(2)
  print("下载完成：",str)

name_list = ['python','java','c++','javascript']
# 实例化一个线程池对象
pool = ThreadPool(4)
# 将列表中每一个列表元素传递给get_page进行处理
pool.map(get_page,name_list)

end_time = time.time()
print('%d second' %(end_time-star_time))


