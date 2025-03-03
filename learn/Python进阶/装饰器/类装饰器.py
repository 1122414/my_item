# from typing import Any


# class Check(object):
#   def __call__(self, *args: Any, **kwds: Any) -> Any:
#     print("Check.__call__")
#     pass

# c = Check()
# # 直接函数调用会直接调用__call__方法
# c()

#定义类装饰器
from typing import Any


class Check(object):
  def __init__(self, func):
    self.func = func

  def __call__(self, *args: Any, **kwds: Any) -> Any:
    print("登录")
    pass

@Check   # comment = Check(comment)
def comment():
  print("评论")

comment()