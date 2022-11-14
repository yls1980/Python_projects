# -*- coding: utf-8 -*-

import random

import simple_draw as sd

sd.resolution = (1200, 600)


def next_pict():
    sd.sleep(3)
    sd.clear_screen()


# Нарисовать пузырек - три вложенных окружностей с шагом 5 пикселей
center_position = sd.get_point(500, 300)
number_circles = 0
for rd in range(150, 0, -5):
    if number_circles == 3:
        break
    sd.circle(center_position, rd, (255, 255, 0), 1)
    number_circles += 1


# Написать функцию рисования пузырька, принммающую 3 (или более) параметра: точка рисования, шаг и цвет
def drow_buble(center_point, radius, step_buble, color_buble):
    lnumber_circles = 0
    for vrad in range(radius, 0, -1 * step_buble):
        if lnumber_circles == 3:
            break
        sd.circle(center_point, vrad, color_buble, 1)
        lnumber_circles += 1


next_pict()

# Нарисовать 10 пузырьков в ряд


for i in range(0, 10):
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    drow_buble(sd.get_point(100 + i * 60, 100), 30, 5, color)

next_pict()

# Нарисовать три ряда по 10 пузырьков
for i in range(0, 10):
    for j in range(0, 3):
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        drow_buble(sd.get_point(300 + i * 60, 300 + j * 50), 40, 2, color)

next_pict()

# Нарисовать 100 пузырьков в произвольных местах экрана случайными цветами
for i in range(0, 100):
    drow_buble(sd.random_point(), sd.random_number(30, 100), 2, sd.random_color())

sd.pause()

# зачет!
