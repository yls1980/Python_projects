# -*- coding: utf-8 -*-

import simple_draw as sd

# Шаг 1: Реализовать падение снежинки через класс. Внести в методы:
#  - создание снежинки с нужными параметрами
#  - отработку изменений координат
#  - отрисовку

"""
class Snowflake:
    # snejinki = []
    total_quant_max = 500

    def __init__(self, v_sf_count=10):
        self.snejinki = []
        self.resBottonSF = []
        self.total_quant_sf = 0
        for i in range(v_sf_count):
            self.create_snej()

    def create_snej(self):
        x = sd.random_number(1, 600)
        y = sd.random_number(1, 600)
        self.snejinki.append([x, y, sd.random_number(10, 50), sd.get_point(x, y)])
        self.total_quant_sf += 1

    def draw(self, color=sd.COLOR_WHITE):
        n = 0
        for snowflake in self.snejinki:
            x, y, size, position = snowflake
            sd.snowflake(center=position, length=size, color=color)
            n += 1

    def move(self, step=10):
        n = 0
        for snowflake in self.snejinki:
            x, y, size, position = snowflake
            y -= step
            new_point = sd.get_point(x, y)
            self.snejinki[n][1] = y
            self.snejinki[n][3] = new_point
            n += 1

    def can_fall(self):
        for i, (x, y, size, position) in enumerate(self.snejinki):
            if y - size <= 0:
                self.resBottonSF.append(i)
                self.delete_snejinka(i)
                # self.create_snej() #cснегопад
        # return self.total_quant_sf < Snowflake.total_quant_max #cснегопад
        return len(self.snejinki) > 0  # падение снежинки

    def delete_snejinka(self, numb_snej):
        self.snejinki.pop(numb_snej)

    def clear_previous_picture(self):
        self.draw(sd.background_color)
"""

sd.clear_screen()


class Snejinka:

    def __init__(self):
        self.x = sd.random_number(1, 600)
        self.y = sd.random_number(1, 600)
        self.size = sd.random_number(10, 50)
        self.position = sd.get_point(self.x, self.y)

    def draw(self, color=sd.COLOR_WHITE):
        sd.snowflake(center=self.position, length=self.size, color=color)

    def move(self, step=10):
        self.y -= step
        self.position = sd.get_point(self.x, self.y)

    def clear_previous_picture(self):
        self.draw(sd.background_color)

    def can_fall(self):
        return self.y - self.size <= 0


#  В этом задании нужно сделать класс одной снежинки, в которой будут сохранятся
# не очень понятно. Класс снежинка - class snejinka:
# class Snowflake - создание и падение снежинок
# не могли бы Вы уточнить более подробно
#  координаты, и реализованы методы рисования, перемещения, ...
#  Для снегопада можно сделать класс снегопада, или реализовать снегопад несколькими
#  функциями.
#  Нужно сделать класс снежинки. Раньше снежика была списком параметров
#  координат и высоты. Сейчас снежинка должна быть самостоятельным объектом.
#  Каждая снежинка должна быть независимым от других классов.
#  В классе снежинки нужно использовать свойста координат, сохранённые
#  или сгенерированные в классе при инициализации объекта.
#  В классе должны быть методы: рисования снежинки, падения и
#  метод can_fall, который сигнализирует упала снежинка или нет.
#
# flake = Snowflake(3)

"""flake = Snejinka()
while True:
    flake.clear_previous_picture()
    flake.move()
    flake.draw()
    if flake.can_fall():
        break
    sd.sleep(0.1)
    if sd.user_want_exit():
        break

sd.pause()"""

# шаг 2: создать снегопад - список объектов Снежинка в отдельном списке, обработку примерно так:
# Раскомментируйте код ниже. После пары небольших изменений задание можно будет зачесть.
snejinki = []


def append_flakes(count):
    for i in range(count):
        snejinki.append(Snejinka())


def get_flakes(count=5):
    append_flakes(count)
    return snejinki


def get_fallen_flakes():
    nfall = 0
    for snej in snejinki:
        if snej.can_fall():
            nfall += 1
            snejinki.remove(snej)
    return nfall


flakes = get_flakes(count=6)  # создать список снежинок
while True:
    for flake in flakes:
        flake.clear_previous_picture()
        flake.move()
        flake.draw()
    fallen_flakes = get_fallen_flakes()  # подчитать сколько снежинок уже упало
    if fallen_flakes > 0:
        append_flakes(count=fallen_flakes)  # добавить еще сверху
    sd.sleep(0.1)
    if sd.user_want_exit():
        break

sd.pause()

# Зачёт!
