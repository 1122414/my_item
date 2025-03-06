import asyncio

def request(url):
  print(f"正在请求的url是 {url}")
  print(f"请求成功 {url}")

# async修饰的函数，调用后返回一个协程序对象
c = request('https://www.baidu.com')

# # 创建一个事件循环对象
# loop = asyncio.get_event_loop()

# # 将协程对象注册到loop中，然后启动loop
# loop.run_until_complete(c)

# task的使用
# loop = asyncio.get_event_loop()
# task = loop.create_task(c)
# print(task)

# loop.run_until_complete(task)
# print(task)

# future的使用
loop = asyncio.get_event_loop()
task = asyncio.ensure_future(c)
print(task)

loop.run_until_complete(task)
print(task)