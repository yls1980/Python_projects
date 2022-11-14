# -*- coding: utf-8 -*-

import simple_draw as sd


# Часть 1.
# Написать функции рисования равносторонних геометрических фигур:
# - треугольника
# - квадрата
# - пятиугольника
# - шестиугольника
# Все функции должны принимать 3 параметра:
# - точка начала рисования
# - угол наклона
# - длина стороны
#
# Примерный алгоритм внутри функции:
#   # будем рисовать с помощью векторов, каждый следующий - из конечной точки предыдущего
#   текущая_точка = начальная точка
#   для угол_наклона из диапазона от 0 до 360 с шагом XXX
#      # XXX подбирается индивидуально для каждой фигуры
#      составляем вектор из текущая_точка заданной длины с наклоном в угол_наклона
#      рисуем вектор
#      текущая_точка = конечной точке вектора
#
# Использование копи-пасты - обязательно! Даже тем кто уже знает про её пагубность. Для тренировки.
# Как работает копипаста:
#   - одну функцию написали,
#   - копипастим её, меняем название, чуть подправляем код,
#   - копипастим её, меняем название, чуть подправляем код,
#   - и так далее.
# В итоге должен получиться ПОЧТИ одинаковый код в каждой функции

# Пригодятся функции
# sd.get_point()
# sd.get_vector()
# sd.line()
# Результат решения см lesson_004/results/exercise_01_shapes.jpg

def triangle(ppoint, angle, length_site):
    v1 = sd.get_vector(start_point=ppoint, angle=angle, length=length_site, width=3)
    v1.draw()

    v2 = sd.get_vector(start_point=v1.end_point, angle=angle + 120, length=length_site, width=3)
    v2.draw()

    v3 = sd.get_vector(start_point=v2.end_point, angle=angle + 240, length=length_site, width=3)
    v3.draw()


def square(ppoint, angle, length_site):
    v1 = sd.get_vector(start_point=ppoint, angle=angle, length=length_site, width=3)
    v1.draw()

    v2 = sd.get_vector(start_point=v1.end_point, angle=angle + 90, length=length_site, width=3)
    v2.draw()

    v3 = sd.get_vector(start_point=v2.end_point, angle=angle + 180, length=length_site, width=3)
    v3.draw()

    v4 = sd.get_vector(start_point=v3.end_point, angle=angle + 270, length=length_site, width=3)
    v4.draw()


def pentagon(ppoint, angle, length_site):
    v1 = sd.get_vector(start_point=ppoint, angle=angle, length=length_site, width=3)
    v1.draw()

    v2 = sd.get_vector(start_point=v1.end_point, angle=angle + 72, length=length_site, width=3)
    v2.draw()

    v3 = sd.get_vector(start_point=v2.end_point, angle=angle + 144, length=length_site, width=3)
    v3.draw()

    v4 = sd.get_vector(start_point=v3.end_point, angle=angle + 216, length=length_site, width=3)
    v4.draw()

    v5 = sd.get_vector(start_point=v4.end_point, angle=angle + 288, length=length_site, width=3)
    v5.draw()


def hexagon(ppoint, angle, length_site):
    v1 = sd.get_vector(start_point=ppoint, angle=angle, length=length_site, width=3)
    v1.draw()

    v2 = sd.get_vector(start_point=v1.end_point, angle=angle + 60, length=length_site, width=3)
    v2.draw()

    v3 = sd.get_vector(start_point=v2.end_point, angle=angle + 120, length=length_site, width=3)
    v3.draw()

    v4 = sd.get_vector(start_point=v3.end_point, angle=angle + 180, length=length_site, width=3)
    v4.draw()

    v5 = sd.get_vector(start_point=v4.end_point, angle=angle + 240, length=length_site, width=3)
    v5.draw()

    v6 = sd.get_vector(start_point=v5.end_point, angle=angle + 300, length=length_site, width=3)
    v6.draw()


point = sd.get_point(100, 100)
triangle(point, 0, 100)

point = sd.get_point(100, 400)
square(point, 0, 120)

point = sd.get_point(400, 100)
pentagon(point, 0, 90)

point = sd.get_point(400, 400)
hexagon(point, 0, 110)


# Часть 1-бис.
# Попробуйте прикинуть обьем работы, если нужно будет внести изменения в этот код.
# Скажем, связывать точки не линиями, а дугами. Или двойными линиями. Или рисовать круги в угловых точках. Или...
# А если таких функций не 4, а 44? Код писать не нужно, просто представь объем работы... и запомни это.

# Часть 2 (делается после зачета первой части)
#  Подумайте как можно устранить разрыв, который проявляется
#  под некоторыми углами поворота фигуры.
# - Я так понимаю, что жти разывы связаны с толшиной линии. При толщине в 30 они явно видны,
# проблема, что поворот линии идет по центру а не по краю. Кроме как уменьшить ширину, мне в голову ничего неприходит
#  Разрывы связаны с тем, что при вычислении вектора под определённым углом к точке
#  используются тригонометрические формулы. Результат чаще всего представляет собой десятичную
#  дробь. А при рисовании используются целые числа координат. Из-за этого получается погрешность.
#  Следующий вектор вычисляется уже от сдвинутой точки. Из-за этого погрешность накапливается.
#  И последний вектор получается с заметным смещением.


def figure_core(ppoint, size_count, length_site):
    if 0 < size_count < 360:
        step = int(360 / size_count)
        res_points = [ppoint]
        for angle in range(0, 360, step):
            v1 = sd.get_vector(start_point=ppoint, angle=angle, length=length_site)
            # v1.draw(color=sd.COLOR_WHITE, width=1)
            ppoint = v1.end_point
            res_points.append(ppoint)
        sd.lines(res_points, sd.COLOR_GREEN, True, 3)


def triangle(ppoint, length_site):
    figure_core(ppoint, 3, length_site)


def square(ppoint, length_site):
    figure_core(ppoint, 4, length_site)


def pentagon(ppoint, length_site):
    figure_core(ppoint, 5, length_site)


def hexagon(ppoint, length_site):
    figure_core(ppoint, 6, length_site)


point = sd.get_point(210, 110)
triangle(point, 200)

point = sd.get_point(110, 510)
square(point, 80)

point = sd.get_point(350, 110)
pentagon(point, 80)

point = sd.get_point(350, 350)
hexagon(point, 70)

# Надо сформировать функцию, параметризированную в местах где была "небольшая правка".
# Это называется "Выделить общую часть алгоритма в отдельную функцию"
# Потом надо изменить функции рисования конкретных фигур - вызывать общую функцию вместо "почти" одинакового кода.
#
# В итоге должно получиться:
#   - одна общая функция со множеством параметров,
#   - все функции отрисовки треугольника/квадрата/етс берут 3 параметра и внутри себя ВЫЗЫВАЮТ общую функцию.
#
# Не забудте в этой общей функции придумать, как устранить разрыв в начальной/конечной точках рисуемой фигуры
# (если он есть. подсказка - на последней итерации можно использовать линию от первой точки)

# Часть 2-бис.
# А теперь - сколько надо работы что бы внести изменения в код? Выгода на лицо :)
# Поэтому среди программистов есть принцип D.R.Y. https://clck.ru/GEsA9


sd.pause()

# зачет!
