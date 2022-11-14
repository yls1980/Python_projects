# -*- coding: utf-8 -*-

# Составить список всех живущих на районе и Вывести на консоль через запятую
# Формат вывода: На районе живут ...
# подсказка: для вывода элементов списка через запятую можно использовать функцию строки .join()
# https://docs.python.org/3/library/stdtypes.html#str.join
from lesson_005.district.central_street.house1 import room1 as r1, room2 as r2
from lesson_005.district.central_street.house2 import room1 as r3, room2 as r4
from lesson_005.district.soviet_street.house1 import room1 as r5, room2 as r6
from lesson_005.district.soviet_street.house2 import room1 as r7, room2 as r8

# Можно получить список жителей простым суммированием
#  импортируемых списков.
#  Это будет проще и бестрее, чем расширять список несколько раз.
# Сформируйте список жильцов и сохраните его в переменную и передавайте переменную в join.
livein_district = r1.folks+r2.folks+r3.folks+r4.folks+r5.folks+r6.folks+r7.folks+r8.folks
print('На районе живут ' + ','.join(livein_district))

# Зачёт!
