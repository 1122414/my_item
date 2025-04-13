import pygame

# 1.初始化
pygame.init()

# 2.创建游戏窗口
# set_mode(大小)
pygame.display.set_mode((400, 600))
# set_caption("My Game")设值游戏标题
pygame.display.set_caption("My Game")
# 设置窗口背景

# 3.让游戏保持一直运行
# game loop(游戏循环)
while True:
  # 4.检测事件
  for event in pygame.event.get():
    # print(event)
    if event.type == pygame.QUIT:
      # 退出游戏
      pygame.quit()
      exit()