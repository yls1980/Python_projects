# -*- coding: utf-8 -*-

# Нужно написать скрипт для упорядочивания фотографий (вообще любых файлов)
# Скрипт должен разложить файлы из одной папки по годам и месяцам в другую.
# Например, так:
#   исходная папка
#       icons/cat.jpg
#       icons/man.jpg
#       icons/new_year_01.jpg
#   результирующая папка
#       icons_by_year/2018/05/cat.jpg
#       icons_by_year/2018/05/man.jpg
#       icons_by_year/2017/12/new_year_01.jpg
#
# Входные параметры основной функции: папка для сканирования, целевая папка.
# Имена файлов в процессе работы скрипта не менять, год и месяц взять из времени последней модификации файла
# (время создания файла берется по разному в разых ОС - см https://clck.ru/PBCAX - поэтому берем время модификации).
#
# Файлы для работы взять из архива icons.zip - раззиповать проводником ОС в папку icons перед написанием кода.
# Имя целевой папки - icons_by_year (тогда она не попадет в коммит, см .gitignore в папке ДЗ)
#
# Пригодятся функции:
#   os.walk
#   os.path.dirname
#   os.path.join
#   os.path.normpath
#   os.path.getmtime
#   time.gmtime
#   os.makedirs
#   shutil.copy2
#
# Чтение документации/гугла по функциям - приветствуется. Как и поиск альтернативных вариантов :)
#
# Требования к коду: он должен быть готовым к расширению функциональности - делать сразу на классах.
# Для этого пригодится шаблон проектирование "Шаблонный метод"
#   см https://refactoring.guru/ru/design-patterns/template-method
#   и https://gitlab.skillbox.ru/vadim_shandrinov/python_base_snippets/snippets/4

import datetime
import os
import shutil


# На первом этапе нужно сделать класс, сортирующий файлы из предварительно
#  распакованного архива.
# all_images - папка с предварительно распакованным архивом. Я не очень понял, что нужно еще?

# Названия классов должны быть записаны в CamelCase.
class ImagesGroup:

    def __init__(self, source_path, dest_path, zip_name=""):
        self.images = {}
        self.zip_name = zip_name
        self.source_path = source_path
        self.dest_path = dest_path

    def read_images(self):
        if os.path.exists(self.source_path):
            for dirpath, dirnames, files in os.walk(self.source_path):
                for file in files:
                    #  Не нужно филльтровать файлы по расширению.
                    # if file.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif', '.ico')):
                    sfile = os.path.normpath(os.path.join(dirpath, file))
                    self.images[sfile] = os.path.getmtime(sfile)
            if len(self.images) == 0:
                print(f'папка с файлами {self.source_path} не содержит файлов')
        else:
            print(f'папка с файлами {self.source_path} не существует на диске')

    def write_images(self):
        if not os.path.exists(self.dest_path):
            os.mkdir(self.dest_path)
        for image in self.images:
            img_time = datetime.datetime.utcfromtimestamp(self.images[image])
            image_file = os.path.basename(image)
            path = os.path.join(self.dest_path, str(img_time.year), str(img_time.month))
            if not os.path.exists(path):
                os.makedirs(path)
            shutil.copy2(image, os.path.join(path, image_file))
        print(f'Каталог {os.path.join(os.path.abspath(os.getcwd()), self.dest_path)} успешно заполнен')


ig = ImagesGroup('all_images', 'icons_by_year')
ig.read_images()
ig.write_images()

# Усложненное задание (делать по желанию)
# Нужно обрабатывать zip-файл, содержащий фотографии, без предварительного извлечения файлов в папку.
# Это относится только к чтению файлов в архиве. В случае паттерна "Шаблонный метод" изменяется способ
# получения данных (читаем os.walk() или zip.namelist и т.д.)
# Документация по zipfile: API https://docs.python.org/3/library/zipfile.html

#  Нужно убрать закомментированный код, который больше не используется.
#  После этого задание можно будет зачесть. Или вы можете сделать усложнённую
#  версие, если захотите.
#  Здесь два варианта решения задания. Первый: сделать класс сортировщик каталога, а затем
#  расширить его сделав сортировку zip архива, заменив пару методов.
#  Второй способ сделать абстрактный класс с двумя наследниками: для сортировки каталога
#  и сортировки архива.

# Зачёт!
