def logging (fn):
  def inner(a,b):
    fn(a,b)
  return inner 
# 使用装饰器装饰函数
@logging
def sum_num(a,b):
  result = a+b
  print(result)

sum_num(1,2) # 输出 3