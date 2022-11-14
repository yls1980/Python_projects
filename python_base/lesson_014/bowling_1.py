# -*- coding: utf-8 -*-
import re
from abc import ABCMeta, abstractmethod


def tryToInt(sstr):
    try:
        if sstr == 'X':
            return 10
        else:
            return int(sstr)
    except ValueError:
        return 0


class MyError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class EmptyEx(Exception):
    def __init__(self, info):
        self.message = f"Результат игры {info} не может быть пустым"
        super().__init__(self.message)


class ManyEx(Exception):
    def __init__(self, info):
        self.message = f"Результат игры {info} не может содержать так много символов"
        super().__init__(self.message)


class UnknownEx(Exception):
    def __init__(self, info, unknow):
        self.message = f"Результат игры {info} содержит неизвестные символы: {unknow}"
        super().__init__(self.message)


class CountFreymEx(Exception):
    def __init__(self, info, count_fr):
        self.message = f"Количество фреймов в игре: {info} должно быть 10, а сыграно {count_fr}"
        super().__init__(self.message)


class FirstSpeirEx(Exception):
    def __init__(self, info, frame):
        self.message = f"Во фрейме {frame} не может быть первый символ </>, игра: {info}"
        super().__init__(self.message)


class ManySkittlesEx(Exception):
    def __init__(self, info, frame):
        self.message = f"Во фрейме {frame} не может быть сбито больше 10 кеглей, игра: {info}"
        super().__init__(self.message)


class ThisNoStrikEx(Exception):
    def __init__(self, info):
        self.message = f"Не может быть страйк после первой попытки, игра: {info}"
        super().__init__(self.message)


class State(metaclass=ABCMeta):
    @abstractmethod
    def get_score(self):
        pass


class InLocal(State):
    def fstrike(self, calc):
        calc += 20
        return calc

    def fspare(self, calc, buf):
        calc -= buf
        calc += 15
        buf = 0
        return calc, buf

    def get_score(self):
        spare = 0  # число бросков во фрейме
        calc = 0  # Общее количество очков
        buf = 0  # буферная переменная
        count_freym = 0  # количество фреймов в игре
        calc_spare = 0  # количество сбитых кеглей во фрейме
        # подсчет бросков
        hit_number = -1
        # Цикл по строке результатов
        for hit in self.game_result:
            hit_number += 1
            if count_freym > 9:
                raise CountFreymEx(self.game_result, count_freym + 1)
            if hit == '/' and spare == 0:
                raise FirstSpeirEx(self.game_result, count_freym)
            if hit == 'X':
                if spare == 1:
                    raise ThisNoStrikEx(self.game_result)
                spare = 0
                count_freym += 1
                calc_spare = 0
                calc = self.fstrike(calc)
            elif hit == '/':
                if spare == 1:
                    spare = 0
                    count_freym += 1
                    calc, buf = self.fspare(calc, buf)
                    calc_spare = 0
                elif spare == 0:
                    raise FirstSpeirEx(self.game_result, count_freym)
            elif hit == '-':
                calc += 0
                if spare == 1:
                    count_freym += 1
                    calc_spare = 0
                spare += 1
            elif tryToInt(hit) > 0:
                if spare == 1:
                    count_freym += 1
                spare += 1
                buf = int(hit)
                calc_spare += buf
                if calc_spare <= 10:
                    calc += buf
                else:
                    raise ManySkittlesEx(self.game_result, count_freym)
            if spare > 1:
                spare = 0
                calc_spare = 0
        if count_freym < 10:
            raise CountFreymEx(self.game_result, count_freym)
        return calc


class InMarket(State):
    def fstrike(self, calc, hit_number):
        calc += 10
        snext = self.game_result[hit_number + 1:hit_number + 3]
        if snext.rfind('/') == 1:
            calc += 10
        else:
            calc += tryToInt(snext[0]) + tryToInt(snext[1])
        return calc

    def fspar(self, calc, calc_spare, hit_number):
        calc += 10 - calc_spare
        calc_spare = 0
        snext = self.game_result[hit_number + 1:hit_number + 2]
        calc += tryToInt(snext)
        return calc, calc_spare

    def get_score(self):
        spare = 0  # число бросков во фрейме
        calc = 0  # Общее количество очков
        buf = 0  # буферная переменная
        count_freym = 0  # количество фреймов в игре
        calc_spare = 0  # количество сбитых кеглей во фрейме
        # подсчет бросков
        hit_number = -1
        # Цикл по строке результатов
        for hit in self.game_result:
            hit_number += 1
            if count_freym > 9:
                raise CountFreymEx(self.game_result, count_freym + 1)
            if hit == '/' and spare == 0:
                raise FirstSpeirEx(self.game_result, count_freym)
            if hit == 'X':
                if spare == 1:
                    raise ThisNoStrikEx(self.game_result)
                spare = 0
                count_freym += 1
                calc_spare = 0
                calc = self.fstrike(calc, hit_number)

            elif hit == '/':
                if spare == 1:
                    spare = 0
                    count_freym += 1
                    calc, calc_spare = self.fspar(calc, calc_spare, hit_number)
                    calc_spare = 0
                elif spare == 0:
                    raise FirstSpeirEx(self.game_result, count_freym)
            elif hit == '-':
                calc += 0
                if spare == 1:
                    count_freym += 1
                    calc_spare = 0
                spare += 1
            elif tryToInt(hit) > 0:
                if spare == 1:
                    count_freym += 1
                spare += 1
                buf = int(hit)
                calc_spare += buf
                if calc_spare <= 10:
                    calc += buf
                else:
                    raise ManySkittlesEx(self.game_result, count_freym)
            if spare > 1:
                spare = 0
                calc_spare = 0
        if count_freym < 10:
            raise CountFreymEx(self.game_result, count_freym)
        return calc


class Bowling:
    def __init__(self, game_result, state=InLocal):
        self._state = state
        self.game_result = game_result
        if len(self.game_result) == 0:
            raise EmptyEx(self.game_result)
        elif len(self.game_result) > 20:
            raise ManyEx(self.game_result)
        elif len(re.findall(r"([^1-9\/X-])+", self.game_result)) > 0:
            unknow = ''.join(re.findall(r"([^1-9\/X-])+", self.game_result))
            raise UnknownEx(self.game_result, unknow)

    def change_state(self, state: State):
        self._state = state

    def set_market(self):
        self._state = InMarket

    def set_local(self):
        self._state = InLocal

    def get_score(self):
        run = getattr(self._state, 'get_score')
        return run(self)
