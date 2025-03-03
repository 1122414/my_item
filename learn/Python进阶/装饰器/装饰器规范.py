# 定义一个装饰器（修饰器的本质是闭包）
def check(fn):
  def inner():
    print("登录验证。。。")
    fn()
  return inner
  
# @解释器遇到@check会立即执行 comment = check(comment)
# 需要被装饰的函数
@check
def comment():
  print("发布评论。。。")
# 2.使用装饰器装饰函数（增加一个登录功能）


# comment = check(comment)

# 调用被装饰的函数
comment()