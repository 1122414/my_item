# def talk(name):
#   def say_info(info):
#     print(name+":Hello, %s" % info)
#   return say_info


# f = talk("张三")
# f("你好")
# f("我是张三")

# f = talk("李四")
# f("你好")
# f("我是李四")

def func_out(num1):
  def func_inner(num2):
    # 声明外部变量
    nonlocal num1
    num1 = num2+10
    print(f"inner:{num1}")
  # 加func_inner 是30
  func_inner(20)

  print(num1)
  return func_inner

f = func_out(10)
f(num2=20)