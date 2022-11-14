# -*- coding: utf-8 -*-

# Имеется файл events.txt вида:
#
# [2018-05-17 01:55:52.665804] NOK
# [2018-05-17 01:56:23.665804] OK
# [2018-05-17 01:56:55.665804] OK
# [2018-05-17 01:57:16.665804] NOK
# [2018-05-17 01:57:58.665804] OK
# ...
#
# Напишите программу, которая считывает файл
# и выводит число событий NOK за каждую минуту в другой файл в формате
#
# [2018-05-17 01:57] 1234
# [2018-05-17 01:58] 4321
# ...
#
# Входные параметры: файл для анализа, файл результата
#
# Требования к коду: он должен быть готовым к расширению функциональности - делать сразу на классах.
# Для этого пригодится шаблон проектирование "Шаблонный метод"
#   см https://refactoring.guru/ru/design-patterns/template-method
#   и https://gitlab.skillbox.ru/vadim_shandrinov/python_base_snippets/snippets/4
import os
import collections


# Названия классов должны быть записаны в CamelCase.
class ReadLog:

    def __init__(self):
        self.log_file = 'events.txt'
        self.out_file = 'out_events.txt'
        self.buf = self.out_file
        self.mins = collections.defaultdict(int)

    def read_file(self, read_pos):
        self.mins.clear()
        if os.path.exists(self.log_file):
            rfile = open(self.log_file, 'r')
            for line in rfile:
                if line[-4:].strip() == 'NOK':
                    smin = line[1:read_pos]
                    # Здесь тоже лучше использовать
                    #  collections.defaultdict.
                    self.mins[smin] += 1
                    # if smin in self.mins:
                    #    self.mins[smin] += 1
                    # else:
                    #    self.mins[smin] = 1
            rfile.close()
        else:
            print(f'Файл {self.log_file} не существует')

    def write_file(self):
        wfile = open(self.out_file, 'w')
        for minute in self.mins:
            wfile.write(f'[{minute}] {self.mins[minute]}\n')
        print(f'Файл {os.path.join(os.path.abspath(os.getcwd()), self.out_file)} успешно сформирован')
        wfile.close()

    def calk(self, times, pref_out_file=''):
        if pref_out_file != '':
            self.out_file = pref_out_file + '_' + self.buf
        self.read_file(times)
        self.write_file()


class ReadLogHour(ReadLog):
    def calkl(self):
        self.calk(times=14, pref_out_file='hour')


class ReadLogMonth(ReadLog):
    def calkl(self):
        self.calk(times=8, pref_out_file='month')


class ReadLogYear(ReadLog):
    def calkl(self):
        self.calk(times=5, pref_out_file='year')


# Нужно фиксировать только те записи, в которых событие типа NOK.
#  Временные диапазоны, в которых нет таких событий нужно пропускать.

rl = ReadLog()
# минуты
rl.calk(times=17)

# Переходите ко второму этапу.
#  Постарайтесь минимизировать дублирование
#  кода.
# После зачета первого этапа нужно сделать группировку событий
#  - по часам

#  Попробуйте изменить задание так, чтобы каждый способ группировки
#  событий был реализован отдельным классом.

rh = ReadLogHour()
rh.calkl()
#  - по месяцуlesson_009/02_log_parser.py:98
rm = ReadLogMonth()
rm.calkl()
#  - по году
ry = ReadLogYear()
ry.calkl()

# Зачёт!
