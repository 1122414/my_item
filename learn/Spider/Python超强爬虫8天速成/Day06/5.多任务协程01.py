import time 
import asyncio

def request(url):
  print(f"正在请求的url是 {url}")
  print(f"请求成功 {url}")

# async修饰的函数，调用后返回一个协程序对象
c = request('https://www.baidu.com')
