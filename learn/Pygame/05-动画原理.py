import pygame

WIN_WIDTH = 500
WIN_HEIGHT = 500

pygame.init()

window = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
pygame.display.set_caption("动画原理")
window.fill((255,255,255))
pygame.display.flip()

y = 0
num = 0

while True:
  num += 1
  # 1.移动动画
  # if num%10000 == 0:
  #   # 1.刷新背景
  #   # window.fill((255,255,255))
  #   # pygame.display.flip()

  #   # 2.覆盖圆
  #   pygame.draw.circle(window,(255,255,255),(250,y),100)
  #   y += 1
  #   pygame.draw.circle(window,(0,0,0),(250,y),100)
  #   pygame.display.update()

  # 2.放缩动画
  if num%10000 == 0:
    # 1.刷新背景
    # window.fill((255,255,255))
    # pygame.display.flip()

    # 2.覆盖圆
    pygame.draw.circle(window,(255,255,255),(250,250),100+y)
    y += 1
    pygame.draw.circle(window,(0,0,0),(250,250),100+y)
    pygame.display.update()

    if y >= 100:
      window.fill((255,255,255))
      pygame.display.update()

      while y >= 0:
        pygame.draw.circle(window,(255,255,255),(250,250),100+y)
        y -= 0.1
        pygame.draw.circle(window,(0,0,0),(250,250),100+y)
        pygame.display.update()



  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      exit()