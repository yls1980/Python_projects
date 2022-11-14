# -*- coding: utf-8 -*-

# Подземелье было выкопано ящеро-подобными монстрами рядом с аномальной рекой, постоянно выходящей из берегов.
# Из-за этого подземелье регулярно затапливается, монстры выживают, но не герои, рискнувшие спуститься к ним в поисках
# приключений.
# Почуяв безнаказанность, ящеры начали совершать набеги на ближайшие деревни. На защиту всех деревень не хватило
# солдат и вас, как известного в этих краях героя, наняли для их спасения.
#
# Карта подземелья представляет собой json-файл под названием rpg.json. Каждая локация в лабиринте описывается объектом,
# в котором находится единственный ключ с названием, соответствующем формату "Location_<N>_tm<T>",
# где N - это номер локации (целое число), а T (вещественное число) - это время,
# которое необходимо для перехода в эту локацию. Например, если игрок заходит в локацию "Location_8_tm30000",
# то он тратит на это 30000 секунд.
# По данному ключу находится список, который содержит в себе строки с описанием монстров а также другие локации.
# Описание монстра представляет собой строку в формате "Mob_exp<K>_tm<M>", где K (целое число) - это количество опыта,
# которое получает игрок, уничтожив данного монстра, а M (вещественное число) - это время,
# которое потратит игрок для уничтожения данного монстра.
# Например, уничтожив монстра "Boss_exp10_tm20", игрок потратит 20 секунд и получит 10 единиц опыта.
# Гарантируется, что в начале пути будет две локации и один монстр
# (то есть в коренном json-объекте содержится список, содержащий два json-объекта, одного монстра и ничего больше).
#
# На прохождение игры игроку дается 123456.0987654321 секунд.
# Цель игры: за отведенное время найти выход ("Hatch")
#
# По мере прохождения вглубь подземелья, оно начинает затапливаться, поэтому
# в каждую локацию можно попасть только один раз,
# и выйти из нее нельзя (то есть двигаться можно только вперед).
#
# Чтобы открыть люк ("Hatch") и выбраться через него на поверхность, нужно иметь не менее 280 очков опыта.
# Если до открытия люка время заканчивается - герой задыхается и умирает, воскрешаясь перед входом в подземелье,
# готовый к следующей попытке (игра начинается заново).
#
# Гарантируется, что искомый путь только один, и будьте аккуратны в рассчетах!
# При неправильном использовании библиотеки decimal человек, играющий с вашим скриптом рискует никогда не найти путь.
#
# Также, при каждом ходе игрока ваш скрипт должен запоминать следущую информацию:
# - текущую локацию
# - текущее количество опыта
# - текущие дату и время (для этого используйте библиотеку datetime)
# После успешного или неуспешного завершения игры вам необходимо записать
# всю собранную информацию в csv файл dungeon.csv.
# Названия столбцов для csv файла: current_location, current_experience, current_date
#
#
# Пример взаимодействия с игроком:
#
# Вы находитесь в Location_0_tm0
# У вас 0 опыта и осталось 123456.0987654321 секунд до наводнения
# Прошло времени: 00:00
#
# Внутри вы видите:
# — Вход в локацию: Location_1_tm1040
# — Вход в локацию: Location_2_tm123456
# Выберите действие:
# 1.Атаковать монстра
# 2.Перейти в другую локацию
# 3.Сдаться и выйти из игры
#
# Вы выбрали переход в локацию Location_2_tm1234567890
#
# Вы находитесь в Location_2_tm1234567890
# У вас 0 опыта и осталось 0.0987654321 секунд до наводнения
# Прошло времени: 20:00
#
# Внутри вы видите:
# — Монстра Mob_exp10_tm10
# — Вход в локацию: Location_3_tm55500
# — Вход в локацию: Location_4_tm66600
# Выберите действие:
# 1.Атаковать монстра
# 2.Перейти в другую локацию
# 3.Сдаться и выйти из игры
#
# Вы выбрали сражаться с монстром
#
# Вы находитесь в Location_2_tm0
# У вас 10 опыта и осталось -9.9012345679 секунд до наводнения
#
# Вы не успели открыть люк!!! НАВОДНЕНИЕ!!! Алярм!
#
# У вас темнеет в глазах... прощай, принцесса...
# Но что это?! Вы воскресли у входа в пещеру... Не зря матушка дала вам оберег :)
# Ну, на этот-то раз у вас все получится! Трепещите, монстры!
# Вы осторожно входите в пещеру... (текст умирания/воскрешения можно придумать свой ;)
#
# Вы находитесь в Location_0_tm0
# У вас 0 опыта и осталось 123456.0987654321 секунд до наводнения
# Прошло уже 0:00:00
# Внутри вы видите:
#  ...
#  ...
#
# и так далее...

import json
import datetime
from decimal import Decimal, ROUND_HALF_UP
import re
import csv

REMAINING_TIME = '123456.0987654321'
# если изначально не писать число в виде строки - теряется точность!
FIELD_NAMES = ['current_location', 'current_experience', 'current_date']
FILE_NAME = 'rpg.json'
OUT_CSV_FILE = 'histDungeon.csv'
# Имена констант пишутся большими буквами

with open(FILE_NAME, 'r') as read_file:
    #  Имена файлов надо присваивать константам и использовать в основном коде только их.
    #  Имена констант пишутся большими буквами. Располагают константы в начале модуля, сразу после
    #  импортов сторонних модулей.
    #  Может возникнуть необходимость изменить имя файла и через константу это делать удобнее - константа это
    #  единое место изменения, а примениться она может во многих местах. Поэтому вверху её легко найти для изменения
    #  без необходимости перелопачивания кода проекта.
    loaded_json_file = json.load(read_file)


class Hero:
    def __init__(self):  # расположите этот метод на первом месте
        self.goto_start()
        self.history = []

    def goto_start(self):
        self.spent_time = 0  #  считается хорошей практикой объявлять все атрибуты в методе __init__ - используется несколько раз поэтому вынесено отдельно
        self.experience = 0
        self.nleft_time = Decimal(REMAINING_TIME)
        self.spent_time = 0
        self.start = datetime.datetime.now()
        print('Вы осторожно входите в пещеру...')

    def set_position(self, position, left_time, experience, spent_time):
        res = None
        print(f'Вы находитесь в {position}')
        left_time -= self.spent_time
        print(f'У вас {experience} опыта и осталось {left_time} секунд до наводнения')
        tspent_time = datetime.datetime.now() - self.start
        print(f"Прошло времени: {spent_time} секунд. Время игры {tspent_time}")

        self.history.append({"location": position, "experience": experience,
                             "datetime": datetime.datetime.now().strftime("%m.%d.%Y, %H:%M:%S")})
        if left_time < 0:
            print('Вы не успели открыть люк!!! НАВОДНЕНИЕ!!! Алярм!')
            print('У вас темнеет в глазах... прощай, принцесса...')
            print()
            print('Но что это?! Вы воскресли у входа в пещеру... Не зря матушка дала вам оберег :)')
            print('# Ну, на этот-то раз у вас все получится! Трепещите, монстры!')
            self.goto_start()
        return res

    def goto_location(self, plocation):
        slocation = plocation
        ntime = Decimal(re.search('tm(\d|\.)+', slocation)[0].replace('tm', ''))
        ntime = ntime.quantize(Decimal("1"), ROUND_HALF_UP)
        # npos = re.search('_\d+_', slocation)[0].replace('_', '')
        self.spent_time += ntime

    def kill_monstr(self,actions,check_action):
        smonstr = actions[check_action][1]
        ntime = int(re.search('tm(\d|\.)+', smonstr)[0].replace('tm', ''))
        nexp = int(re.search('_exp\d+_', smonstr)[0][4:].replace('_', ''))
        self.experience += nexp
        self.spent_time = self.spent_time + ntime
        print(f'Вы выбрали сражаться с монстром {smonstr}')
        actions.pop(check_action)

    def choose(self, actions):  # очень большой метод, стоит его декомпозировать не несколько более мелких
        npp = 0
        print('Выберите действие:')
        for action in actions:
            npp += 1
            print(f'{npp}. {action[0]}')
        try:
            check_action = int(input("Напишите цифру ответа: "))
            print(f"  --   Вы нажали {check_action}  ---")
        except ValueError:
            check_action = -1
        if -1 < check_action <= len(actions):
            check_action -= 1
            if actions[check_action][2] is not None:
                # идем по локации
                self.goto_location(actions[check_action][1])
                return actions[check_action][2]
            elif actions[check_action][1] is not None and actions[check_action][2] is None:
                # убиваем монстра
                self.kill_monstr(actions=actions,check_action=check_action)
                if self.set_position(actions[check_action][3], self.nleft_time, self.experience,
                                     self.spent_time) is None:
                    return self.choose(actions)
                else:
                    return None  # победили
            else:
                # сдаемся
                print("Вы проиграли")
                return None
        else:
            print("Ничего не выбрано - вы проиграли")
            return None

    def do_it(self, locations, cur_loc=None):
        if isinstance(locations, dict):
            for name, place in locations.items():
                if self.set_position(name, self.nleft_time, self.experience, self.spent_time) == 1:
                    return None  # победили
                self.do_it(place, cur_loc=name)
        elif isinstance(locations,str):
            if self.experience >= 280 and self.nleft_time >= 0:
                print('УРА вы победили и нашли выход')
                print(locations)

        if isinstance(locations, list):
            print('Внутри вы видите:')
            actions = []
            for item in locations:
                if isinstance(item, str):
                    print(f'— Монстра {item}')
                    actions.append((f'Атаковать монстра {item}', item, None, cur_loc))
                elif isinstance(item, dict):
                    for locs in item:
                        print(f'— Вход в локацию: {locs}')
                        actions.append((f'Перейти в локацию {locs}', locs, item, cur_loc))
                    # do_it(item)
                else:
                    print(type(item))
            actions.append(('Сдаться и выйти из игры', None, None, cur_loc))
            nextt = self.choose(actions)
            if nextt is not None:
                self.do_it(nextt)

    def hist2csv(self):
        with open(OUT_CSV_FILE, 'w', newline='') as out_csv:  # Аналогично предыдущему
            writer = csv.DictWriter(out_csv, delimiter=',', fieldnames=self.history[0])
            writer.writeheader()
            writer.writerows(self.history)


my_hero = Hero()  # в имена переменных между словами надо ставить знак подчёркивания
my_hero.do_it(loaded_json_file)
my_hero.hist2csv()
#  игра заканчивается до перехода в Hatch
#  А при каких услорвиях, что то я не могу подобрать такого исхода?
#   Комментарий был о том, что игра не показывает возможность перехода в Hatch после
#  битвы с монстром и сразу сообщает о победе, хотя для перехода в Hatch нужно затрать определенное время и набрать
#  нужный опыт, это нужно учесть

# Вроде бы однозначно написано условие победы: Чтобы открыть люк ("Hatch") и выбраться через него на поверхность,
# нужно иметь не менее 280 очков опыта.
# или я что-то не учел? if experience >= 280: (line 140)
#  Да, игра заканчивается в подземелье, у выходного люка (hatch):
#  Выберите действие:
# 1. Атаковать монстра Mob_exp40_tm50
# 2. Перейти в локацию Hatch_tm159.098765432
# 3. Сдаться и выйти из игры
# Напишите цифру ответа: 1
#   --   Вы нажали 1  ---
# Вы выбрали сражаться с монстром Mob_exp40_tm50
# Вы находитесь в Location_B2_tm2000
# У вас 280 опыта и осталось 159.0987654321 секунд до наводнения
# Прошло времени: 123297 секунд. Время игры 0:17:12.445162
# УРА вы победили и нашли выход
#  Видите: в локации находится монстр и выход, убиваем монстра и сразу выигрываем, а ведь чтобы выйти из люка нужно
#  время которое указано в строке новой локации доступной из текущей локации: Hatch_tm159.098765432. У игрока два
#  параметра: текущий опыт и остаток времени до наводненияРечь про то, что надо дать игроку возможность выбрать локацию
#  и сделать переход в неё - то есть учесть время необходимое на переход.
#  После этого уже делать вывод об успешном окончании игры, ведь времени же может и не хватить.
# А... понятно...)
# for pos in go_dungeon(loaded_json_file):
#     set_position(loaded_json_file[0],nleft_time,nexperience,spent_time)
#     break


# Учитывая время и опыт, не забывайте о точности вычислений!

# зачет!