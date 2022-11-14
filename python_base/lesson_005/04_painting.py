# -*- coding: utf-8 -*-

# Создать пакет, в который скопировать функции отрисовки из предыдущего урока
#  - радуги
#  - стены
#  - дерева
#  - смайлика
#  - снежинок
# Функции по модулям разместить по тематике. Название пакета и модулей - по смыслу.
# Создать модуль с функцией отрисовки кирпичного дома с широким окном и крышей.

# С помощью созданного пакета нарисовать эпохальное полотно "Утро в деревне".
# На картине должны быть:
#  - кирпичный дом, в окошке - смайлик.
#  - слева от дома - сугроб (предположим что это ранняя весна)
#  - справа от дома - дерево (можно несколько)
#  - справа в небе - радуга, слева - солнце (весна же!)
# пример см. lesson_005/results/04_painting.jpg
# Приправить своей фантазией по вкусу (коты? коровы? люди? трактор? что придумается)
from lesson_005.results.vilage.fractal import derevo
from lesson_005.results.vilage.rainbow import raduga
from lesson_005.results.vilage.smile import smile
from lesson_005.results.vilage.snowfall import sneg
from lesson_005.results.vilage.sun import sun
from lesson_005.results.vilage.wall import house

sd = house()
sd = smile(540, 75, sd)
sd = raduga(sd, -200, -600, 530)
start_point = sd.get_point(900, 10)
derevo(start_point, 90, 90, sd.COLOR_YELLOW, 20, 30)
sd = sneg(sd)
sd = sun(sd, 150, 450)
sd.pause()

# Исправьте замечания среды разработки по оформлению кода
#  во всех модулях, что вы импортируете и используете в этом задании.

# Зачёт!
