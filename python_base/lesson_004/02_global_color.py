# -*- coding: utf-8 -*-
import simple_draw as sd


def figure_core(ppoint, size_count, length_site, ch_color):
    if 0 < size_count < 360:
        step = int(360 / size_count)
        for angle in range(0, 360, step):
            v1 = sd.get_vector(start_point=ppoint, angle=angle, length=length_site, width=4)
            v1.draw(color=ch_color)
            ppoint = v1.end_point


def triangle(ppoint, length_site, ch_color=sd.COLOR_WHITE):
    figure_core(ppoint, 3, length_site, ch_color)


def square(ppoint, length_site, ch_color=sd.COLOR_WHITE):
    figure_core(ppoint, 4, length_site, ch_color)


def pentagon(ppoint, length_site, ch_color=sd.COLOR_WHITE):
    figure_core(ppoint, 5, length_site, ch_color)


def hexagon(ppoint, length_site, ch_color=sd.COLOR_WHITE):
    figure_core(ppoint, 6, length_site, ch_color)


# Добавить цвет в функции рисования геом. фигур. из упр lesson_004/01_shapes.py
# (код функций скопировать сюда и изменить)
# Запросить у пользователя цвет фигуры посредством выбора из существующих:
#   вывести список всех цветов с номерами и ждать ввода номера желаемого цвета.
# Потом нарисовать все фигуры этим цветом

# Пригодятся функции
# sd.get_point()
# sd.line()
# sd.get_vector()
# и константы COLOR_RED, COLOR_ORANGE, COLOR_YELLOW, COLOR_GREEN, COLOR_CYAN, COLOR_BLUE, COLOR_PURPLE
# Результат решения см lesson_004/results/exercise_02_global_color.jpg

#  Интересная структура данных, но будет удобнее, если ключами словаря будут
#  цифры, причём в виде строк. Это позволит по введённой пользователем цифре
#  сразу получить значение словаря. Название и значение цвета нужно хранить в значениях
#  словаря в кортеже, списке или словаре. Использование в ключах словаря строк
#  позволит не делать проверку sChoose.isdigit() и не преобразовывать sChoose в число.

colors = {
    '1': ("Красный", sd.COLOR_RED,),
    '2': ("Оранжевый", sd.COLOR_ORANGE,),
    '3': ("Желтый", sd.COLOR_YELLOW,),
    '4': ("Зеленый", sd.COLOR_GREEN,),
    '5': ("Сине-зеленый", sd.COLOR_CYAN),
    '6': ("Голубой", sd.COLOR_BLUE),
    '7': ("Синий", sd.COLOR_PURPLE),
    '8': ("Темно-желтый", sd.COLOR_DARK_YELLOW),
    '9': ("Темно-оранжевый", sd.COLOR_DARK_ORANGE),
    '10': ("Темно-красный", sd.COLOR_DARK_RED),
    '11': ("Темно=зеленый", sd.COLOR_DARK_GREEN),
    '12': ("Темной-сине-зеленый", sd.COLOR_DARK_CYAN),
    '13': ("Темно-голубой", sd.COLOR_DARK_BLUE),
    '14': ("Темно-синий", sd.COLOR_DARK_PURPLE),
    '15': ("Черный", sd.COLOR_BLACK,),
    '16': ("Белый", sd.COLOR_WHITE,)
}

print("Выберите номер цвета для раскраски фигур:")
for ncolor in colors:
    print(ncolor, colors.get(ncolor)[0])
sChoose = input("?:")
choose_color = colors.get(sChoose)[1]
if choose_color is None:
    choose_color = sd.COLOR_WHITE

point = sd.get_point(100, 400)
triangle(point, 80, choose_color)

point = sd.get_point(400, 100)
square(point, 80, choose_color)

point = sd.get_point(100, 100)
pentagon(point, 80, choose_color)

point = sd.get_point(400, 400)
hexagon(point, 70, choose_color)
sd.pause()

#  Обращайте внимание на предупреждения среды разработки о
#  проблемах в коде или нарушении стандарта PEP 8.
#  Попробуйте найти зеленую галочку справа над полосой прокрутки.
#  Если вместо нее, квадрат красного, желтого или серого цвета,
#  значит в файле есть недостатки оформления или ошибки.

# зачет!
