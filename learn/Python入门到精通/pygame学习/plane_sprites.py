import pygame

# 定义屏幕大小常量
SCREEN_RECT = pygame.Rect(0, 0, 480, 700)
# 刷新帧率
FRAME_PER_SEC = 60

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