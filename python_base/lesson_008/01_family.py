# -*- coding: utf-8 -*-

from termcolor import cprint
from random import randint


# Часть первая
#
# Создать модель жизни небольшой семьи.
#
# Каждый день участники жизни могут делать только одно действие.
# Все вместе они должны прожить год и не умереть.
#
# Муж может:
#   есть,
#   играть в WoT,
#   ходить на работу,
# Жена может:
#   есть,
#   покупать продукты,
#   покупать шубу,
#   убираться в доме,

# Все они живут в одном доме, дом характеризуется:
#   кол-во денег в тумбочке (в начале - 100)
#   кол-во еды в холодильнике (в начале - 50)
#   кол-во грязи (в начале - 0)
#
# У людей есть имя, степень сытости (в начале - 30) и степень счастья (в начале - 100).
#
# Любое действие, кроме "есть", приводит к уменьшению степени сытости на 10 пунктов
# Кушают взрослые максимум по 30 единиц еды, степень сытости растет на 1 пункт за 1 пункт еды.
# Степень сытости не должна падать ниже 0, иначе чел умрет от голода.
#
# Деньги в тумбочку добавляет муж, после работы - 150 единиц за раз.
# Еда стоит 10 денег 10 единиц еды. Шуба стоит 350 единиц.
#
# Грязь добавляется каждый день по 5 пунктов, за одну уборку жена может убирать до 100 единиц грязи.
# Если в доме грязи больше 90 - у людей падает степень счастья каждый день на 10 пунктов,
# Степень счастья растет: у мужа от игры в WoT (на 20), у жены от покупки шубы (на 60, но шуба дорогая)
# Степень счастья не должна падать ниже 10, иначе чел умирает от депрессии.
#
# Подвести итоги жизни за год: сколько было заработано денег, сколько сьедено еды, сколько куплено шуб.


class House:
    house_money = 0
    eat_in_cold = 0
    dust_count = 0
    eat_for_cat = 0
    all_send_money = 0
    all_send_eat = 0
    all_pay_coat = 0

    def __init__(self):
        self.house_money = 100
        self.eat_in_cold = 50
        self.eat_for_cat = 30

    def __str__(self):
        return 'деньги {}, еда в холодильнике {}, мусор {}'.format(self.house_money, self.eat_in_cold, self.dust_count)


class Man:
    satiety = 30
    degree_of_happiness = 100
    name = ''
    house = None
    isChild = False

    def __init__(self, name):
        self.name = name
        self.house = home

    def __str__(self):
        return '{} сытость {} и счастье {}'.format(self.name, self.satiety, self.degree_of_happiness)

    def eat(self, grub):
        self.satiety += grub
        self.house.eat_in_cold -= grub
        self.house.all_send_eat += grub
        print(self.name + " поел")

    def act(self):
        if self.degree_of_happiness < 10:
            return self.name + " умер от депрессии"
        else:
            if self.house.dust_count > 90:
                self.degree_of_happiness -= 10
        if self.satiety < 10:
            return self.name + " умер от голода"
        else:
            self.satiety -= 10
        return self.satiety, self.degree_of_happiness

    def buzz(self, happiness=10):
        self.degree_of_happiness += happiness

    def pet_cat(self):
        self.degree_of_happiness += 5
        print(self.name + " гладил кота")


class Husband(Man):

    #  Вы не меняете поведение родительского метода __init__
    #  не нужно его переопределять.
    #  Вы не меняете поведение родительского метода,
    #  не нужно его переопределять.

    def eat(self, **kwargs):
        grub = randint(10, 30)
        super().eat(grub)

    def work(self):
        self.house.house_money += 150
        print(self.name + " работал")

    def gaming(self):
        self.buzz(20)
        print(self.name + " играл")

    def act(self):
        # рост грязи
        self.house.dust_count += 2
        if self.house.house_money < 150:
            self.work()
        elif self.satiety < 20:
            self.eat()
            return
        elif self.degree_of_happiness < 20:
            self.gaming()
        else:
            self.gaming()
        super().act()


class Wife(Man):

    #  Вы не меняете поведение родительского метода __init__
    #  не нужно его переопределять.

    #  Вы не меняете поведение родительского метода,
    #  не нужно его переопределять.
    def act(self):
        self.house.dust_count += 3
        if self.satiety < 20:
            self.eat()
            return
        elif self.house.eat_in_cold < 100:
            self.shopping()
        elif self.house.dust_count > 100:
            self.clean_house()
        elif self.degree_of_happiness < 20:
            self.buy_fur_coat()
        else:
            if self.house.house_money > 400:
                self.buy_fur_coat()
            else:
                rnd = randint(1, 3)
                if rnd == 1:
                    self.shopping()
                elif rnd == 2:
                    self.clean_house()
                elif rnd == 3:
                    self.pet_cat()
                else:
                    self.eat()
                    return ()
        super().act()

    def eat(self, **kwargs):
        grub = randint(10, 30)
        super().eat(grub)

    def shopping(self):
        if self.house.house_money > 10:
            eat = randint(10, self.house.house_money)
            self.house.eat_in_cold += eat
            self.house.house_money -= eat
            self.house.all_send_money += eat
            if self.house.eat_for_cat < 15:
                eatcat = randint(10, 20)
                self.house.eat_for_cat += eatcat
                self.house.house_money -= eatcat
                self.house.all_send_money += eatcat
        print(self.name + " Ходила в магазин")

    def buy_fur_coat(self):
        self.house.house_money -= 350
        self.house.all_send_money += 350
        self.house.all_pay_coat += 1
        self.buzz(60)
        print(self.name + " Купила шубу")

    def clean_house(self):
        if self.house.dust_count >= 100:
            self.house.dust_count -= 100
            print(self.name + " убралась")
        else:
            print(self.name + " хотела убраться, но мусора нету")


#  После исправления замечаний переходите ко второй части задания.
# сделал после реализации первой части - отдать на проверку учителю

# Часть вторая
#
# После подтверждения учителем первой части надо
# отщепить ветку develop и в ней начать добавлять котов в модель семьи
#
# Кот может:
#   есть,
#   спать,
#   драть обои
#
# Люди могут:
#   гладить кота (растет степень счастья на 5 пунктов)
#
# В доме добавляется:
#   еда для кота (в начале - 30)
#
# У кота есть имя и степень сытости (в начале - 30)
# Любое действие кота, кроме "есть", приводит к уменьшению степени сытости на 10 пунктов
# Еда для кота покупается за деньги: за 10 денег 10 еды.
# Кушает кот максимум по 10 единиц еды, степень сытости растет на 2 пункта за 1 пункт еды.
# Степень сытости не должна падать ниже 0, иначе кот умрет от голода.
#
# Если кот дерет обои, то грязи становится больше на 5 пунктов


class Cat:
    name = ''
    satiety = 30
    house = None

    def __init__(self, name):
        self.name = name
        self.house = home

    def __str__(self):
        return '{} сытость {}'.format(self.name, self.satiety)

    def eat(self):
        grub = randint(1, 10)
        self.satiety += 2 * grub
        print("Кот " + self.name + " ест")

    # Нужно реализовать метод sleep.
    def sleep(self):
        print("Кот " + self.name + " спит")

    def soil(self):
        print("Кот " + self.name + " дерет обои")
        self.house.dust_count += 5

    def act(self):
        if self.satiety < 10:
            return 'Кот ' + self.name + " умер от голода"
        if self.satiety < 20:
            self.eat()
            return
        else:
            buf = randint(1, 2)
            if buf == 1:
                self.sleep()
            else:
                self.soil()
        self.satiety -= 10


# Часть вторая бис
#
# После реализации первой части надо в ветке мастер продолжить работу над семьей - добавить ребенка
#
# Ребенок может:
#   есть,
#   спать,
#
# отличия от взрослых - кушает максимум 10 единиц еды,
# степень счастья  - не меняется, всегда ==100 ;)

class Child(Man):

    #  isChild нужно объявить как переменную класса,
    #  аналогично классу Man. Метод __init__ нужно будет
    #  убрать. Сейчас из-за него задание выбрасывает ошибку.

    def act(self):
        if self.satiety < 20:
            self.eat(0)
        else:
            self.sleep()

    # В родительском методе есть аргумент grub.
    #  При переопределении методов не нужно менять
    #  количество аргументов метода.
    def eat(self, grub):
        super().eat(grub=randint(1, 10))

    def sleep(self):
        super().act()
        print(self.name + " спит")


#  после реализации второй части - отдать на проверку учителем две ветки


# ####################################################### Часть третья
#
# после подтверждения учителем второй части (обоих веток)
# влить в мастер все коммиты из ветки develop и разрешить все конфликты
# отправить на проверку учителем.


home = House()
serge = Husband(name='Сережа')
masha = Wife(name='Маша')
kolya = Child(name='Коля')
kolya.isChild = True
murzik = Cat(name='Мурзик')

for day in range(365):
    cprint('================== День {} =================='.format(day), color='red')
    serge.act()
    masha.act()
    kolya.act()
    murzik.act()
    cprint(serge, color='cyan')
    cprint(masha, color='cyan')
    cprint(kolya, color='cyan')
    cprint(murzik, color='cyan')

cprint('Съедено еды {}'.format(home.all_send_eat), color='blue')
cprint('Потрачено денег {}'.format(home.all_send_money), color='blue')
cprint('Куплено шуб {}'.format(home.all_pay_coat), color='blue')

# Усложненное задание (делать по желанию)
#
# Сделать из семьи любителей котов - пусть котов будет 3, или даже 5-10.
# Коты должны выжить вместе с семьей!
#
# Определить максимальное число котов, которое может прокормить эта семья при значениях зарплаты от 50 до 400.
# Для сглаживание случайностей моделирование за год делать 3 раза, если 2 из 3х выжили - считаем что выжили.
#
# Дополнительно вносить некий хаос в жизнь семьи
# - N раз в год вдруг пропадает половина еды из холодильника (коты?)
# - K раз в год пропадает половина денег из тумбочки (муж? жена? коты?!?!)
# Промоделировать - как часто могут случаться фейлы что бы это не повлияло на жизнь героев?
#   (N от 1 до 5, K от 1 до 5 - нужно вычислит максимумы N и K при котором семья гарантированно выживает)
#
# в итоге должен получится приблизительно такой код экспериментов
# for food_incidents in range(6):
#   for money_incidents in range(6):
#       life = Simulation(money_incidents, food_incidents)
#       for salary in range(50, 401, 50):
#           max_cats = life.experiment(salary)
#           print(f'При зарплате {salary} максимально можно прокормить {max_cats} котов')

# Зачёт!
