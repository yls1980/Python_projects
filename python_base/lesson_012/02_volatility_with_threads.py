# -*- coding: utf-8 -*-


# Задача: вычислить 3 тикера с максимальной и 3 тикера с минимальной волатильностью в МНОГОПОТОЧНОМ стиле
#
# Бумаги с нулевой волатильностью вывести отдельно.
# Результаты вывести на консоль в виде:
#   Максимальная волатильность:
#       ТИКЕР1 - ХХХ.ХХ %
#       ТИКЕР2 - ХХХ.ХХ %
#       ТИКЕР3 - ХХХ.ХХ %
#   Минимальная волатильность:
#       ТИКЕР4 - ХХХ.ХХ %
#       ТИКЕР5 - ХХХ.ХХ %
#       ТИКЕР6 - ХХХ.ХХ %
#   Нулевая волатильность:
#       ТИКЕР7, ТИКЕР8, ТИКЕР9, ТИКЕР10, ТИКЕР11, ТИКЕР12
# Волатильности указывать в порядке убывания. Тикеры с нулевой волатильностью упорядочить по имени.
#
#  Внимание! это задание можно выполнять только после зачета lesson_012/01_volatility.py !!!

#  тут ваш код в многопоточном стиле

# -*- coding: utf-8 -*-


import csv
import os
from collections import defaultdict
import operator
from threading import Thread


def print_volat(pvolatility, bsort=True):
    zerovl = []
    show_vols = []
    i = 0
    for name, val in pvolatility:
        if val == 0:
            zerovl.append(name)
        elif i < 3:
            i += 1
            show_vols.append((name, val))
        else:
            break

    show_vols = sorted(show_vols, reverse=bsort, key=lambda item: item[1])
    for x, y in show_vols:
        print(f'{x} - {round(y, 2)} %')
    if len(zerovl) != 0:
        zerovl = sorted(zerovl)
        print("Нулевая волатильность:")
        print(', '.join(zerovl))


def select_volatility(volatilitys):
    vl = sorted(volatilitys.items(), key=operator.itemgetter(1), reverse=True)
    print("Максимальная волатильность:")
    print_volat(vl)
    vl = sorted(volatilitys.items(), key=operator.itemgetter(1))
    print("Минимальная волатильность:")
    print_volat(vl)


class Trader(Thread):

    def __init__(self, file_name, volatilitys, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file_name = file_name
        self.volatilitys = volatilitys

    def read_file(self):
        if not os.path.isfile(self.file_name):
            print(f'Файл {self.file_name} не найден')
            return
        with open(self.file_name, 'r', encoding='cp1251') as file_f:
            try:
                line = file_f.readline()[:-1]
                field_names = line.split(',')
                datas = csv.DictReader(file_f, fieldnames=field_names, delimiter=',')
                #  Для поиска максимума и минимума не нужно сохранять всё значения.
                #  Значений может быть очень много, и для их хранения потребуется дополнительная память.
                #  Задайте начальные значения минимума и максимума и меняйте их, если в одной из строк
                #  встретится значение больше или меньше заданного. Для начального значения лучше
                #  всего взять цену из первой строки с данными.
                f_row = next(datas)
                sname = f_row.get('SECID')
                max_sum = float(f_row['PRICE']) * int(f_row['QUANTITY'])
                min_sum = max_sum
                count_tickets = 1
                for vals in datas:
                    # Проверку на сравнение с None лучше выполнять с использованием
                    #  оператора is: sname is None
                    sum_s = float(vals['PRICE']) * int(vals['QUANTITY'])
                    if sum_s > max_sum:
                        max_sum = sum_s
                    if sum_s < min_sum:
                        min_sum = sum_s
                    count_tickets += 1

                if count_tickets == 0:
                    half_sum = 0
                else:
                    half_sum = (max_sum + min_sum) / count_tickets
                volatility = ((max_sum - min_sum) / half_sum) * 100
                self.volatilitys[sname] += volatility
                #print(f'Проверил файл {self.file_name}: {sname} === {volatility}')
            except Exception as exc:
                print(f'Ошибка в файле {self.file_name}  - {exc}')

    def run(self):
        self.read_file()

# Переменные должны быть записаны строчными буквами.
#  Не забывайте про оформление кода.
spath = 'trades'
global_volatilitys = defaultdict(float)
files = [Trader(file_name=os.path.join(spath, file),volatilitys=global_volatilitys) for file in os.listdir(spath)]
for trade_file in files:
    trade_file.start()

for trade_file in files:
    trade_file.join()

# Вывод на экран
select_volatility(global_volatilitys)

# Зачёт!
