# -*- coding: utf-8 -*-
def sun(sd, x, y):
    st_point = sd.get_point(x, y)
    sd.circle(st_point, 40, sd.COLOR_YELLOW, 0)
    for i in range(0,360,30):
        sd.vector(start=st_point, angle=i, length=80, color=sd.COLOR_YELLOW, width=5)
    return sd
