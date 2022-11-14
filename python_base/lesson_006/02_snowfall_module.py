# -*- coding: utf-8 -*-

from lesson_006.snowfall import *

# На основе кода из lesson_004/05_snowfall.py
# сделать модуль snowfall.py в котором реализовать следующие функции
#  создать_снежинки(N) - создает N снежинок
#  нарисовать_снежинки_цветом(color) - отрисовывает все снежинки цветом color
#  сдвинуть_снежинки() - сдвигает снежинки на один шаг
#  номера_достигших_низа_экрана() - выдает список номеров снежинок, которые вышли за границу экрана
#  удалить_снежинки(номера) - удаляет снежинки с номерами из списка
# снежинки хранить в глобальных переменных модуля snowfall
#
# В текущем модуле реализовать главный цикл падения снежинок,
# обращаясь ТОЛЬКО к функциям модуля snowfall

# создать_снежинки(N)

N = 6
create_sf(N)
while True:
    #  нарисовать_снежинки_цветом(color=sd.background_color)
    draw_color_sf(sd.background_color)
    #  сдвинуть_снежинки()
    move_sf(10)
    #  нарисовать_снежинки_цветом(color)
    draw_color_sf(sd.COLOR_ORANGE)
    sd.start_drawing()
    #  если есть номера_достигших_низа_экрана() то
    #       удалить_снежинки(номера)
    #       создать_снежинки(count)
    n_bottom_sf = bottom_of_screen_numbers()
    cnt_bottom_sf = len(n_bottom_sf)
    sd.finish_drawing()
    if cnt_bottom_sf > 0:
        deletesf(n_bottom_sf)
        create_sf(cnt_bottom_sf)
    sd.sleep(0.1)
    if sd.user_want_exit():
        break

sd.pause()

# Зачёт!
