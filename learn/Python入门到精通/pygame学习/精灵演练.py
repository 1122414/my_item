import pygame
from plane_sprites import *

pygame.init()
screen = pygame.display.set_mode((480, 700))
clock = pygame.time.Clock()


bg = pygame.image.load(r"learn\Python入门到精通\飞机大战\images\images\background.png")
hero = pygame.image.load(r"learn\Python入门到精通\飞机大战\images\images\me1.png")
w_hero,h_hero = hero.get_size()

hero_location = pygame.Rect(150,500,w_hero,h_hero)

# 创建敌机精灵
enemy = GameSpirte(r"learn\Python入门到精通\飞机大战\images\images\enemy1.png")
enemy1 = GameSpirte(r"learn\Python入门到精通\飞机大战\images\images\enemy1.png",speed=2)

# 创建敌机精灵组
enemy_group = pygame.sprite.Group(enemy,enemy1)



while True:
  # 设置刷新率
  clock.tick(60)
  # 更新英雄位置
  hero_location.y-=1

  if hero_location.y<=-h_hero:
    hero_location.y=700

  screen.blit(bg,(0,0))
  screen.blit(hero,hero_location)

  # 让精灵组调用两个方法
  # update
  enemy_group.update()

  # draw - 在screen上绘制所有精灵
  enemy_group.draw(screen)

  pygame.display.update()

  for event in pygame.event.get():
    # print(event)
    if event.type == pygame.QUIT:
      # 退出游戏
      pygame.quit()
      exit()
  