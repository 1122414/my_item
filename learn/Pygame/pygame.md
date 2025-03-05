# pygame入门

| 模块名           | 功能                       |
| ---------------- | -------------------------- |
| pygame.cdrom     | 访问光驱                   |
| pygame.cursors   | 加载光标                   |
| pygame.display   | 访问显示设备               |
| pygame.draw      | 绘制形状、线和点           |
| pygame.event     | 管理事件                   |
| pygame.font      | 使用字体                   |
| pygame.image     | 加载和存储图片             |
| pygame.joystick  | 使用游戏手柄或者类似的东西 |
| pygame.key       | 读取键盘按键               |
| pygame.mixer     | 声音                       |
| pygame.mouse     | 鼠标                       |
| pygame.movie     | 播放视频                   |
| pygame.music     | 播放音频                   |
| pygame.overlay   | 访问高级视频叠加           |
| pygame.rect      | 管理矩形区域               |
| pygame.sndarry   | 操作声音数据               |
| pygame.sprite    | 操作移动图像               |
| pygame.surface   | 管理图像和屏幕             |
| pygame.surfarray | 管理点阵图像数据           |
| pygame.time      | 管理时间和帧信息           |
| pygame.transform | 缩放和移动图像             |

## 01. 使用 `pygame` 创建图形窗口

### 1.1 游戏的初始化和退出

- 要使用 `pygame` 提供的所有功能之前，需要调用 `init` 方法
- 在游戏结束前需要调用一下 `quit` 方法

### 1.2 理解游戏中的坐标系

pygame.Rect()

~~~python
Rect(x,y,width,height) -> Rect
~~~

注意：pygame是一个比较特殊的类，内部只封装一些数字计算，不执行pygame.init()也能直接使用

注意：size属性返回的是元组，arg1：width，arg2：height



2、pygame.display()

pygame提供一个模块pygame.display用于创建、管理游戏窗口

| 方法                      | 说明               |
| ------------------------- | ------------------ |
| pygame.display.set_mode() | 初始化游戏显示窗口 |
| pygame.display.update()   | 刷新屏幕内容显示   |

#### set_mode方法

~~~python
set_mode(resolution=(0,0),flags=0.depth=0)
~~~

- **作用**：创建游戏显示窗口
- **参数**

  - resolution` 指定屏幕的 `宽` 和 `高`，默认创建的窗口大小和屏幕大小一致


  - flags` 参数指定屏幕的附加选项，例如是否全屏等等，默认不需要传递
  - depth` 参数表示颜色的位数，默认自动匹配

- **返回值**

  - ​	暂时** 可以理解为 **游戏的屏幕**，**游戏的元素** 都需要被绘制到 **游戏的屏幕** 上

- **注意**：必须使用变量记录 `set_mode` 方法的返回结果！因为：后续所有的图像绘制都基于这个返回结果

~~~python
# 创建游戏主窗口
screen = pygame.display.set_mode((480, 700))
~~~



### 1.4 简单的游戏循环

- 为了做到游戏程序启动后，**不会立即退出**，通常会在游戏程序中增加一个 **游戏循环**

- 所谓 **游戏循环** 就是一个 **无限循环**

- 在 **创建游戏窗口** 代码下方，增加一个无限循环

- - 注意：**游戏窗口不需要重复创建**

~~~python
# 创建游戏主窗口
screen = pygame.display.set_mode((480, 700))

# 游戏循环
while True:
    pass
~~~



## 02. 理解 **图像** 并实现图像绘制

### 代码演练 I —— 绘制背景图像

**需求**

1. 加载 `background.png` 创建背景
2. 将 **背景** 绘制在屏幕的 `(0, 0)` 位置
3. 调用屏幕更新显示背景图像

~~~python
# 绘制背景图像
# 1> 加载图像
bg = pygame.image.load("./images/background.png")

# 2> 绘制在屏幕
screen.blit(bg, (0, 0))

# 3> 更新显示
pygame.display.update()
~~~



### 代码演练 II —— 绘制英雄图像

**需求**

1. 加载 `me1.png` 创建英雄飞机
2. 将 **英雄飞机** 绘制在屏幕的 `(200, 500)` 位置
3. 调用屏幕更新显示飞机图像

~~~python
# 1> 加载图像
hero = pygame.image.load("./images/me1.png")

# 2> 绘制在屏幕
screen.blit(hero, (200, 500))

# 3> 更新显示
pygame.display.update()
~~~

**透明图像**

- `png` 格式的图像是支持 **透明** 的
- 在绘制图像时，**透明区域** 不会显示任何内容
- 但是如果**下方已经有内容**，会 **透过** **透明区域** 显示出来



### 理解 `update()` 方法的作用

可以在 `screen` 对象完成 **所有** `blit` 方法之后，**统一调用一次** `display.update` 方法，同样可以在屏幕上 **看到最终的绘制结果**

- 使用 `display.set_mode()` 创建的 `screen` **对象** 是一个 **内存中的屏幕数据对象**
  - 可以理解成是 **油画** 的 **画布**
- `screen.blit` 方法可以在 **画布** 上绘制很多 **图像**
  - 例如：**英雄**、**敌机**、**子弹**...
  - **这些图像** 有可能 会彼此 **重叠或者覆盖**
- `display.update()` 会将 **画布** 的 **最终结果** 绘制在屏幕上，这样可以 **提高屏幕绘制效率**，**增加游戏的流畅度**

~~~python
# 绘制背景图像
# 1> 加载图像
bg = pygame.image.load("./images/background.png")

# 2> 绘制在屏幕
screen.blit(bg, (0, 0))

# 绘制英雄图像
# 1> 加载图像
hero = pygame.image.load("./images/me1.png")

# 2> 绘制在屏幕
screen.blit(hero, (200, 500))

# 3> 更新显示 - update 方法会把之前所有绘制的结果，一次性更新到屏幕窗口上
pygame.display.update()
~~~



## 03. 理解 **游戏循环** 和 **游戏时钟**

现在 **英雄飞机** 已经被绘制到屏幕上了，**怎么能够让飞机移动呢** ？

### 3.1 游戏中的动画实现原理

- 跟 **电影** 的原理类似，游戏中的动画效果，本质上是 **快速** 的在屏幕上绘制 **图像**
  - 电影是将多张 **静止的电影胶片** **连续、快速**的播放，产生连贯的视觉效果！
- 一般在电脑上 **每秒绘制 60 次**，就能够达到非常 **连续** **高品质** 的动画效果
  - 每次绘制的结果被称为 **帧 Frame**

### 3.2 **游戏循环**

#### 游戏的两个组成部分

**游戏循环的开始** 就意味着 **游戏的正式开始**

![image-20250303205201013](img/image-20250303205201013.png)

#### 游戏循环的作用

1. 保证游戏 **不会直接退出**
2. **变化图像位置** —— 动画效果
   - 每隔 `1 / 60 秒` 移动一下所有图像的位置
   - 调用 `pygame.display.update()` 更新屏幕显示
3. **检测用户交互** —— 按键、鼠标等...



### 3.3 游戏时钟

- `ygame` 专门提供了一个类 `pygame.time.Clock` 可以非常方便的设置屏幕绘制速度 —— **刷新帧率**
- 要使用 **时钟对象** 需要两步：
  1. 在 **游戏初始化** 创建一个 **时钟对象**
  2. 在 **游戏循环** 中让时钟对象调用 `tick(帧率)` 方法
- `tick` 方法会根据 **上次被调用的时间**，自动设置 **游戏循环** 中的延时

~~~python
# 3. 创建游戏时钟对象
clock = pygame.time.Clock()
i = 0

# 游戏循环
while True:

    # 设置屏幕刷新帧率
    clock.tick(60)

    print(i)
    i += 1
~~~



### 3.4 英雄的简单动画实现

**需求**

1. 在 **游戏初始化** 定义一个 `pygame.Rect` 的变量记录英雄的初始位置
2. 在 **游戏循环** 中每次让 **英雄** 的 `y - 1` —— 向上移动
3. `y <= 0` 将英雄移动到屏幕的底部

每一次调用 update() 方法之前，需要把 所有的游戏图像都重新绘制一遍,而且应该 最先 重新绘制 背景图像

~~~python
# 4. 定义英雄的初始位置
hero_rect = pygame.Rect(150, 500, 102, 126)

while True:

    # 可以指定循环体内部的代码执行的频率
    clock.tick(60)

    # 更新英雄位置
    hero_rect.y -= 1

    # 如果移出屏幕，则将英雄的顶部移动到屏幕底部
    if hero_rect.y <= 0:
        hero_rect.y = 700

    # 绘制背景图片
    screen.blit(bg, (0, 0))
    # 绘制英雄图像
    screen.blit(hero, hero_rect)

    # 更新显示
    pygame.display.update()
~~~



### 3.5 在游戏循环中 监听 事件

#### 事件 `event`

- 就是游戏启动后，**用户针对游戏所做的操作**
- 例如：**点击关闭按钮**，**点击鼠标**，**按下键盘**..

#### 监听

- 在 **游戏循环** 中，判断用户 **具体的操作*

只有 **捕获** 到用户具体的操作，才能有针对性的做出响应

#### 代码实现

- `pygame` 中通过 `pygame.event.get()` 可以获得 **用户当前所做动作** 的 **事件列表**
  - 用户可以同一时间做很多事情
- 提示：**这段代码非常的固定**，几乎所有的 `pygame` 游戏都 **大同小异**！

~~~python
# 游戏循环
while True:

    # 设置屏幕刷新帧率
    clock.tick(60)

    # 事件监听
    for event in pygame.event.get():

        # 判断用户是否点击了关闭按钮
        if event.type == pygame.QUIT:
            print("退出游戏...")

            pygame.quit()

            # 直接退出系统
            exit()
~~~



## 04. 理解 **精灵** 和 **精灵组**

### 4.1 精灵 和 精灵组

- 在刚刚完成的案例中，**图像加载**、**位置变化**、**绘制图像** 都需要程序员编写代码分别处理
- 为了简化开发步骤，`pygame` 提供了两个类
  - `pygame.sprite.Sprite` —— 存储 **图像数据 image** 和 **位置 rect** 的 **对象**
  - pygame.sprite.Group

![image-20250303215042305](img/image-20250303215042305.png)

#### 精灵

- 在游戏开发中，通常把 **显示图像的对象** 叫做精灵 `Sprite`
- **精灵** 需要 有 **两个重要的属性**
  - `image` 要显示的图像
  - `rect` 图像要显示在屏幕的位置
- 默认的 `update()` 方法什么事情也没做
  - 子类可以重写此方法，在每次刷新屏幕时，更新精灵位置
- **注意**：`pygame.sprite.Sprite` 并没有提供 `image` 和 `rect` 两个属性
  - 需要程序员从 `pygame.sprite.Sprite` 派生子类
  - 并在 **子类** 的 **初始化方法** 中，设置 `image` 和 `rect` 属性



### 4.2 派生精灵子类

1. 新建 `plane_sprites.py` 文件
2. 定义 `GameSprite` 继承自 `pygame.sprite.Sprite`

**注意**
- 如果一个类的 **父类** 不是 `object`
- 在重写 **初始化方法** 时，**一定要** 先 `super()` 一下父类的 `__init__` 方法
- **保证父类中实现的** `**__init__**` **代码能够被正常执行**

![image-20250303215941264](img/image-20250303215941264.png)

**属性**

- `image` 精灵图像，使用 `image_name` 加载
- `rect` 精灵大小，默认使用图像大小
- `speed` 精灵移动速度，默认为 `1`

**方法**

- `update` 每次更新屏幕时在游戏循环内调用
  - 让精灵的 `self.rect.y += self.speed`

**提示**

- `image` 的 `get_rect()` 方法，可以返回 **pygame.Rect(0, 0, 图像宽, 图像高)** 的对象

~~~python
import pygame

class GameSprite(pygame.sprite.Sprite):
    """游戏精灵基类"""
    
    def __init__(self, image_name, speed=1):
        
        # 调用父类的初始化方法
        super().__init__()
        
        # 加载图像
        self.image = pygame.image.load(image_name)
        # 设置尺寸
        self.rect = self.image.get_rect()
        # 记录速度
        self.speed = speed

    def update(self, *args):
        
        # 默认在垂直方向移动
        self.rect.y += self.speed
~~~



### 4.3 使用 游戏精灵 和 精灵组 创建敌机

**需求**

- 使用刚刚派生的 **游戏精灵** 和 **精灵组** 创建 敌机 并且实现敌机动画

**步骤**

1. 使用 `from` 导入 `plane_sprites` 模块

   - `from` 导入的模块可以 **直接使用**
   - `import` 导入的模块需要通过 **模块名.** 来使用

2. 在 **游戏初始化** 创建 **精灵对象** 和 **精灵组对象**

3. 在 **游戏循环中** 让 **精灵组** 分别调用 `update()` 和 `draw(screen)` 方法

**职责**

- 精灵

  - 封装 **图像 image**、**位置 rect** 和 **速度 speed**
  - 提供 `update()` 方法，根据游戏需求，**更新位置 rect**
- 精灵组
  - 包含 **多个** **精灵对象**
  - update` 方法，让精灵组中的所有精灵调用 `update` 方法更新位置
  - draw(screen)` 方法，在 `screen` 上绘制精灵组中的所有精灵



# **游戏框架搭建**

**目标** —— 使用 **面相对象** 设计 **飞机大战游戏类**

## 目标

- 明确主程序职责
- 实现主程序类
- 准备游戏精灵组

## 01. 明确主程序职责

- 回顾 **快速入门案例**，一个游戏主程序的 **职责** 可以分为两个部分：
  - 游戏初始化
  - 游戏循环
- 根据明确的职责，设计 `PlaneGame` 类如下：

![image-20250303222655893](img/image-20250303222655893.png)

**提示** 根据 **职责** 封装私有方法，可以避免某一个方法的代码写得太过冗长，如果某一个方法编写的太长，既不好阅读，也不好维护！



## 02. 实现飞机大战主游戏类

### 2.1 明确文件职责

![image-20250304141400124](img/image-20250304141400124.png)

- `plane_main`

   1. 封装 **主游戏类**
   2. 创建 **游戏对象**
   3. **启动游戏**

- `plane_sprites`

  - 封装游戏中 **所有** 需要使用的 **精灵子类**
  - 提供游戏的 **相关工具**

#### 代码实现

- 新建 `plane_main.py` 文件，并且设置为可执行
- 编写 **基础代码**

~~~python
import pygame
from plane_sprites import *


class PlaneGame(object):
    """飞机大战主游戏"""

    def __init__(self):
        print("游戏初始化")

    def start_game(self):
        print("开始游戏...")


if __name__ == '__main__':
    # 创建游戏对象
    game = PlaneGame()

    # 开始游戏
    game.start_game()
~~~



#### 使用 常量 代替固定的数值

- 常量 —— 不变化的量
- 变量 —— 可以变化的量

**应用场景**

- 在开发时，可能会需要使用 **固定的数值**，例如 **屏幕的高度** 是 `700`
- 这个时候，建议 **不要** 直接使用固定数值，而应该使用 **常量**
- 在开发时，为了保证代码的可维护性，尽量不要使用 **魔法数字**

**常量的定义**

- 定义 **常量** 和 定义 **变量** 的语法完全一样，都是使用 **赋值语句**
- **常量** 的 **命名** 应该 **所有字母都使用大写**，**单词与单词之间使用下划线连接**

**常量的好处**

- 阅读代码时，通过 **常量名** **见名之意**，不需要猜测数字的含义
- 如果需要 **调整值**，只需要 **修改常量定义** 就可以实现 **统一修改**

提示：Python 中并没有真正意义的常量，只是通过命名的约定 —— **所有字母都是大写的就是常量，开发时不要轻易的修改**！



# 碰撞检测

 目标 

- 了解碰撞检测方法
- 碰撞实现

## 01. 了解碰撞检测方法

- `pygame` 提供了 **两个非常方便** 的方法可以实现碰撞检测：

### pygame.sprite.groupcollide()

- **两个精灵组** 中 **所有的精灵** 的碰撞检测

~~~python
groupcollide(group1, group2, dokill1, dokill2, collided = None) -> Sprite_dict
~~~

- 如果将 `dokill` 设置为 `True`，则 **发生碰撞的精灵将被自动移除**
- `collided` 参数是用于 **计算碰撞的回调函数** 
  - 如果没有指定，则每个精灵必须有一个 `rect` 属性

### pygame.sprite.spritecollide()

- 判断 **某个精灵** 和 **指定精灵组** 中的精灵的碰撞

  ~~~python
  spritecollide(sprite, group, dokill, collided = None) -> Sprite_list
  ~~~
  
- 如果将 `dokill` 设置为 `True`，则 **指定精灵组** 中 **发生碰撞的精灵将被自动移除**

- `collided` 参数是用于 **计算碰撞的回调函数** 

  - 如果没有指定，则每个精灵必须有一个 `rect` 属性

- 返回 **精灵组** 中跟 **精灵** 发生碰撞的 **精灵列表**