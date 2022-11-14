# -*- coding: utf-8 -*-

# (цикл for)

import simple_draw as sd

rainbow_colors = (sd.COLOR_RED, sd.COLOR_ORANGE, sd.COLOR_YELLOW, sd.COLOR_GREEN,
                  sd.COLOR_CYAN, sd.COLOR_BLUE, sd.COLOR_PURPLE)

# Нарисовать радугу: 7 линий разного цвета толщиной 4 с шагом 5 из точки (50, 50) в точку (350, 450)
sd.resolution = (600, 500)
sd.background_color = sd.COLOR_DARK_BLUE
step = 0
for color in rainbow_colors:
    step += 5
    sd.line(sd.get_point(50 + step, 50), sd.get_point(350 + step, 450), color, 4)

sd.sleep(3)
sd.clear_screen()
# Усложненное задание, делать по желанию.
# Нарисовать радугу дугами от окружности (cсм sd.circle) за нижним краем экрана,
# поэкспериментировать с параметрами, что бы было красиво

for color in rainbow_colors:
    step += 15
    sd.circle(sd.get_point(170 * 4, -80 * 3), 165 * 3 + step, color, 15)

sd.pause()

# зачет!
