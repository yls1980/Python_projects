# -*- coding: utf-8 -*-

import simple_draw as sd


# Запросить у пользователя желаемую фигуру посредством выбора из существующих
#   вывести список всех фигур с номерами и ждать ввода номера желаемой фигуры.
# и нарисовать эту фигуру в центре экрана

# Код функций из упр lesson_004/02_global_color.py скопировать сюда
# Результат решения см lesson_004/results/exercise_03_shape_select.jpg

def figure_core(spoint, size_count, length_site, ch_color):
    if 0 < size_count < 360:
        step = int(360 / size_count)
        v_point = spoint
        for angle in range(0, 360, step):
            v1 = sd.get_vector(start_point=v_point, angle=angle, length=length_site, width=4)
            v1.draw(color=ch_color)
            v_point = v1.end_point


def triangle(p_point, length_site, ch_color=sd.COLOR_WHITE):
    figure_core(p_point, 3, length_site, ch_color)


def square(p_point, length_site, ch_color=sd.COLOR_WHITE):
    figure_core(p_point, 4, length_site, ch_color)


def pentagon(p_point, length_site, ch_color=sd.COLOR_WHITE):
    figure_core(p_point, 5, length_site, ch_color)


def hexagon(p_point, length_site, ch_color=sd.COLOR_WHITE):
    figure_core(p_point, 6, length_site, ch_color)


functs = [triangle, square, pentagon, hexagon]

print("Какую фигуру нарисовать")
print("1 - Треугольник")
print("2 - Квадрат")
print("3 - Пятиугольник")
print("4 - Шестиугольник")
sChoose = input("?:")
nChoose = 0
if sChoose.isdigit():
    nChoose = int(sChoose)

if not (1 <= nChoose <= 4):
    nChoose = 1
sx, sy = 600, 600
nlength = 150
sd.set_screen_size(sx, sy)
# центр экрана
# центр экрана
ppoint = sd.get_point(int((sx - nlength) / 2), int((sy - nlength) / 2))
draw_function = functs[nChoose - 1]
draw_function(ppoint, nlength)

#  В этом задании нужно использовать отдельный функци рисования фигур.
#  Если нужно нарисовать треугольник, выз2ываете функцию triangle,
#  для квадрата square, и т. д.
#  Можно создать словарь или список с названием фигур и ссылками на функции:
#  functs = [pentagon, hexagon, triangle]
#  draw_function = functs[0]
#  draw_function(start_point, start_angle, length)
sd.pause()

# Есть галочка
#  Обращайте внимание на предупреждения среды разработки о
#  проблемах в коде или нарушении стандарта PEP 8.
#  Попробуйте найти зеленую галочку справа над полосой прокрутки.
#  Если вместо нее, квадрат красного, желтого или серого цвета,
#  значит в файле есть недостатки оформления или ошибки.

# зачет!
