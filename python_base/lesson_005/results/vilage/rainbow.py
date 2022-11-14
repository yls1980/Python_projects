# -*- coding: utf-8 -*-
def raduga(sd, x, y, rad=120):
    rainbow_colors = (sd.COLOR_RED, sd.COLOR_ORANGE, sd.COLOR_YELLOW, sd.COLOR_GREEN,
                      sd.COLOR_CYAN, sd.COLOR_BLUE, sd.COLOR_PURPLE)

    step = 0

    for color in rainbow_colors:
        step += 15
        sd.circle(sd.get_point(x, y), rad * 3 + step, color, 15)

    return sd

# зачет!
