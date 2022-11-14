# -*- coding: utf-8 -*-
#  Странные мнипуляции с объектом sd
#  Лучше убрать Следующую строку и функцию init, а вместо них
#  импортировать библиотеку import simple_draw as sd
import simple_draw as sd


def derevo(start_point, coner_draw, length_branch, col, delta=30, rnd=40, wdt=3):
    v1 = sd.vector(start=start_point, angle=coner_draw, length=length_branch, color=col, width=wdt)
    delta_length = 0.75 * sd.random_number(-20, 20) / 100
    next_length = length_branch * (0.75 + delta_length)
    if next_length < 7:
        col = sd.COLOR_GREEN
        wdt = 1
    if next_length < 2:
        return None
    delta_coner1 = delta * sd.random_number(-rnd, rnd) / 100
    next_coner = coner_draw - delta + delta_coner1
    derevo(v1, next_coner, next_length, col, delta, rnd, wdt)
    delta_coner2 = delta * sd.random_number(-rnd, rnd) / 100
    next_coner1 = coner_draw - (360 - (delta + delta_coner2))
    derevo(v1, next_coner1, next_length, col, delta, rnd, wdt)
