# 带有参数的装饰器就是使用装饰器装饰函数的时候可以传入指定参数
# 注意外部函数只能有一个参数
def logging(flag):
  # 内部函数
  def decorator(fn):
    def inner(num1,num2):
      if flag == "+":
        print(f"Adding {num1} and {num2}")
      elif flag == "-":
        print(f"Subtracting {num1} and {num2}")
      result = fn(num1,num2)
      return result
    return inner
  return decorator

# 1 logging("+") 2 @decorator起装饰器作用
@logging("+")
def add(a,b):
  result = a + b
  return result

@logging("-")
def sub(a,b):
  result = a - b
  return result