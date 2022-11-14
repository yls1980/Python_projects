# -*- coding: utf-8 -*-

# Есть файл с протоколом регистраций пользователей на сайте - registrations.txt
# Каждая строка содержит: ИМЯ ЕМЕЙЛ ВОЗРАСТ, разделенные пробелами
# Например:
# Василий test@test.ru 27
#
# Надо проверить данные из файла, для каждой строки:
# - присутсвуют все три поля
# - поле имени содержит только буквы
# - поле емейл содержит @ и .
# - поле возраст является числом от 10 до 99
#
# В результате проверки нужно сформировать два файла
# - registrations_good.log для правильных данных, записывать строки как есть
# - registrations_bad.log для ошибочных, записывать строку и вид ошибки.
#
# Для валидации строки данных написать метод, который может выкидывать исключения:
# - НЕ присутсвуют все три поля: ValueError
# - поле имени содержит НЕ только буквы: NotNameError (кастомное исключение)
# - поле емейл НЕ содержит @ и .(точку): NotEmailError (кастомное исключение)
# - поле возраст НЕ является числом от 10 до 99: ValueError
# Вызов метода обернуть в try-except.
import re


class NotNameError(Exception):
    pass


class NotEmailError(Exception):
    pass


def parse_str(pstr):
    llt_str = pstr.split(' ')
    # ptrn = "[^(a-z|а-я|A-Z|А-Я|Ё|ё)]"
    if len(llt_str) != 3:
        raise ValueError("НЕ присутсвуют все три поля")
    #  Проще и быстрее проверять строку используя встроенный метод
    #  строк str.isalpha, знакомый вам с прошлого урока.
    # elif re.search(ptrn, llt_str[0]) is not None:
    elif str(llt_str[0]).isalpha():
        raise NotNameError(f"поле имени содержит НЕ только буквы")
    elif len(re.findall(r"[(@|/.)]", llt_str[1])) < 2:
        raise NotEmailError(f"поле емейл НЕ содержит @ и .(точку)")
    elif re.search(r"\d\d", llt_str[2]) is None or not (10 <= int(llt_str[2]) <= 99):
        raise ValueError("поле возраст НЕ является числом от 10 до 99")


def wbstr(pstr1, pstr2):
    bstr = "В строке '{0}' {1}".format(pstr1, pstr2)
    fbad.write(bstr + '\n')
    print(bstr)


#  Можно открыть сразу несколько файлов в
#  одном менеджере контеста.
#  with open('file1', 'w') as file1, open('file2', 'w') as file2:
with open('registrations.txt', 'r') as file, open('registrations_good.log', 'w') as fgood, open('registrations_bad.log',
                                                                                                'w') as fbad:
    for line in file:
        try:
            lstr = line.replace('\n', '')
            parse_str(lstr)
            fgood.write(lstr + '\n')
        except Exception as exc:
            wbstr(lstr, exc)

# Зачёт!
