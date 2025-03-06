import os
import execjs

# 'c:\\Users\\Lenovo\\Desktop\\vscode_python'
# path1 = os.path.abspath('.')
# 'c:\\Users\\Lenovo\\Desktop'
# path2 = os.path.abspath('..')

current_path = os.path.dirname(os.path.abspath(__file__))
farther_path = os.path.dirname(current_path)
need_path = os.path.join(farther_path, 'JS_code/wechat.js')
# 1.实例化对象
node = execjs.get() 
# 2.js源文件编译
ctx = node.compile(open(need_path).read())

# 3.执行js函数
funcName = 'get_pwd("{0}")'.format('123456')
pwd = ctx.eval(funcName)
print(pwd)