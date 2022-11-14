#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Есть словарь кодов товаров

goods = {
    'Лампа': '12345',
    'Стол': '23456',
    'Диван': '34567',
    'Стул': '45678',
}

# Есть словарь списков количества товаров на складе.

store = {
    '12345': [
        {'quantity': 27, 'price': 42},
    ],
    '23456': [
        {'quantity': 22, 'price': 510},
        {'quantity': 32, 'price': 520},
    ],
    '34567': [
        {'quantity': 2, 'price': 1200},
        {'quantity': 1, 'price': 1150},
    ],
    '45678': [
        {'quantity': 50, 'price': 100},
        {'quantity': 12, 'price': 95},
        {'quantity': 43, 'price': 97},
    ],
}

# Рассчитать на какую сумму лежит каждого товара на складе
# например для ламп

# lamps_cost = store[goods['Лампа']][0]['quantity'] * store[goods['Лампа']][0]['price']
# или проще (/сложнее ?)
lamp_code = goods['Лампа']
lamps_item = store[lamp_code][0]
lamps_quantity = lamps_item['quantity']
lamps_price = lamps_item['price']
lamps_cost = lamps_quantity * lamps_price
# print('Лампа -', lamps_quantity, 'шт, стоимость', lamps_cost, 'руб')

# Вывести стоимость каждого вида товара на складе:
# один раз распечать сколько всего столов и их общая стоимость,
# один раз распечать сколько всего стульев и их общая стоимость,
#   и т.д. на складе
# Формат строки <товар> - <кол-во> шт, стоимость <общая стоимость> руб

# WARNING для знающих циклы: БЕЗ циклов. Да, с переменными; да, неэффективно; да, копипаста.
# Это заданина ручное вычисление - что бы потом понять как работают циклы и насколько с ними проще жить.

# лампы
item_name = list(goods.keys())[0]
item_code = goods[item_name]
item_data = store[item_code][0]
item_quantity = item_data['quantity']
item_price = item_data['price']
print('%s - %s шт, стоимость %s руб' % (item_name, item_quantity, item_quantity * item_price))

# столы
item_name = list(goods.keys())[1]
item_code = goods[item_name]
item_data = store[item_code][0]
item_quantity = item_data['quantity']
item_cost = item_quantity * item_data['price']
item_data = store[item_code][1]
item_quantity += item_data['quantity']
item_cost += item_data['quantity'] * item_data['price']
print('%s - %s шт, стоимость %s руб' % (item_name, item_quantity, item_cost))

# Диваны
item_name = list(goods.keys())[2]
item_code = goods[item_name]
item_data = store[item_code][0]
item_quantity = item_data['quantity']
item_cost = item_quantity * item_data['price']
item_data = store[item_code][1]
item_quantity += item_data['quantity']
item_cost += item_data['quantity'] * item_data['price']
print('%s - %s шт, стоимость %s руб' % (item_name, item_quantity, item_cost))

# Стулья
item_name = list(goods.keys())[3]
item_code = goods[item_name]
item_data = store[item_code][0]
item_quantity = item_data['quantity']
item_cost = item_quantity * item_data['price']
item_data = store[item_code][1]
item_quantity += item_data['quantity']
item_cost += item_data['quantity'] * item_data['price']
item_data = store[item_code][2]
item_quantity += item_data['quantity']
item_cost += item_data['quantity'] * item_data['price']
print('%s - %s шт, стоимость %s руб' % (item_name, item_quantity, item_cost))

##########################################################################################
# ВНИМАНИЕ! После того как __ВСЯ__ домашняя работа сделана и запушена на сервер,         #
# нужно зайти в ЛМС (LMS - Learning Management System ) по адресу http://go.skillbox.ru  #
# и оформить попытку сдачи ДЗ! Без этого ДЗ не будет проверяться!                        #
# Как оформить попытку сдачи смотрите видео - https://youtu.be/qVpN0L-C3LU               #
##########################################################################################

#  Нужно посчитать общие количество и стоимость товаров каждого типа:
#  столы, стулья, диваны, лампы. В словаре store может быть несколько товаров одного
#  типа с разным количеством и ценой.

#  Вы не совсем правильно считаете общую стоимость товара одного типа.
#  У вас общая цена умножается на общее количество.
#  Т. е. 3 стула по 10 и два стула по 15. В общем должны стоить 60.
#  По вашей способу получится 125.
#  Нужно посчитать стоимость для каждой разновидности одного товара (стул1, стул2, ...)
#  умножив количество на цену, а затем сложением получить общую стоимость товаров
#  одного типа.

# Исправил

# В примере с лампами было показано два варианта выполнения задания.
#  Ваша реализация больше похожа на первый способ.  На первый взгляд он кажется проще и компактней.
#  Давайте разберём, почему он не очень хорош, вернее очень нехорош:
#  - Такой код сложнее прочитать и понять. В процессе жизни программы её части гораздо чаще прочитывают, чем меняют.
#   Поэтому потратив немного больше времени при написании, вы, затем значительно сэкономите его поддерживая код
#  - Лёгкость изменения. Представьте себе, что в словаре goods поменялось название диван на софа. Посчитайте
#   сколько мест в программе вам нужно будет исправить?
#  - Большое количество скопированного кода. Довольно часто студенты ошибаются с индексами или названиями товаров
#   при копировании частей кода.
#  - Сложность отладки. Если программу расписать более подробно будет удобнее проверять полученные значения
#   в процессе отладки.
#  Нужно переписать программу по второму примеру, показанному для ламп.

# переписал. Я так понимаю что в реальности програма будет решаться через циклы
# с этой точки зрения код я думаю приемлем чтобы встроитьь его в итерации цикла.
# Сократил количество переменных, "что в словаре goods поменялось название диван на софа"

# Зачёт!
