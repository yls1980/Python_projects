# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

import simple_draw as sd

N = 4
snowflakes = []


# Названия функций и их аргументы должны быть записаны строчными буквами.
def create_sf(v_sf_count):
    #  При изменении содержимого объекта из глобальной области видимости
    #  не нужно объявлять её глобальной. global нужно только в случае, когда вы
    #  вы меняете саму переменную. Например для my_list.append() global не нужен.
    #  А для my_list = [] без global не обойтись.
    # global snowflakes
    for i in range(v_sf_count):
        x = sd.random_number(1, 600)
        y = sd.random_number(1, 600)
        snowflakes.append([x, y, sd.random_number(10, 50), sd.get_point(x, y)])


# Названия функций должны быть записаны строчными буквами.
def draw_color_sf(color):
    #  start_drawing и finish_drawing нужно перенести в основной модуль программы
    #  и вызывать до стирания и после рисования снежинок.
    n = 0
    for snowflake in snowflakes:
        x, y, size, position = snowflake
        sd.snowflake(center=position, length=size, color=color)
        n += 1


# Названия функций должны быть записаны строчными буквами.
def move_sf(step=10):
    # sd.start_drawing()
    n = 0
    for snowflake in snowflakes:
        x, y, size, position = snowflake
        y -= step
        new_point = sd.get_point(x, y)
        # sd.snowflake(center=position, length=size, color=sd.background_color)
        # sd.snowflake(center=new_point, length=size, color=color)
        snowflakes[n][1] = y
        snowflakes[n][3] = new_point
        n += 1
    # sd.finish_drawing()


# сделал так что возвращает не список номеров снежинок, а список их координат
# так как со списком номеров, после какого-то числа, начинает глючить, и показыват ошибки, что такой номера уже нету.
# на каком этапе происходит рассинхронизация я так и не понял.
#  При удалении элемента списка, все элементы, стоявшие в списке после него,
#  сдвигаются вперёд на одну позицию. Если в ground больше одного элемента,
#  то удаляютеся не те снежинки, которые нужно. Иногда может возникать ошибка
#  при попытке удалить элемент на позиции, большей чем количество оставшихся элементов.
#  Для исправления нужно либо развернуть его через метод списка reverse,
#  функцию reversed или через срез ground[::-1].
#  Это можно будет сделать перед циклом в функции удаления снежинок.
#  Сохранять номера упавших снежинок и удалять по индексу оптимальнее,
#  чем через метод remove, в котором выполняется поиск по объекту.
#
# сделал (строка 77)
def bottom_of_screen_numbers():
    resBottonSF = []
    #  Можно распаковать список snowflake сразу при
    #  объявлении цикла:
    #  for i, (x, y, size, position) in enumerate(snowflakes):
    for i, (x, y, size, position) in enumerate(snowflakes):
        if y - size <= 0:
            resBottonSF.append(i)
    return resBottonSF


# Названия функций и их аргументы должны быть записаны строчными буквами.
def deletesf(numbs_sf):
    rnumbs_sf = numbs_sf[::-1]
    for i in rnumbs_sf:
        snowflakes.pop(i)

# Обращайте внимание на предупреждения среды разработки о
#  проблемах в коде или нарушении стандарта PEP 8.
#  Попробуйте найти зеленую галочку справа над полосой прокрутки.
#  Если вместо нее, квадрат красного, желтого или серого цвета,
#  значит в файле есть недостатки оформления или ошибки.
#  Места с ошибками помечены цветными отметками на полосе прокрутки.
