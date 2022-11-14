# -*- coding: utf-8 -*-

# (цикл for)
import simple_draw

# Нарисовать стену из кирпичей. Размер кирпича - 100х50
# Использовать вложенные циклы for

simple_draw.resolution = (600, 700)
simple_draw.background_color = (160, 54, 35)
WIDTH_BLOCK = 100
HEIGTH_BLOCK = 50
WIDTH_WALL = 600
HEIGTH_WALL = 700
CEMENT_COLOR = (165, 163, 145)

k = 0
for i in range(0, HEIGTH_WALL, HEIGTH_BLOCK):
    start = simple_draw.get_point(1, i)
    end = simple_draw.get_point(WIDTH_WALL, i)
    simple_draw.line(start, end, CEMENT_COLOR, 3)

    k = HEIGTH_BLOCK - k
    for j in range(k, WIDTH_WALL + WIDTH_BLOCK, WIDTH_BLOCK):
        # Определения отступа для рядя лучше делать во внешнем цикле.
        # Я не очень понимаю как во внешнем цикле, когда я использую переменную внутреннего цикла(j) (чарез goto?)
        #  В зависимости от номера ряда можно задавать начальное значение диапазона
        #  внутреннего цикла. Т. е. вместо WIDTH_BLOCK на каждой итерации начинать с
        #  WIDTH_BLOCK - delta, a delta определять в зависимости от номера ряда.
        #  Ещё есть хитрый трюк, позволяющий совсе убрать условие.
        #  В внешнем цикле на каждой итерации меняем k:
        #  k = WIDTH_BLOCK - k. В результате k поочерёдно будет меняться с 50 на 0 и наоборот.
        # не могу понять как переменная без условия будет меняться?
        start_vert = simple_draw.get_point(j, 0 + i)
        end_vert = simple_draw.get_point(j, HEIGTH_BLOCK + i)
        simple_draw.line(start_vert, end_vert, CEMENT_COLOR, 3)

simple_draw.pause()

# зачет!
