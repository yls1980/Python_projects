# -*- coding: utf-8 -*-


# Описание предметной области:
#
# При торгах на бирже совершаются сделки - один купил, второй продал.
# Покупают и продают ценные бумаги (акции, облигации, фьючерсы, етс). Ценные бумаги - это по сути долговые расписки.
# Ценные бумаги выпускаются партиями, от десятка до несколько миллионов штук.
# Каждая такая партия (выпуск) имеет свой торговый код на бирже - тикер - https://goo.gl/MJQ5Lq
# Все бумаги из этой партии (выпуска) одинаковы в цене, поэтому говорят о цене одной бумаги.
# У разных выпусков бумаг - разные цены, которые могут отличаться в сотни и тысячи раз.
# Каждая биржевая сделка характеризуется:
#   тикер ценнной бумаги
#   время сделки
#   цена сделки
#   обьем сделки (сколько ценных бумаг было куплено)
#
# В ходе торгов цены сделок могут со временем расти и понижаться. Величина изменения цен называтея волатильностью.
# Например, если бумага №1 торговалась с ценами 11, 11, 12, 11, 12, 11, 11, 11 - то она мало волатильна.
# А если у бумаги №2 цены сделок были: 20, 15, 23, 56, 100, 50, 3, 10 - то такая бумага имеет большую волатильность.
# Волатильность можно считать разными способами, мы будем считать сильно упрощенным способом -
# отклонение в процентах от полусуммы крайних значений цены за торговую сессию:
#   полусумма = (максимальная цена + минимальная цена) / 2
#   волатильность = ((максимальная цена - минимальная цена) / полусумма) * 100%
# Например для бумаги №1:
#   half_sum = (12 + 11) / 2 = 11.5
#   volatility = ((12 - 11) / half_sum) * 100 = 8.7%
# Для бумаги №2:
#   half_sum = (100 + 3) / 2 = 51.5
#   volatility = ((100 - 3) / half_sum) * 100 = 188.34%
#
# В реальности волатильность рассчитывается так: https://goo.gl/VJNmmY
#
# Задача: вычислить 3 тикера с максимальной и 3 тикера с минимальной волатильностью.
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
# Подготовка исходных данных
# 1. Скачать файл https://drive.google.com/file/d/1l5sia-9c-t91iIPiGyBc1s9mQ8RgTNqb/view?usp=sharing
#       (обратите внимание на значок скачивания в правом верхнем углу,
#       см https://drive.google.com/file/d/1M6mW1jI2RdZhdSCEmlbFi5eoAXOR3u6G/view?usp=sharing)
# 2. Раззиповать средствами операционной системы содержимое архива
#       в папку python_base/lesson_012/trades
# 3. В каждом файле в папке trades содержится данные по сделакам по одному тикеру, разделенные запятыми.
#   Первая строка - название колонок:
#       SECID - тикер
#       TRADETIME - время сделки
#       PRICE - цена сделки
#       QUANTITY - количество бумаг в этой сделке
#   Все последующие строки в файле - данные о сделках
#
# Подсказка: нужно последовательно открывать каждый файл, вычитывать данные, высчитывать волатильность и запоминать.
# Вывод на консоль можно сделать только после обработки всех файлов.
#
# Для плавного перехода к мультипоточности, код оформить в обьектном стиле, используя следующий каркас
#

# написать код в однопоточном/однопроцессорном стиле
import csv
import os
from collections import defaultdict
import operator


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
        print("Нулевая волатильность:")
        print(', '.join(zerovl))


class Trader:
    file_name = ''
    volatilitys = defaultdict(float)
    total_ticks = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
                self.total_ticks += 1
                # print (sname, max_sum, min_sum, count_tickets, half_sum, volatility)
            except Exception as exc:
                print(f'Ошибка в файле {self.file_name}  - {exc}')

    def select_volatility(self):
        # пчетаем по отсортированным волатильностям(сначала по возрастанию, потом по убыванию)
        # Вместо lambda рекомендуется использовать operator.itemgetter
        #  В большинстве случаев он работает быстрее и надёжнее, чем lambda.
        # vl = sorted(self.volatilitys.items(), reverse=True, key=lambda item: item[1])
        vl = sorted(self.volatilitys.items(), key=operator.itemgetter(1), reverse=True)
        print("Максимальная волатильность:")
        print_volat(vl)
        # vl = sorted(self.volatilitys.items(), key=lambda item: item[1])
        vl = sorted(self.volatilitys.items(), key=operator.itemgetter(1))
        print("Минимальная волатильность:")
        print_volat(vl)

    def run(self):
        self.read_file()


# Переменные должны быть записаны строчными буквами.
#  Не забывайте про оформление кода.
v_trader = Trader()
spath = 'trades'
files = os.listdir(spath)
for file in files:
    v_trader.file_name = os.path.join(spath, file)
    v_trader.run()
v_trader.select_volatility()

# Переходите ко второму заданию.
