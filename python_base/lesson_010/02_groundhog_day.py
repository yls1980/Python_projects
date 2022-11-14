# -*- coding: utf-8 -*-
import random


# День сурка
#
# Напишите функцию one_day() которая возвращает количество кармы от 1 до 7
# и может выкидывать исключения:
# - IamGodError
# - DrunkError
# - CarCrashError
# - GluttonyError
# - DepressionError
# - SuicideError
# Одно из этих исключений выбрасывается с вероятностью 1 к 13 каждый день
#
# Функцию оберните в бесконечный цикл, выход из которого возможен только при накоплении
# кармы до уровня ENLIGHTENMENT_CARMA_LEVEL. Исключения обработать и записать в лог.
# При создании собственных исключений максимально использовать функциональность
# базовых встроенных исключений.

#  Для исключений, созданных в этом задании лучше сделать общий родительский класс,
#  например MainException, унаследованный от Exception, от которого нужно
#  наследовать остальные а в except перехватывать общее исключение.
#  Я не очень пойму, как потом в этом классе(MainException) перечислить все нижеследующие классы исключений
# Нужно все остальные исключения, созданные в задании наследовать от MainException,
#  например IamGodError(MainException)

#  В задании есть ошибки в оформлении, которые нужно исправить.

class MainException(Exception):
    value_exc = ''

    def __str__(self):
        return self.value_exc


class IamGodError(MainException):
    value_exc = "Я Бог"


class DrunkError(MainException):
    value_exc = 'Напился пьяный'


class CarCrashError(MainException):
    value_exc = 'Машина разбилась'


class GluttonyError(MainException):
    value_exc = 'Обожрался'


class DepressionError(MainException):
    value_exc = 'Депрессия'


class SuicideError(MainException):
    value_exc = 'Самоубийство'


ENLIGHTENMENT_CARMA_LEVEL = 777
excs = [IamGodError, DrunkError, CarCrashError, GluttonyError, DepressionError, SuicideError]


def one_day():
    karma = random.randint(1, 7)
    beda = random.randint(0, 5)
    #  Можно упростить код с условиями:
    #  Перечислить исключения в списке или кортеже, случайно выбирать один
    #  из элементов списка и вызывать полученное исключение.
    #  Сообщения можно сохранять в методах __str__ класов исключений.
    if random.randint(1, 13) == 5:
        raise excs[beda]
    else:
        # print (f"рост кармы на {karma}")
        return karma


res = 0
day = 0
file = open("groundhoc.log", "w")
while 1 == 1:
    try:
        day += 1
        res += one_day()
        print(f"день {res} - Общая карма {res}")

        if res >= ENLIGHTENMENT_CARMA_LEVEL:
            break
    #  Если сделать общий класс для всех ошибок, то
    #  будут перехватываться только исключения, созданные
    #  в задании.
    #  После того, как добавленные исключения станут наследниками
    #  класса MainException, нужно будет заменить Exception на MainException.
    except MainException as exc:
        file.write(f"день {res} - исключение {exc}\n")
        print(exc, "-карма не изменилась")
file.close()

# https://goo.gl/JnsDqu

# Зачёт!
