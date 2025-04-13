# 入口文件
from flask import Flask

# 使用Flast类创建一个app对象
# __name__:代表当前app.py这个模块
# 相当于把当前的app.py当做一个包来处理
app = Flask(__name__)

# 创建一个路由和视图函数的映射
@app.route('/')
def hello_world():
    return 'Hello, World!'

# 1.debug模式

# 2.修改host

# 3.修改端口

if __name__ == '__main__':
    app.run()