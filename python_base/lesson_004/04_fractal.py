# -*- coding: utf-8 -*-

import simple_draw as sd


# 1) Написать функцию draw_branches, которая должна рисовать две ветви дерева из начальной точки
# Функция должна принимать параметры:
# - точка начала рисования,
# - угол рисования,
# - длина ветвей,
# Отклонение ветвей от угла рисования принять 30 градусов,

# 2) Сделать draw_branches рекурсивной
# - добавить проверку на длину ветвей, если длина меньше 10 - не рисовать
# - вызывать саму себя 2 раза из точек-концов нарисованных ветвей,
#   с параметром "угол рисования" равным углу только что нарисованной ветви,
#   и параметром "длинна ветвей" в 0.75 меньшей чем длина только что нарисованной ветви

# 3) Запустить вашу рекурсивную функцию, используя следующие параметры:
# root_point = sd.get_point(300, 30)
# draw_branches(start_point=root_point, angle=90, length=100)

# Пригодятся функции
# sd.get_point()
# sd.get_vector()
# Возможный результат решения см lesson_004/results/exercise_04_fractal_01.jpg

# можно поиграть -шрифтами- цветами и углами отклонения
from simple_draw import Point


def draw_branches(start_point, coner_draw, length_branch, ncount=0):
    v1 = sd.get_vector(start_point=start_point, angle=coner_draw, length=length_branch, width=3)
    v1.draw()
    next_length = length_branch * 0.75
    if next_length < 10 or ncount == 2:
        return None
    next_coner = coner_draw - 30
    ncount += 1
    draw_branches(v1.end_point, next_coner, next_length, ncount)
    next_coner1 = coner_draw - (360 - 30)
    draw_branches(v1.end_point, next_coner1, next_length, ncount)
    return None


point1: Point = sd.get_point(300, 30)
# draw_branches(point1,90, 100)


# 4) Усложненное задание (делать по желанию)
# - сделать рандомное отклонение угла ветвей в пределах 40% от 30-ти градусов
# - сделать рандомное отклонение длины ветвей в пределах 20% от коэффициента 0.75
# Возможный результат решения см lesson_004/results/exercise_04_fractal_02.jpg


sd.set_screen_size(900, 800)


def draw_branches_rnd(start_point, coner_draw, length_branch):
    v1 = sd.get_vector(start_point=start_point, angle=coner_draw, length=length_branch, width=3)
    v1.draw()
    delta_length = 0.75 * sd.random_number(-20, 20) / 100
    next_length = length_branch * (0.75 + delta_length)
    if next_length < 10:
        return None
    delta_coner1 = 30 * sd.random_number(-40, 40) / 100
    next_coner = coner_draw - 30 + delta_coner1
    draw_branches_rnd(v1.end_point, next_coner, next_length)
    delta_coner2 = 30 * sd.random_number(-40, 40) / 100
    next_coner1 = coner_draw - (360 - (30 + delta_coner2))
    draw_branches_rnd(v1.end_point, next_coner1, next_length)
    return None


# Пригодятся функции
# sd.random_number()
point2 = sd.get_point(450, 30)
draw_branches_rnd(point2, 90, 150)

sd.pause()

# зачет!
