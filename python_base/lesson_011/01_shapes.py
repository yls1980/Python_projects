# -*- coding: utf-8 -*-

import simple_draw as sd


# На основе вашего кода из решения lesson_004/01_shapes.py сделать функцию-фабрику,
# которая возвращает функции рисования треугольника, четырехугольника, пятиугольника и т.д.
#
# Функция рисования должна принимать параметры
# - точка начала рисования
# - угол наклона
# - длина стороны
#
# Функция-фабрика должна принимать параметр n - количество сторон.


def get_polygon(n):
    def shape_n(point, angle, length):
        for i in range(0, n):
            povorot = i * round(360 / n)
            vsize = sd.get_vector(start_point=point, angle=angle + povorot, length=length, width=3)
            vsize.draw()
            point = vsize.end_point

    return shape_n


draw_triangle = get_polygon(n=3)
draw_triangle(point=sd.get_point(200, 200), angle=13, length=100)

sd.pause()

# Зачёт!
