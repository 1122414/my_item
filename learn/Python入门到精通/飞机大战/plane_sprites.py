import random
import pygame
from enum import Enum

# 定义屏幕大小常量
SCREEN_RECT = pygame.Rect(0, 0, 480, 700)
# 刷新帧率
FRAME_PER_SEC = 60
# 创建敌机定时器常量
CREATE_ENEMY_EVENT = pygame.USEREVENT
# 敌机间隔
CREATE_ENEMY_INTERVAL = 1000
# 英雄发射子弹事件
HERO_FIRE_EVENT = pygame.USEREVENT + 1
# 英雄发射子弹间隔
HERO_FIRE_INTERVAL = 500
# 游戏结束
GAME_OVER_EVENT = pygame.USEREVENT + 2


class GameSpirte(pygame.sprite.Sprite):
  """飞机大战游戏精灵"""
  def __init__(self, image_name, speed):
    # 当子类的父类不是Object基类，要先调用父类初始化方法
    super().__init__()
    
    # 定义对象的属性
    self.image = pygame.image.load(image_name)
    self.rect = self.image.get_rect()
    self.speed = speed

  def update(self):
    # 移动对象
    self.rect.y += self.speed

  def destory(self):
    # 销毁动画
    self.kill()
    print("精灵被销毁")

# 第一步：创建动画管理基类
class AnimatedSprite(GameSpirte):
    def __init__(self, image_name, speed, destroy_frames, frame_duration=100):
        super().__init__(image_name, speed)
        self.destroy_frames = destroy_frames  # 预加载的动画帧列表
        self.frame_duration = frame_duration  # 每帧持续时间(ms)
        self.current_frame = 0  # 当前动画帧索引
        self.animation_start_time = 0  # 动画开始时间
        self.is_destroying = False  # 是否正在播放销毁动画

    def start_destroy(self):
        print(f"开始播放销毁动画，剩余帧数：{len(self.destroy_frames)}")  # 调试用
        """开始播放销毁动画"""
        if not self.is_destroying:
            self.is_destroying = True
            self.current_frame = 0
            self.animation_start_time = pygame.time.get_ticks()
            if self.destroy_frames:
                self.image = self.destroy_frames[0]

    def update_animation(self):
        """更新动画帧（需在update()中调用）"""
        if self.is_destroying and self.destroy_frames:
            now = pygame.time.get_ticks()
            if now - self.animation_start_time > self.frame_duration:
                self.current_frame += 1
                self.animation_start_time = now
                if self.current_frame >= len(self.destroy_frames):
                    self.kill()
                    return True  # 返回True表示动画播放完成
                self.image = self.destroy_frames[self.current_frame]
        return False

class Background(GameSpirte):
  def __init__(self, is_alt = False):
    # 1.调用父类方法实现精灵创建（image/rect/speed）
    super().__init__(r"learn\Python入门到精通\飞机大战\images\images\background.png", 1)

    # 2.判断是否为背景图2，并设置相应属性
    if is_alt:
      self.rect.y = -self.rect.height

  """游戏背景精灵"""
  def update(self):
    # 调用父类
    super().update()

    # 判断是否移出屏幕，移出则将图像放屏幕上方
    if self.rect.y >= SCREEN_RECT.height:
      self.rect.y = -self.rect.height
    
class Enemy_Category(Enum):
  """敌机种类"""
  SMALL = 1
  MIDDLE = 2
  BIG = 3
  
class Enemy(AnimatedSprite):
  def __init__(self):
    self.is_destroying = False
    # 速度随机
    self.speed = random.randint(1, 3)
    # 类型随机
    self.category = random.randint(1, 3)
    # 每个类型敌机有不同分数、血量
    self.score = Enemy_Category(self.category).value * 10
    self.hp = Enemy_Category(self.category).value * 10

    # 加载销毁动画帧（必须转换为Surface对象）
    destroy_frames = [
        pygame.image.load(
            f"learn/Python入门到精通/飞机大战/images/images/enemy{self.category}_down{i}.png"
        ).convert_alpha() 
        for i in range(1 , 5 if self.category < 3 else 7)
    ]

    super().__init__(
      f"learn/Python入门到精通/飞机大战/images/images/enemy{self.category}.png",
      self.speed,
      destroy_frames=destroy_frames
    )

    # 指定动敌机初始位置
    self.rect.bottom = 0
    # 位置随机
    self.rect.x = random.randint(0, SCREEN_RECT.width - self.rect.width)

  # def __load_destroy_frames(self):
  #   """根据敌机类型加载不同动画帧"""
  #   frame_count = 4 if self.category in [1,2] else 6
  #   return [
  #     pygame.image.load(
  #         f"learn/Python入门到精通/飞机大战/images/images/enemy{self.category}_destroy_{i}.png"
  #     ).convert_alpha() 
  #     for i in range(frame_count)
  #   ]
  
  def update(self):
    if self.is_destroying:
        if self.update_animation():
            self.__del__()
        return
    # 1.调用父类方法，保持垂直方向的飞行
    super().update()
    # 2.判断是否飞出屏幕，是则从精灵组删除
    if self.rect.y >= SCREEN_RECT.height:
      self.kill()
    
  def destroy(self):
    """触发销毁动画"""
    self.is_destroying = True
    self.start_destroy()

  def __del__(self):
    self.kill()
    print("敌机被销毁")

class Hero(AnimatedSprite):
  def __init__(self):
    destroy_frames = [
      pygame.image.load(
          f"learn/Python入门到精通/飞机大战/images/images/me_destroy_{i}.png"
      ).convert_alpha()
      for i in range(1,5)
    ]
    # 初始化GameSpirte
    super().__init__(
      r"learn/Python入门到精通/飞机大战/images/images/me1.png",
      0,
      destroy_frames=destroy_frames
    )

    # 调用父类方法，创建精灵
    # super().__init__(r"learn\Python入门到精通\飞机大战\images\images\me1.png", 0)

    # 英雄机有score属性
    self.score = 0
    self.speed_x=0
    self.speed_y=0

    # 设置英雄初始位置
    self.rect.centerx = SCREEN_RECT.centerx
    self.rect.bottom = SCREEN_RECT.bottom - 10

    # 创建子弹精灵组
    self.bullets = pygame.sprite.Group()

    self.is_destroying = False

  def update(self):
    if self.is_destroying:
      self.update_animation()
      return
    # 英雄在水平方向移动
    self.rect.x += self.speed_x

    # 英雄在垂直方向移动
    self.rect.y += self.speed_y

    # 是否移出屏幕
    if self.rect.right >= SCREEN_RECT.right:
      self.rect.right = SCREEN_RECT.right
    elif self.rect.left <= 0:
      self.rect.left = 0

    if self.rect.bottom >= SCREEN_RECT.bottom:
      self.rect.bottom = SCREEN_RECT.bottom
    elif self.rect.top <= 0:
      self.rect.top = 0
    

  def fire(self):
    for i in range(1,4):
      print("开火")
      # 创建子弹精灵
      bullet = Bullet()

      # 设置精灵位置
      bullet.rect.bottom = self.rect.y - i * 20
      bullet.rect.centerx = self.rect.centerx

      # 将精灵添加到精灵组
      self.bullets.add(bullet)

  def destroy(self):
    """触发英雄机销毁动画"""
    if not self.is_destroying:
      self.is_destroying = True
      print("hero销毁程序")
      self.start_destroy()

class Bullet(GameSpirte):
  def __init__(self):
    super().__init__(r"learn\Python入门到精通\飞机大战\images\images\bullet1.png", -2)

  def update(self):
    super().update()
    if self.rect.bottom <= 0:
      self.__del__()

  def __del__(self):
    self.kill()
    print("子弹被销毁")

