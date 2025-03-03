def logging (fn):
  def inner(*args,**kwargs):
    result = fn(*args,**kwargs)
    return result
  
  return inner 
# 使用装饰器装饰函数
@logging
def sum_num(*args,**kwargs):
  print(args,kwargs)

sum_num(1,2,3,age="18") # 输出 (1, 2, 3) {'age': '18'}