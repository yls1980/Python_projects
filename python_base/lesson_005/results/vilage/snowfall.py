# -*- coding: utf-8 -*-
from random import shuffle


def sneg(sd):
    snowflakes = []
    for i in range(1, 15):
        x = sd.random_number(10, 200)
        y = sd.random_number(1, 30)
        snowflakes.append([x, y, sd.random_number(5, 30), sd.get_point(x, y)])
    # номера снежинок
    ind = [i for i in range(len(snowflakes))]

    for kolv in range(1, 50):
        sd.start_drawing()
        shuffle(ind)
        for n in ind:
            x, y, s, old_pos = snowflakes[n]
            point = old_pos
            if y < s:
                y = sd.random_number(10, 30)
            else:
                sd.snowflake(center=point, length=s, color=sd.background_color)
                y -= sd.random_number(5, 30)
            x += sd.random_number(-1 * round(0.2 * x), round(0.2 * x))
            new_point = sd.get_point(x, y)
            sd.snowflake(center=new_point, length=s, color=sd.COLOR_WHITE)
            snowflakes[n][1] = y
            snowflakes[n][3] = new_point

        sd.finish_drawing()
    return sd
