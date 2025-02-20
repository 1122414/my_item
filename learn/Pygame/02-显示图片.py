import os
import pygame

current_path = os.path.dirname(__file__)

pygame.init()
window = pygame.display.set_mode((840, 480))
pygame.display.set_caption("显示页面")
# 设置背景颜色
window.fill((255,255,255))

# ============游戏开始页面静态效果=============
# 显示图片
# 1.加载图片
image1 = pygame.image.load(os.path.join(current_path, "images/hei.jpg"))

# 2.渲染图片
# window.blit(image1, (0, 0))
# 3.操作图片
# 1)获取图片大小
w,h = image1.get_size()
# window.blit(image1,((840-w)/2,(480-h)/2))
# print(w,h)

# 2)旋转和缩放
# scale(缩放对象，目标大小)
new_image = pygame.transform.scale(image1, (200, 200))
w_new,h_new = new_image.get_size()
# window.blit(new_image, (840-w_new, 480-h_new))

# rotozoom(缩放、旋转对象，旋转角度，缩放比例)
# 逆时针旋转
new_image_2 = pygame.transform.rotozoom(image1, 180, 0.5)
w_new,h_new = new_image_2.get_size()
window.blit(new_image_2,(0,0))


# 4.刷新页面
# 第一次刷新用flip()，后续刷新用update()
pygame.display.flip()
# pygame.display.update()

while True:
  # ==========游戏帧刷新============
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      exit()