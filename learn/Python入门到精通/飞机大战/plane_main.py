import time
import pygame
from plane_sprites import *

class PlaneGame(object):
  """飞机大战主游戏"""

  def __init__(self) -> None:
    pygame.init()
    # 1.创建游戏窗口
    self.screen = pygame.display.set_mode(SCREEN_RECT.size)
    # 2.创建游戏时钟
    self.clock = pygame.time.Clock()
    # 3.调用私有方法，精灵和精灵组的创建
    self.__create_sprites()
    # 4.设置定时器事件-创建敌机
    pygame.time.set_timer(CREATE_ENEMY_EVENT,CREATE_ENEMY_INTERVAL)
    pygame.time.set_timer(HERO_FIRE_EVENT,HERO_FIRE_INTERVAL)
    # 5.设置字体
    self.font = pygame.font.Font(r'learn\Pygame\font\font.ttf',30)
    # 6.设置游戏状态
    self.paused = False
    # 加载暂停/继续图标
    self.pause_image = pygame.image.load(
        r'learn\Python入门到精通\飞机大战\images\images\pause_nor.png'
    ).convert_alpha()
    self.resume_image = pygame.image.load(
        r'learn\Python入门到精通\飞机大战\images\images\resume_pressed.png'
    ).convert_alpha()
    # 设置图标位置（右上角）
    self.status_rect = self.pause_image.get_rect(topright=SCREEN_RECT.topright)
    # 7.加载游戏结束图片
    self.gameover_image = pygame.image.load(
            r'learn\Python入门到精通\飞机大战\images\images\gameover.png'
        ).convert_alpha()
    self.gameover_rect = self.gameover_image.get_rect(
            center=SCREEN_RECT.center
        )
    self.game_over = False  # 新增游戏结束标识

    print("游戏初始化")

  def __create_sprites(self):
    # 创建背景精灵和精灵组
    bg1 = Background()
    bg2 = Background(True)
    self.bg_group = pygame.sprite.Group(bg1,bg2)

    # 创建敌机精灵组
    self.en_group = pygame.sprite.Group()

    # 创建英雄的精灵和精灵组
    self.hero = Hero()
    self.hero_group = pygame.sprite.Group(self.hero)

  def start_game(self):
      # 无限循环，用于游戏的主循环
      while True:
        # 1.设置刷新帧率
        # 使用pygame的clock对象来控制游戏的帧率，确保游戏以每秒FRAME_PER_SEC帧的速度运行
        self.clock.tick(FRAME_PER_SEC)
        
        # 2.事件监听
        # 调用私有方法__event_handle来处理所有的事件，如键盘输入、鼠标点击等
        self.__event_handle()
        # 只在非暂停状态处理游戏逻辑
        if not self.paused:
          # 3.碰撞检测
          # 调用私有方法__check_collide来检测游戏中的碰撞事件，如精灵之间的碰撞
          self.__check_collide()
          # 4.更新/绘制精灵组
          # 调用私有方法__update_sprites来更新所有精灵的状态，并绘制到屏幕上
          self.__update_sprites()

        # 5.更新屏幕显示
        # 调用私有方法__draw_ui来绘制游戏的用户界面，如分数、生命值等
        self.__draw_ui()
        # 使用pygame的display.update方法来更新整个屏幕的显示
        pygame.display.update()
  
  def __event_handle(self):
    for event in pygame.event.get():
      print(f"现在的事件是：{event}")
      if event.type == pygame.QUIT:
        self.__game_over()

      if event.type == GAME_OVER_EVENT:
        self.__game_over()

      # 只在非暂停状态处理游戏相关事件
      if not self.paused:
        if event.type == CREATE_ENEMY_EVENT:
          self.enemy = Enemy()
          self.en_group.add(self.enemy)
          print("敌机出场")
        elif event.type == HERO_FIRE_EVENT:
          self.hero.fire()

      if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        self.__update_sprites()
        self.paused = not self.paused  # 切换暂停状态
        print(f"游戏状态：{'已暂停' if self.paused else '运行中'}")

      
        
         
      # 事件循环中  一次按下只执行一次
      # elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
      #   print("向右移动")
    # 使用键盘提供的方法获取键盘按键 - 按键元组
    keys_pressed = pygame.key.get_pressed()

    # 两个方向单独检测，不然会出现：按着上键的同时，再按着右键，然后松开上键，飞机还是会往上移动
    # 水平方向检测（独立判断）
    if keys_pressed[pygame.K_RIGHT]:
        self.hero.speed_x = 2
    elif keys_pressed[pygame.K_LEFT]:
        self.hero.speed_x = -2
    else:  # 没有水平按键时归零
        self.hero.speed_x = 0

    # 垂直方向检测（独立判断）
    if keys_pressed[pygame.K_UP]:
        self.hero.speed_y = -2
    elif keys_pressed[pygame.K_DOWN]:
        self.hero.speed_y = 2
    else:  # 没有垂直按键时归零
        self.hero.speed_y = 0
    

  def __check_collide(self):
    # 子弹摧毁敌机
    # 实现摧毁敌机加分
    # 子弹与敌机碰撞检测（子弹消失，敌机暂不消失）
    collisions = pygame.sprite.groupcollide(
        self.hero.bullets,  # 子弹组
        self.en_group,      # 敌机组
        True,               # 是否删除子弹（碰撞后删除）
        False               # 是否删除敌机（稍后根据HP判断）
    )

    # 遍历所有被击中的敌机
    for bullet, hit_enemies in collisions.items():
        for self.enemy in hit_enemies:
            self.enemy.hp -= 10  # 每次命中扣10HP
            print(f"敌机HP剩余：{self.enemy.hp}")
            if self.enemy.hp <= 0 and not self.enemy.is_destroying:
                self.enemy.destroy()  # 触发动画
                # self.enemy.kill()  # 销毁敌机
                self.hero.score += self.enemy.score  # 累加分
                print(f"击毁敌机，获得{self.enemy.score}分")

    # 每帧更新得分文字（无论是否碰撞）
    self.score_text = self.font.render(
        f'英雄得分：{self.hero.score}', 
        True, 
        (255,0,0), 
        (255,255,0)
    )

    # 敌机撞英雄检测（立即销毁双方）
    if pygame.sprite.spritecollideany(self.hero, self.en_group):
        self.game_over = True
        self.hero.destroy()  # 触发动画
        # 设置100ms后结束游戏（
        pygame.time.set_timer(GAME_OVER_EVENT, 50)  

    # enemies = pygame.sprite.spritecollide(self.hero,self.en_group,True)
    # # 如果collide返回列表不为空，表示有撞击
    # if enemies:
    #   self.hero.kill()
    #   self.__game_over()

  def __update_sprites(self):
    self.bg_group.update()
    self.bg_group.draw(self.screen)

    self.en_group.update()
    self.en_group.draw(self.screen)

    self.hero_group.update()
    self.hero_group.draw(self.screen)

    self.hero.bullets.update()
    self.hero.bullets.draw(self.screen)

  def __draw_ui(self):
    # 最后绘制文字（确保在最上层）
    if hasattr(self, 'score_text'):  # 确保首次渲染前不会报错
        self.screen.blit(self.score_text, (0,0))
    current_image = self.pause_image if not self.paused else self.resume_image
    self.screen.blit(current_image, self.status_rect)
    # 绘制Game Over画面
    if self.game_over:
        self.screen.blit(self.gameover_image, self.gameover_rect)

  # 静态方法，没使用到类属性、对象属性等
  @staticmethod
  def __game_over():
    print("游戏结束")
    pygame.quit()
    exit()

if __name__ == '__main__':

  # 创建游戏对象
  game = PlaneGame()

  # 启动游戏
  game.start_game()