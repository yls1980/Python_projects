# -*- coding: utf-8 -*-

# (определение функций)
import simple_draw as sd


# Написать функцию отрисовки смайлика по заданным координатам
# Форма рожицы-смайлика на ваше усмотрение
# Параметры функции: кордината X, координата Y, цвет.
# Вывести 10 смайликов в произвольных точках экрана.

def drow_smile(px, py, color_smile):
    left1 = sd.get_point(px - 10, py + 10)
    right1 = sd.get_point(px + 100, py + 90)
    sd.ellipse(left1, right1, (165, 42, 42), 0)

    left = sd.get_point(px, py)
    right = sd.get_point(px + 90, py + 80)
    sd.ellipse(left, right, color_smile, 0)

    rot1 = sd.get_point(x + 30, y + 20)
    rot2 = sd.get_point(x + 60, y + 20)
    sd.line(rot1, rot2, sd.COLOR_DARK_RED, 8)

    nos1 = sd.get_point(px + 45, py + 60)
    nos2 = sd.get_point(px + 45, py + 30)
    sd.line(nos1, nos2, sd.COLOR_DARK_RED, 3)

    glas1 = sd.get_point(px + 22, py + 55)
    glas2 = sd.get_point(px + 67, py + 55)
    sd.circle(glas1, 8, sd.COLOR_BLUE, 0)
    sd.circle(glas2, 8, sd.COLOR_BLUE, 0)

    zrach1 = sd.get_point(x + 26, y + 55)
    zrach2 = sd.get_point(x + 63, y + 55)
    sd.circle(zrach1, 4, sd.COLOR_RED, 0)
    sd.circle(zrach2, 4, sd.COLOR_RED, 0)

    uho1 = sd.get_point(px + 5, py + 45)
    uho2 = sd.get_point(px + 84, py + 45)
    sd.circle(uho1, 10, sd.COLOR_GREEN, 0)
    sd.circle(uho2, 10, sd.COLOR_GREEN, 0)


for i in range(0, 10):
    x = sd.random_number(100, 500)
    y = sd.random_number(100, 500)
    drow_smile(x, y, sd.COLOR_GREEN)

sd.pause()

# зачет!
