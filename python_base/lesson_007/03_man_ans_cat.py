# -*- coding: utf-8 -*-

""""""
# Доработать практическую часть урока lesson_007/python_snippets/08_practice.py

# Необходимо создать класс кота. У кота есть аттрибуты - сытость и дом (в котором он живет).
# Кот живет с человеком в доме.
# Для кота дом характеризируется - миской для еды и грязью.
# Изначально в доме нет еды для кота и нет грязи.

# Доработать класс человека, добавив методы
#   подобрать кота - у кота появляется дом.
#   купить коту еды - кошачья еда в доме увеличивается на 50, деньги уменьшаются на 50.
#   убраться в доме - степень грязи в доме уменьшается на 100, сытость у человека уменьшается на 20.
# Увеличить кол-во зарабатываемых человеком денег до 150 (он выучил пайтон и устроился на хорошую работу :)
# Кот может есть, спать и драть обои - необходимо реализовать соответствующие методы.
# Когда кот спит - сытость уменьшается на 10
# Когда кот ест - сытость увеличивается на 20, кошачья еда в доме уменьшается на 10.
# Когда кот дерет обои - сытость уменьшается на 10, степень грязи в доме увеличивается на 5
# Если степень сытости < 0, кот умирает.
# Так же надо реализовать метод "действуй" для кота, в котором он принимает решение
# что будет делать сегодня
# Человеку и коту надо вместе прожить 365 дней.
# Реализуем модель человека.
# Человек может есть, работать, играть, ходить в магазин.
# У человека есть степень сытости, немного еды и денег.
# Если сытость < 0 единиц, человек умирает.
# Человеку надо прожить 365 дней.
# """
from random import randint

from termcolor import cprint


class Cat:

    def __init__(self, name='Мурзик'):
        self.name = name
        self.satiety = 50
        self.house = None

    def __str__(self):
        return 'Кот {} - сытость {}'.format(
            self.name, self.satiety,
        )

    def eat(self):
        if self.house.cats_food >= 10:
            cprint('Кот {} поел'.format(self.name), color='yellow')
            self.satiety += 20
            self.house.cats_food -= 10
        else:
            cprint('{} пытался поесть, но нет еды'.format(self.name), color='red')

    def sleep(self):
        cprint('Кот {} спит'.format(self.name), color='green')
        self.satiety -= 10

    def tear_wallpaper(self):
        cprint('Кот {} дерет обои'.format(self.name), color='red')
        self.satiety -= 10
        self.house.mud += 5

    def act(self):
        if self.satiety <= 0:
            cprint('Кот {} умер...'.format(self.name), color='cyan')
            self.house.cats.pop(0)
            return
        dice = randint(1, 3)
        if self.satiety < 20:
            self.eat()
        elif dice == 2:
            self.sleep()
        else:
            self.tear_wallpaper()


class Man:

    def __init__(self, name):
        self.name = name
        self.fullness = 50
        self.house = None

    def __str__(self):
        return 'Я - {}, сытость {}, дом {}'.format(
            self.name, self.fullness, self.house
        )

    def eat(self):
        if self.house.food >= 10:
            cprint('{} поел'.format(self.name), color='yellow')
            self.fullness += 10
            self.house.food -= 10
        else:
            cprint('{} нет еды'.format(self.name), color='red')
            self.shopping()

    def work(self):
        cprint('{} сходил на работу'.format(self.name), color='blue')
        self.house.money += 150
        self.fullness -= 10

    # Названия функций и методов нужно записывать строчными буквами.
    def watch_mtv(self):
        cprint('{} смотрел MTV целый день'.format(self.name), color='green')
        self.fullness -= 10

    def shopping(self):
        if self.house.money >= 50:
            cprint('{} сходил в магазин за едой'.format(self.name), color='magenta')
            self.house.money -= 50
            self.house.food += 50
        else:
            cprint('{} деньги кончились!'.format(self.name), color='red')

    def go_to_the_house(self, house):
        self.house = house
        self.fullness -= 10
        cprint('{} Вьехал в дом'.format(self.name), color='cyan')

    def cat_to_the_house(self, cat_name='Мурзик'):
        kotik = Cat(cat_name)
        kotik.house = self.house
        self.house.cats.append(kotik)
        cprint('{} Подобрал кота {} в дом'.format(self.name, kotik.name), color='cyan')

    def buy_cat_eat(self):
        if self.house.money >= 50:
            cprint('{} купил кошачью еду'.format(self.name), color='magenta')
            self.house.money -= 50
            self.house.cats_food += 50
        else:
            cprint('{} деньги кончились!'.format(self.name), color='red')

    def clean_the_house(self):
        cprint('{} убрался в доме'.format(self.name), color='grey')
        self.house.mud -= max(100, self.house.mud)
        self.fullness -= 20

    def act(self):
        if self.fullness <= 0:
            cprint('{} умер...'.format(self.name), color='red')
            return
        dice = randint(1, 5)
        if self.fullness < 40:
            self.eat()
        elif self.house.money < 50:
            self.work()
        elif self.house.cats_food < 20:
            self.buy_cat_eat()
        elif self.house.food < 10:
            self.shopping()
        elif self.house.mud >= 100:
            self.clean_the_house()
        elif dice == 1:
            self.work()
        elif dice == 2:
            self.eat()
        #        elif dice == 3:
        #            self.cat_to_the_house()
        else:
            self.watch_mtv()


class House:

    def __init__(self):
        self.food = 50
        self.money = 0
        self.mud = 0
        self.cats_food = 0
        self.cats = []

    def __str__(self):
        if len(self.cats) == 0:
            scats = 'Нет котов в доме'
        else:
            scats = self.cats[0]
        return 'В доме еды осталось {}, денег осталось {}, грязи накопилось {}, кошачьей еды осталось {}, коты {}'. \
            format(self.food, self.money, self.mud, self.cats_food, scats)


my_sweet_home = House()
man1 = Man('Леха')
man1.go_to_the_house(house=my_sweet_home)
man1.cat_to_the_house()
man1.cat_to_the_house("Пушок")
man1.cat_to_the_house("Васька")
# ЛИШНИЙ КОТ
# man1.cat_to_the_house("кот4")

for day in range(1, 366):
    print('================ день {} =================='.format(day))
    man1.act()
    if len(man1.house.cats) > 0:
        for cat in man1.house.cats:
            cat.act()
    print('--- в конце дня ---')
    print(man1)
    if not (man1.fullness > 0 or len(man1.house.cats) > 0):
        break
    print()

    # print(my_sweet_home)

# Усложненное задание (делать по желанию)
# Создать несколько (2-3) котов и подселить их в дом к человеку.
# Им всем вместе так же надо прожить 365 дней.

# (Можно определить критическое количество котов, которое может прокормить человек...)

# Зачёт!
