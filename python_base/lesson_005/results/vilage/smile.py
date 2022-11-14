# -*- coding: utf-8 -*-
def drow_smile(px, py, color_smile, sd):
    left1 = sd.get_point(px - 10, py + 10)
    right1 = sd.get_point(px + 100, py + 90)
    sd.ellipse(left1, right1, (165, 42, 42), 0)

    left = sd.get_point(px, py)
    right = sd.get_point(px + 90, py + 80)
    sd.ellipse(left, right, color_smile, 0)

    rot1 = sd.get_point(px + 30, py + 20)
    rot2 = sd.get_point(px + 60, py + 20)
    sd.line(rot1, rot2, sd.COLOR_DARK_RED, 8)

    nos1 = sd.get_point(px + 45, py + 60)
    nos2 = sd.get_point(px + 45, py + 30)
    sd.line(nos1, nos2, sd.COLOR_DARK_RED, 3)

    glas1 = sd.get_point(px + 22, py + 55)
    glas2 = sd.get_point(px + 67, py + 55)
    sd.circle(glas1, 8, sd.COLOR_BLUE, 0)
    sd.circle(glas2, 8, sd.COLOR_BLUE, 0)

    zrach1 = sd.get_point(px + 26, py + 55)
    zrach2 = sd.get_point(px + 63, py + 55)
    sd.circle(zrach1, 4, sd.COLOR_RED, 0)
    sd.circle(zrach2, 4, sd.COLOR_RED, 0)

    uho1 = sd.get_point(px + 5, py + 45)
    uho2 = sd.get_point(px + 84, py + 45)
    sd.circle(uho1, 10, sd.COLOR_GREEN, 0)
    sd.circle(uho2, 10, sd.COLOR_GREEN, 0)


def smile(x, y, sd):
    drow_smile(x, y, sd.COLOR_GREEN, sd)
    return sd
