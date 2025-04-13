import pygame

pygame.init()

window = pygame.display.set_mode((640, 480))
pygame.display.set_caption("显示文字")

# 设置背景颜色
window.fill((255, 255, 255))

# =======显示文字========
# 1. 创建字体对象
# pygame.font.SysFont()  # 系统字体
# Font(字体文件路径，字号)
font = pygame.font.Font(r'learn\Pygame\font\font.ttf',30)  # 自定义字体

# 2.创建文字对象
# render(文字内容，True，文字颜色，背景颜色)
text = font.render('pygame hello',True,(255,0,0),(255,255,0))

# 3.渲染
window.blit(text,(0,0))

# 4.操作文字
# 1)获取大小
w,h = text.get_size()
window.blit(text,(640-w,480-h))

# 2)缩放和旋转
new_t1 = pygame.transform.scale(text,(200,100))
window.blit(new_t1,(0,60))

new_t2 = pygame.transform.rotozoom(text,45,2)
window.blit(new_t1,(0,120))


# 刷新
pygame.display.flip()

while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      exit()