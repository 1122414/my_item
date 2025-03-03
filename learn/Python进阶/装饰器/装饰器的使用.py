# 1.定义装饰器
# 2.装饰函数
# 要被装饰的函数
import time
def decorate(fn):
  def wrapper():
    start_time = time.time()
    print("装饰器开始")
    fn()
    end_time = time.time()
    print("装饰器结束，耗时：", end_time - start_time)
  return wrapper

@decorate
def func():
  for i in range(100000):
    print(i)

func()