# -*- coding: utf-8 -*-

from random import shuffle

import simple_draw as sd

# На основе кода из практической части реализовать снегопад:
# - создать списки данных для отрисовки N снежинок
# - нарисовать падение этих N снежинок
# - создать список рандомных длинн лучей снежинок (от 10 до 100) и пусть все снежинки будут разные

N = 20

# Пригодятся функции
# sd.get_point()
# sd.snowflake()
# sd.sleep()
# sd.random_number()
# sd.user_want_exit()
snowflakes = []
for i in range(1, 25):
    x = sd.random_number(1, 600)
    y = sd.random_number(1, 600)
    snowflakes.append([x, y, sd.random_number(10, 50), sd.get_point(x, y)])
# номера снежинок
ind = [i for i in range(len(snowflakes))]

while True:
    n = 0
    sd.start_drawing()
    shuffle(ind)
    for n in ind:
        x, y, s, old_pos = snowflakes[n]
        point = old_pos
        if y < s:
            y = sd.random_number(1, 600)
        else:
            sd.snowflake(center=point, length=s, color=sd.background_color)
            y -= sd.random_number(5, 30)
        x += sd.random_number(-1 * round(0.2 * x), round(0.2 * x))
        new_point = sd.get_point(x, y)
        sd.snowflake(center=new_point, length=s, color=sd.COLOR_WHITE)
        snowflakes[n][1] = y
        snowflakes[n][3] = new_point

    sd.finish_drawing()
    sd.sleep(0.3)
    if sd.user_want_exit():
        break
sd.pause()

# Примерный алгоритм отрисовки снежинок
#   навсегда
#     очистка экрана
#     для индекс, координата_х из списка координат снежинок
#       получить координата_у по индексу
#       создать точку отрисовки снежинки
#       нарисовать снежинку цветом фона
#       изменить координата_у и запомнить её в списке по индексу
#       создать новую точку отрисовки снежинки
#       нарисовать снежинку на новом месте белым цветом
#     немного поспать
#     если пользователь хочет выйти
#       прервать цикл

# Переходите ко второй части.
# Часть 2 (делается после зачета первой части)
#
# Ускорить отрисовку снегопада
# - убрать clear_screen() из цикла
# - в начале рисования всех снежинок вызвать sd.start_drawing()
# - на старом месте снежинки отрисовать её же, но цветом sd.background_color
# - сдвинуть снежинку
# - отрисовать её цветом sd.COLOR_WHITE на новом месте
# - после отрисовки всех снежинок, перед sleep(), вызвать sd.finish_drawing()

# Усложненное задание (делать по желанию)
# - сделать рандомные отклонения вправо/влево при каждом шаге
# - сделать сугоб внизу экрана - если снежинка долетает до низа, оставлять её там,
#   и добавлять новую снежинку
# Результат решения см https://youtu.be/XBx0JtxHiLg

# зачет!
