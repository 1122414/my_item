# 装饰器1
def check1(fn1):
  def inner1():
    print("check1")
    fn1()
  return inner1

# 装饰器2
def check2(fn2):
  def inner2():
    print("check2")
    fn2()
  return inner2

@check1
@check2
def comment():
  print("评论内容")

comment()