# -*- coding: utf-8 -*-

# Создать модуль my_burger. В нем определить функции добавления инградиентов:
#  - булочки
#  - котлеты
#  - огурчика
#  - помидорчика
#  - майонеза
#  - сыра
# В каждой функции выводить на консоль что-то вроде "А теперь добавим ..."

# В этом модуле создать рецепт двойного чизбургера (https://goo.gl/zA3goZ)
# с помощью фукций из my_burger и вывести на консоль.

# Создать рецепт своего бургера, по вашему вкусу.
# Если не хватает инградиентов - создать соответствующие функции в модуле my_burger

from lesson_005.results import my_burger

my_burger.bul()
my_burger.kot()
my_burger.gs()
my_burger.luk()
my_burger.ogur()
my_burger.chees()
my_burger.pgril()

print("Мой бургер:")
my_burger.bul()
for i in range(1, 7):
    my_burger.kot()
my_burger.luk()
my_burger.bul()

# Исправьте замечания среды разработки по оформлению кода
#  в модуле my_burger.

# Зачёт!
