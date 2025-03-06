import numpy as np
def draw_hexagon(q, r):
  x = q * np.sqrt(3) + r * np.sqrt(3) / 2
  y = r * 1.5
  return x,y

size = 18

goals = [(size, -size, 0), (0, size, -size), (-size, 0, -size), (0, -size, size)]

for goal in goals:
  x, y = draw_hexagon(goal[0], goal[1])
  print(f"x:{x},y:{y}")