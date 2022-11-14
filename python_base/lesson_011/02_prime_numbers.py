# -*- coding: utf-8 -*-
from functools import reduce


# Есть функция генерации списка простых чисел


def get_prime_numbers(n):
    prime_numbers = []
    for _number in range(2, n + 1):
        for prime in prime_numbers:
            if _number % prime == 0:
                break
        else:
            prime_numbers.append(_number)
    return prime_numbers


# Часть 1
# На основе алгоритма get_prime_numbers создать класс итерируемых обьектов,
# который выдает последовательность простых чисел до n
#
# Распечатать все простые числа до 10000 в столбик


class PrimeNumbers:
    def __init__(self, n):
        #  Простые числа нужно генерировать в процессе итерации по
        #  объекту PrimeNumbers. Сейчас простые числа генерируются функцией
        #  и сохраняются в список. Нужно генерировать числа в процессе работы,
        #  т. е. в методе __next__ должен быть реализован алгоритм из функции
        #  get_prime_numbers.
        # self.s_numbers = get_prime_numbers(n)
        self.max = n
        self.prime_numbers = []
        self.last_prime = 2

    def __iter__(self):
        self.number = 1
        return self

    def __next__(self):
        for _number in range(self.last_prime, self.max + 1):
            if _number >= self.max:
                raise StopIteration
            for prime in self.prime_numbers:
                if _number % prime == 0:
                    break
            else:
                self.prime_numbers.append(_number)
                self.last_prime = _number
                return _number
        # while True:
        #  Число prime нужно проверять не всеми числами от
        #  двух, до round(self.number / 2) + 1, а по списку простых чисел,
        #  который нужно заполнять найденными простыми числами.
        # Не понятно, а где взять список простых чисел.
        # Я генерировал - список функцией get_prime_numbers, но это было не правильно
        #  Неправильно было сгенерировать все простые числа в методе __init__.
        #  Это существенно замедляло инициализацию класса PrimeNumbers.
        #  Нужно с небольшими изменениями реализовать алгоритм из функции get_prime_numbers
        #  в методе __next__
        #  Создавать список для простых чисел prime_numbers нужно в методе __init__
        #  В методе __next__ нужно во внешнем цикле проверять числа от последнего простого
        #  числа, найденного ранее до максимального. Во внутреннем цикле по списку найденных
        #  ранее простых чисел проверяется число на делимость.
        # Z lj
        # for prime in range(2, round(self.number / 2) + 1):
        #    if self.number % prime == 0:
        #        self.number += 1
        #        break
        # else:
        #    if self.number > self.max:
        #        raise StopIteration
        #    return self.number


prime_number_iterator = PrimeNumbers(n=10000)


# for number in prime_number_iterator:
#    print(number)
# try:
#  Исключение StopIteration не нужно перехватывать.
#  Оно нужно для остановки цикла по итерируемогу объекту.
# except StopIteration:
#    pass


#  после подтверждения части 1 преподователем, можно делать
# Часть 2
# Теперь нужно создать генератор, который выдает последовательность простых чисел до n
# Распечатать все простые числа до 10000 в столбик

# Вторую часть нужно будет доработать аналогично первой части.
def prime_numbers_generator(_number):
    prime_numbers = []
    for _number in range(2, _number + 1):
        for prime in prime_numbers:
            if _number % prime == 0:
                break
        else:
            prime_numbers.append(_number)
            yield _number


# for val in prime_numbers_generator(10000):
#    print(val)

# for number in prime_numbers_generator(n=10000):
#    print(number)

#  Переходите к третьей части задания.
# Часть 3
# Написать несколько функций-фильтров, которые выдает True, если число:
# 1) "счастливое" в обыденном пониманиии - сумма первых цифр равна сумме последних
#       Если число имеет нечетное число цифр (например 727 или 92083),
#       то для вычисления "счастливости" брать равное количество цифр с начала и конца:
#           727 -> 7(2)7 -> 7 == 7 -> True
#           92083 -> 92(0)83 -> 9+2 == 8+3 -> True
# 2) "палиндромное" - одинаково читающееся в обоих направлениях. Например 723327 и 101
# 3) придумать свою (https://clck.ru/GB5Fc в помощь)
#
# Подумать, как можно применить функции-фильтры к полученной последовательности простых чисел
# для получения, к примеру: простых счастливых чисел, простых палиндромных чисел,
# простых счастливых палиндромных чисел и так далее. Придумать не менее 2х способов.
#
# Подсказка: возможно, нужно будет добавить параметр в итератор/генератор.

def happiness_number1(_number):
    nlen = len(str(_number))
    substr_len = nlen // 2
    s1 = str(_number)[:substr_len:]
    s2 = str(_number)[-1 * substr_len::]
    ns1 = sum(map(int, s1))
    ns2 = sum(map(int, s2))
    return ns1 == ns2


def happiness_number2(_number):
    buf = str(_number)
    return buf == buf[::-1]


def happiness_number3(_number):
    # сумма чисел круглое число
    buf = str(_number)
    s1 = sum(map(int, buf))
    return s1 % 10 == 0


def happiness_number4(_number):
    # произведение четных и нечетных чисел
    s1 = list(map(int, str(_number)[1::2]))
    s2 = list(map(int, str(_number)[::2]))
    if len(s1) > 0 and len(s2) > 0:
        s1 = reduce(lambda x, y: x * y, s1)
        s2 = reduce(lambda x, y: x * y, s2)
    return s1 == s2 and s1 > 0


# Доработайте генератор так, чтобы он мог принимать несколько генераторов.
# Я не понимаю, какая конструкция должна получится? зачем в этот генератор добавлять еще генераторы? Не вижу направления решения.
def filter_(number_, filters):
    res = True
    if filters is None:
        return True
    else:
        for func in filters:
            res *= func(number_)
    return res


def prime_numbers_generator1(_number, filters):
    prime_numbers = []
    for _number in range(2, _number + 1):
        for prime in prime_numbers:
            if _number % prime == 0:
                break
        else:
            prime_numbers.append(_number)
            if filter_ is None or filter_(_number, filters):
                yield _number


def print_numbers(nсount, func=None):
    # Название переменных и аргументов функций должно быть записано строчными буквами.
    for val in prime_numbers_generator1(nсount, func):
        print(val)


#  Сделайте ещё один способ фильтрации простых чисел. Нужно изменить
#  генератор так, чтобы он принимал в аргумент список функция фильтров.
#  Возвращаться должно только такое число, для которого все функции фильтры выдадут True.
#  При отсутствии функций в аргументах генератор должен работать как обычно и возвращать
#  все простые числа.

# без фильтра
print_numbers(10000)
# применение фильтров
happiness_numbers = [happiness_number1, happiness_number2, happiness_number3]
print_numbers(10000, happiness_numbers)
happiness_numbers = [happiness_number2, happiness_number3, happiness_number4]
print_numbers(50000, happiness_numbers)

# Зачёт!
