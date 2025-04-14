# Flask:

## 初始：

### 需要建立两个文件夹和一个入口文件

1. static文件夹（存放js、css、img等静态资源）
2. templates文件夹（存放html页面资源）
3. app.py（入口文件）

### 

### 代码框架

~~~python
from flask import Flask
app = Flask(__name__)
@app.route('/')
def hello_world():
    return 'Hello World!'
if __name__ == '__main__':
    # 注：vscode中的host、port、debug均要在launch中配置
    app.run(
    	host='127.0.0.5',
        port= 5000,
        debug=True
    )
~~~



### 解释点

~~~python
# 路由  <int>必须遵守，不然会出现页面not found
@app.route('/blog/<int:blog_id>')
~~~

![image-20250413225215893](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20250413225215893.png)



~~~python
# 查询字符串传参
# 前端传入：127.0.0.5:8000/book/list?page=5
# 加default 页数错误会返回default页；不加 错误则返回None
@app.route('/book/list')
def book_list():
    page = request.args.get('page',default=1,type=int)
    return f'您获取的是第{page}页!'
~~~

**还有，路由下的函数中必须要有return！！**



## 模版：

### 基础模版

~~~python
@app.route('/')
def hello_world():
    user = User("张三", 18)
    person = {"name": "李四", "age": 20}
    # 渲染模版
    return render_template('index.html',userss=user,personn=person)

# 在templates的html页面中使用{{userss}},{{psersonn}}接收值
~~~

![image-20250413225744937](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20250413225744937.png)

### 系统定义过滤器

~~~python
# 在html中使用管道符 | 实现
{{my_list|length}}
~~~

### 自定义过滤器

~~~python
def datetime_format(value,format="%Y-%m-%d %H:%M:%S"):
    return value.strftime(format)
# 划重点 add_template_filter 自定义过滤器
app.add_template_filter(datetime_format,'dtf')

@app.route('/filter')
def filter_demo():
    my_list = [1, 2, 3, 4, 5]
    my_time = datetime.datetime.now()
    return render_template('filter.html',my_list=my_list,my_time=my_time)
~~~

![image-20250413230019770](C:\Users\Lenovo\AppData\Roaming\Typora\typora-user-images\image-20250413230019770.png)

### 继承

~~~html
<-- 父模版中：不会理会block，会无视，即：{% block title%}111111{% endblock %} 等价于 111111 -->
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{% block title%}111111{% endblock %}</title>
  </head>
  <body>
    <ul>
      <li><a href="#">1</a></li>
      <li><a href="#">2</a></li>
      <li><a href="#">3</a></li>
      <li><a href="#">4</a></li>
      <li><a href="#">5</a></li>
    </ul>
    父模版文字 {% block body%}1111111{% endblock %}
    <footer>这是底部标签</footer>
  </body>
</html>

~~~

~~~jinja2
<-- 在html中进行 -->
<-- 注意子模版中的block中的内容会直接全部替换掉base中的block内容 -->
{% extends 'base.html' %} 
{%block title %} 我是子模版的标题1 {% endblock %}
{%block body %} 我是child1 {% endblock %}
~~~



### 控制器（if、for等）

~~~python
@app.route('/control')
def control_demo():
    age = 17
    books = [
        {
            'name': '西游记',
            'author': '吴承恩',
            'price': 109
        },
        {
            'name': '红楼梦',
            'author': '曹雪芹',
            'price': 120
        },
    ]
    return render_template('control.html',age=age,books=books)
# 在html中 必须成对出现
{%if%}
{%elif%}
{%elif%}
{%endif%}

{%for%}
{%endfor%}

# 样例
{%if age>18 %}
<p>成年人</p>
{% elif age==18 %}
<p>刚成年</p>
{% elif age<18 %}
<p>未成年</p>
{%endif%}

{%for i in books%} {{i}} {%endfor%}
~~~



## 数据库：

### 安装并导入几个库

~~~python
# 在app.config中设置好连接数据库的信息
# 然后使用SQLAlchemy(app)创建一个db对象
# SQLAlchemy会自动读取app.config中的配置信息，并创建数据库连接
from flask_sqlalchemy import SQLAlchemy

# SQLAlchemy执行sql语句时，不能直接使用字符串，需引入text
from sqlalchemy import text

# 迁移ORM模型：在对对象进行修改后，能对数据库进行修改
from flask_migrate import Migrate
~~~



### 创建

### 连接对象

~~~python
from flask import Flask
app = Flask(__name__)
HOSTNAME = 'localhost'
PORT = 3306
USERNAME = 'root'
PASSWORD = '3306'
DATABASE = 'flask_demo'
DB_URI = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4'
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
~~~



### 测试连接

~~~python
# 测试连接
with app.app_context():
  with db.engine.connect() as conn:
    # SQLAlchemy执行sql语句时，不能直接使用字符串，需要text()进行封装
    rs = conn.execute(text("select 1"))
    print(rs.fetchone())
~~~



### ORM模型：关系对象映射模型，只需要修改少量代码即可更换数据库

~~~python
# 将类变为ORM模型，只需继承db.Model即可
class User(db.Model):
    # 数据库中表名叫user
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # String相当于varchar
    name = db.Column(db.String(25), nullable=False)
    age = db.Column(db.Integer, default=18)
~~~



### 执行创建表

~~~python
with app.app_context():
  # create_all的局限性：只能识别新出现的模型，对模型中的字段的修改无能为力
  db.create_all()
~~~



### 增

~~~python
@app.route('/user/add')
def add_user():
  # 1.创建ORM对象
  user1 = User(name='zhangsan2222', age=18)
  user2 = User(name='zhangsan3333', age=18)
  # 2，将对象添加到db.session中
  db.session.add_all([user1,user2])
  db.session.commit()
  return 'user add success'
~~~



### 删

~~~python
@app.route('/user/delete')
def delete_user():
  # 1.先查询出要更新的用户
  # 删除不存在的记录话会报错
  user = User.query.filter(User.name == 'zhangsan2222').first()
  if user is not None:
    # 2.修改属性
    db.session.delete(user)
    # 3.提交事务
    db.session.commit()
    return 'user delete success'
  else:
    return 'not found'
~~~



### 改

~~~python
@app.route('/user/update')
def update_user():
  # 1.先查询出要更新的用户
  user = User.query.get(1)
  # 2.修改属性
  user.name = 'lisi'
  # 3.提交事务
  db.session.commit()
  return 'user update success'
~~~



### 查

~~~python
@app.route('/user/query')
def query_user():
  # query:类似数组，有切片等方法、可以通过索引取值
  # 1.get查找：根据主键查找：返回的是user对象，而不是下面的query对象
  user1 = User.query.get(1)

  # 2.filter查找：根据条件查找
  # 也可以用User.query.filter(User.id == '2')[0]，但是如果没有数据，会报错，所以first更安全
  user2 = User.query.filter(User.id == '2').first()

  # 3.filter_by查找：根据条件查找
  users = User.query.filter_by(name='zhangsan2222')

  # 4.all查找：查找所有
  users2 = User.query.all()

  print(f'user1:{user1}--------user2:{user2}--------users:{users}--------users2:{users2[2]}')
  return f'{user1.name}----------{user2.age}----------{users[0].name}-------{users2[2].name}'
~~~



### 外键

~~~python
class User(db.Model):
    # 数据库中表名叫user
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(25), nullable=False)
    # back_populates
    # articles = db.relationship('Article', back_populates='author')

class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(25), nullable=False)
    content = db.Column(db.Text, nullable=False)

    # 添加作者外键
    # 外键必须是另外表的主键
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # back_populates
    # author = db.relationship('User', back_populates='articles')
    
    # relationship作用：相当于article.author = User.query.get(article.author_id)
    # back_populates、backref：反向查找，相当于user.articles = Article.query.filter(Article.author_id == user.id)
    # backref与back_populates的区别：backref与back_populates作用一样，但是back_populates要给双方绑定，更清楚
    author = db.relationship('User', backref='articles')
    
    
# 书籍增加
@app.route('/article/add')
def article_add():
  article1 = Article(title='title11111', content='content11111', author_id=1)
  article1.author = User.query.get(1)

  article2 = Article(title='title22222', content='content22222', author_id=1)
  article2.author = User.query.get(2)

  article3 = Article(title='title33333', content='content33333', author_id=1)
  article3.author = User.query.get(2)

  db.session.add_all([article1, article2, article3])
  db.session.commit()
  return 'article add success'
    
# 外键查询  
@app.route('/article/query_users_article')
# def query_articles():
#   '''打印文章的user'''
#   articles = Article.query.all()
#   for article in articles:
#     print(f'article:{article.title}, author:{article.author.name}')
#   return 'article query success'

def query_users_article():
  '''打印user的文章'''
  users = User.query.all()
  for user in users:
    print(f'user:{user.name}')
    for article in user.articles:
      print(f'\tarticle:{article.title}')
  return 'article query success'
~~~



### ORM模型迁移

~~~python
# create_all的局限性：只能识别新出现的模型，对模型中的字段的修改无能为力
# 所以引入
from flask_migrate import Migrate

# ORM模型映射成表的三步，在控制台执行
# 1.flask db init 创建迁移脚本，只需执行一次
# 2.flask db migrate 识别ORM模型的改变，生成迁移脚本
# 3.flask db upgrade 执行迁移脚本

# 在数据库中会生成一个版本记录表：alembic_version
# 在app.py的根目录下，生成一个migrations文件夹
# migrations文件夹中，versions文件夹：保存有每次迁移修改的信息以及版本号，支持版本回退

upgrade()：应用变更（如创建表、修改列）
downgrade()：撤销变更（回退到前一状态）
~~~

~~~bash
# Migrate一些操作

# 查看迁移历史
flask db history

# 回退到特定版本号
flask db downgrade ae1027a6acf

# 回退一个版本（相对路径）
flask db downgrade -1
~~~

