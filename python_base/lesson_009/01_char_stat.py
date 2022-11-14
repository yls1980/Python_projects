# -*- coding: utf-8 -*-

# Подсчитать статистику по буквам в романе Война и Мир.
# Входные параметры: файл для сканирования
# Статистику считать только для букв алфавита (см функцию .isalpha() для строк)
#
# Вывести на консоль упорядоченную статистику в виде
# +---------+----------+
# |  буква  | частота  |
# +---------+----------+
# |    А    |   77777  |
# |    Б    |   55555  |
# |   ...   |   .....  |
# |    a    |   33333  |
# |    б    |   11111  |
# |   ...   |   .....  |
# +---------+----------+
# |  итого  | 9999999  |
# +---------+----------+
#
# Упорядочивание по частоте - по убыванию. Ширину таблицы подберите по своему вкусу
#
# Требования к коду: он должен быть готовым к расширению функциональности - делать сразу на классах.
# Для этого пригодится шаблон проектирование "Шаблонный метод"
#   см https://refactoring.guru/ru/design-patterns/template-method
#   и https://gitlab.skillbox.ru/vadim_shandrinov/python_base_snippets/snippets/4
import os
import zipfile
import collections
import operator


# Названия классов должны быть записаны в CamelCase.
#  Этот класс можно убрать и сделать методом основного класса сортировки.
#  Он достаточно компактен и используется всего в одном месте.


# Названия классов должны быть записаны в CamelCase,
#  т. е. название должно начинаться с заглавной буквы,
#  символа подчёркивания буть не должно, а разные слова обозначаются
#  заглавными буквами. В данном случае нужно сделать из stat_file StatFile
class StatFile:
    preverse = True
    pcolumn = 1
    zip_name = 'voyna-i-mir.txt.zip'

    def __init__(self):
        self.file_name = []
        self.stat = collections.defaultdict(int)

    #  Сделайте эту функцию частью класса.
    @staticmethod
    def pr(width1=5, width2=10, val1="", val2=""):
        if val1 == "" and val2 == "":
            znak = "+"
            empty = '-'
        else:
            znak = "|"
            empty = ' '
        # print(znak+'{}'+znak+'{}'+znak.format(width1 * empty, width2 * empty))
        s_templ = znak + '{var:' + empty + '^' + str(width1) + '}' + znak + '{var1:' + empty + '>' + str(
            width2) + '}' + znak
        print(s_templ.format(var=val1, var1=val2))

    def unzip(self, extract_path):
        if self.zip_name.endswith('.zip'):
            zfile = zipfile.ZipFile(self.zip_name, 'r')
            zfile.extractall(extract_path)
            if os.path.exists(extract_path):
                for file in os.listdir(extract_path):
                    if file.endswith('.txt'):
                        self.file_name.append(os.path.join(extract_path, file))
            zfile.close()

    def read_file(self, file_name):
        # Отделите сбор статистики от вывода результата.
        print(f"{file_name:_^100}")
        with open(file_name, 'r', encoding='cp1251') as file:
            for line in file:
                for char in line:
                    if char.isalpha():
                        #  Подобная конструкций со словарём может
                        #  быть значительно упрощена, если заменить словарь на
                        #  defaultdict или Counter из библиотеки collections. Нужно будет
                        #  в функции __init__ заменить {} на collections.defaultdict(int),
                        #  а из следующих 4 строк оставить одну с +=. Похожим способом можно
                        #  применить collections.Counter
                        self.stat[char] += 1
                        # if char in self.stat:
                        #    self.stat[char] += 1
                        # else:
                        #    self.stat[char] = 1

    def out_stat(self):
        self.stat_zip_files()
        self.pr()
        self.pr(val1="буква", val2="частота")
        self.pr()
        all_simbols = 0

        # Аргумент key оптимальнее использовать вместе с функцией
        #  operator.itemgetter вместо lambda. Функция itemgetter
        #  работает быстрее и надёжнее чем lambda
        for char, cnt in sorted(self.stat.items(), key=operator.itemgetter(self.pcolumn), reverse=self.preverse):
            self.pr(val1=char, val2=str(cnt))
            all_simbols += cnt
        self.pr()
        self.pr(val1="итого", val2=str(all_simbols))
        self.pr()

    def stat_zip_files(self):
        cur_dir = os.path.abspath(os.getcwd())
        for dirpath, dirnames, files in os.walk(cur_dir):
            for file in files:
                if file == self.zip_name:
                    self.zip_name = os.path.join(dirpath, file)
                    break
            if os.path.exists(self.zip_name):
                break

        self.unzip(os.path.join(cur_dir, 'ARH'))
        for file in self.file_name:
            self.read_file(file)


stat = StatFile()
stat.out_stat()


#  Переходите ко второму этапу задания. Постарайтесь
#  сделать решение на классах и максимально унифицировать
#  код, избегая его дублирования.

# После зачета первого этапа нужно сделать упорядочивание статистики
#  - по частоте по возрастанию
#  Попробуйте изменить задание так, чтобы каждый способ упорядочивания
#  статистики был реализован отдельным классом. Параметры сортировки,
#  которые сейчас передаются при инициализации задавались переменными класса.
# Пример с демонстрацией отличия переменных класса от переменных экземпляра:
#
#  class MainClass:
#     variable1 = 0  # Это переменная класса
#
#      def __init__():
#           variable2 = 1  #  Это переменная экземпляра.
#  В результате должно получиться что-то подобное:
# class MainClass:
#     variable1 = 1
#
#     def __init__()
#         ...
#
# class Aggregation1(MainClass):
#     variable1 = 2
#
# class Aggregation2(MainClass):
#     variable1 = 3

class StatFileFreq(StatFile):
    preverse = False


class StatFileaAlph1(StatFile):
    preverse = False
    pcolumn = 0


class StatFileaAlph2(StatFile):
    reverse = True
    pcolumn = 0


# - по частоте по возрастанию
print('Сортировка по частоте по возрастанию')
sff = StatFileFreq()
sff.out_stat()
print('Сортировка по алфавиту по возрастанию')
sfa1 = StatFileaAlph1()
sfa1.out_stat()
print('Сортировка по алфавиту по убыванию')
sfa2 = StatFileaAlph2()
sfa2.out_stat()

# Зачёт!
