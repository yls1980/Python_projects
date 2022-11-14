# -*- coding: utf-8 -*-

# Создать прототип игры Алхимия: при соединении двух элементов получается новый.
# Реализовать следующие элементы: Вода, Воздух, Огонь, Земля, Шторм, Пар, Грязь, Молния, Пыль, Лава.
# Каждый элемент организовать как отдельный класс.
# Таблица преобразований:
#   Вода + Воздух = Шторм
#   Вода + Огонь = Пар
#   Вода + Земля = Грязь
#   Воздух + Огонь = Молния
#   Воздух + Земля = Пыль
#   Огонь + Земля = Лава

# Сложение элементов реализовывать через __add__
# Если результат не определен - то возвращать None
# Вывод элемента на консоль реализовывать через __str__
#
# Примеры преобразований:
#   print(Water(), '+', Air(), '=', Water() + Air())
#   print(Fire(), '+', Air(), '=', Fire() + Air())


class Water:
    res = None

    def __init__(self):
        self.name = 'Вода'

    def __add__(self, element):
        #  Используйте функцию isinstance, которая позволяет
        # Не очень понятно, для каких целей использовать тут данную функцию?
        #  определить является ли объект экземпляром определённого класса.
        #  list1 = [1, 2, 3]
        #  isinstance(list1, list) вернёт True
        #  isinstance(list1, str) вернёт False
        #  Функция isinstance позволяет просто и надёжно проверить,
        #  что объект является экземпляром определённого класса.

        #  Нужно либо реализовать проверки в отдельных классах.
        #  В методе __add__ класса Воды нужно проверять что к воде
        #  проибавляется Воздух, Огонь или Земля и возвращать
        #  соответствующий результат. Не нужно оставлять функцию
        #  alhimiya. В ней большое количество проверок выполняемых
        #  в цикле. Надеяться на свойства (переменные)
        #  класса менее надёжно, чем проверять принадлежность к
        #  определённому классу.
        if isinstance(element, Air):
            return Storm()
        elif isinstance(element, Fire):
            return Steam()
        elif isinstance(element, Earth):
            return Dirt()
        else:
            return self

    def __str__(self):
        return self.name


class Air:
    def __init__(self):
        self.name = 'Воздух'

    def __add__(self, element):
        if isinstance(element, Water):
            return Storm()
        elif isinstance(element, Fire):
            return Lightning()
        elif isinstance(element, Earth):
            return Dust()
        else:
            return self

    def __str__(self):
        return self.name


class Fire:
    def __init__(self):
        self.name = 'Огонь'

    def __add__(self, element):
        if isinstance(element, Water):
            return Steam()
        elif isinstance(element, Air):
            return Lightning()
        else:
            return self

    def __str__(self):
        return self.name


class Earth:
    def __init__(self):
        self.name = 'Земля'

    def __add__(self, element):
        if isinstance(element, Water):
            return Dirt()
        if isinstance(element, Air):
            return Dust()
        else:
            return self

    def __str__(self):
        return self.name


class Storm:
    def __init__(self):
        self.name = 'Шторм'

    def __add__(self, element):
        return self

    def __str__(self):
        return self.name


class Steam:
    def __init__(self):
        self.name = 'Пар'

    def __add__(self, element):
        return self

    def __str__(self):
        return self.name


class Dirt:
    def __init__(self):
        self.name = 'Грязь'

    def __add__(self, element):
        return self

    def __str__(self):
        return self.name


class Lightning:
    def __init__(self):
        self.name = 'Молния'

    def __add__(self, element):
        return self

    def __str__(self):
        return self.name


class Dust:
    def __init__(self):
        self.name = 'Пыль'

    def __add__(self, element):
        return self

    def __str__(self):
        return self.name


class Lava:
    def __init__(self):
        self.name = 'Лава'

    def __add__(self, element):
        return self

    def __str__(self):
        return self.name


"""rules = [('Вода', 'Воздух', 'Шторм'),
         ('Вода', 'Огонь', 'Пар'),
         ('Вода', 'Земля', 'Грязь'),
         ('Воздух', 'Огонь', 'Молния'),
         ('Воздух', 'Земля', 'Пыль'),
         ('Огонь', 'Земля', 'Лава')]


def alhimiya(first, second):
    Storm1 = Storm()
    Steam1 = Steam()
    Dirt1 = Dirt()
    Lightning1 = Lightning()
    Dust1 = Dust()
    Lava1 = Lava()
    for a, b, c in rules:
        if (first == a and second == b) or (first == b and second == a):
            if Storm1.name == c:
                return Storm1
            elif Steam1.name == c:
                return Steam1
            elif Dirt1.name == c:
                return Dirt1
            elif Lightning1.name == c:
                return Lightning1
            elif Dust1.name == c:
                return Dust1
            elif Lava1.name == c:
                return Lava1"""


print(Air(), '+', Water(), '=', Air() + Water())
print(Fire(), '+', Air(), '=', Fire() + Air())
print(Dirt(), '+', Air(), '=', Dirt() + Air())

# Усложненное задание (делать по желанию)
# Добавить еще элемент в игру.
# Придумать что будет при сложении существующих элементов с новым.
# Исправьте оформление кода в задании.

# Зачёт!
