import pygame

pygame.init()

window = pygame.display.set_mode((500, 500))
pygame.display.set_caption("显示图形")

window.fill((255, 255, 255))

# =========显示图形=========
# 1.画直线
# line(画在哪, 颜色, 起点坐标, 终点坐标, 线宽)
pygame.draw.line(window, (0, 0, 0), (0, 0), (500, 500), 5)

# 2.画折线
# lines(画在哪, 颜色, 是否闭合(第一个点和最后一个点连起来),点[列表]， 宽度 )
points = [(100, 100), (200, 200), (300, 100), (400, 200)]
pygame.draw.lines(window, (0, 0, 0), True, points, 5)
# pygame.draw.lines(window, (0, 0, 0), False, ((100, 100), (200, 200), (300, 100), (400, 200)), 5)

# 3.画圆
# circle(画在哪, 颜色, 圆心坐标, 半径, 线宽(默认是0填充,非0是圆环))
pygame.draw.circle(window, (0, 0, 0), (250, 250), 50, 5)

# 4.画矩形
# rect(画在哪, 颜色, 矩形范围, 线宽(默认是0填充,非0是边框))
pygame.draw.rect(window, (0, 0, 0), (100, 100, 200, 200), 5)

# 5.画椭圆
# ellipse(画在哪, 颜色, 矩形范围, 线宽(默认是0填充,非0是边框))
pygame.draw.ellipse(window, (0, 0, 0), (300, 300, 200, 100), 5)

# 6.画弧线
# arc(画在哪, 颜色, 矩形范围, 起始角度, 终止角度, 半径, 线宽(默认是1))
pygame.draw.arc(window, (0, 0, 0), (400, 400, 200, 200), 0, 3.1415926 * 2, 100, 5)


pygame.display.flip()

while True:
  for evenr in pygame.event.get():
    if evenr.type == pygame.QUIT:
      pygame.quit()
      exit()