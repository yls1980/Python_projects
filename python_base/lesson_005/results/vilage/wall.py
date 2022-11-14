# -*- coding: utf-8 -*-
import math
import simple_draw as sd

def figure_core(spoint, length_site, ch_color, angle, wd):
    v_point = spoint
    v1 = sd.get_vector(start_point=v_point, angle=angle, length=length_site, width=wd)
    v1.draw(color=ch_color)
    return v1.end_point


def triangle(p_point, length_site, ch_color=sd.COLOR_WHITE, pangle=60):
    x, y = p_point.x, p_point.y
    vlength_site = length_site
    h = round((length_site / 2) * math.tan(math.radians(pangle)))
    while vlength_site >= 0:
        v_point = sd.get_point(x, y)
        figure_core(v_point, vlength_site, ch_color, 0, 1)
        delta = round((length_site / h) / math.tan(math.radians(pangle)))
        vlength_site -= delta * 2
        x += round(delta)
        y += 1


def wall():
    sd.resolution = (1200, 600)
    sd.background_color = (160, 54, 35)
    WIDTH_BLOCK = 30
    HEIGTH_BLOCK = 15
    WIDTH_WALL = 300
    HEIGTH_WALL = 300
    CEMENT_COLOR = (165, 163, 145)

    k = 0
    left = 400
    n = 0
    for i in range(0, HEIGTH_WALL, HEIGTH_BLOCK):
        start = sd.get_point(1 + left, i)
        end = sd.get_point(WIDTH_WALL + left, i)
        sd.line(start, end, CEMENT_COLOR, 3)
        n += 1
        if n % 2 != 0:
            start_vert = sd.get_point(left, 0 + i)
            end_vert = sd.get_point(left, HEIGTH_BLOCK + i)
            sd.line(start_vert, end_vert, CEMENT_COLOR, 3)
        k = HEIGTH_BLOCK - k
        for j in range(k, WIDTH_WALL + k + 1, WIDTH_BLOCK):
            if j == WIDTH_WALL + k:
                vleft = j + left - k
            else:
                vleft = j + left
            start_vert = sd.get_point(vleft, 0 + i)
            end_vert = sd.get_point(vleft, HEIGTH_BLOCK + i)
            sd.line(start_vert, end_vert, CEMENT_COLOR, 3)


def house():
    point = sd.get_point(300, 300)
    wall()
    triangle(point, 500, sd.COLOR_ORANGE, 40)

    sd.rectangle(sd.get_point(470, 70), sd.get_point(630, 230), sd.COLOR_BLUE, width=0)
    ram1 = (630 - 470 - 10) + 400
    ram2 = (230 - 70 + 10)
    sd.line(sd.get_point(ram1, 70), sd.get_point(ram1, 230), width=3)
    sd.line(sd.get_point(470, ram2), sd.get_point(630, ram2), width=3)
    return sd
