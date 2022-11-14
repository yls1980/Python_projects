# -*- coding: utf-8 -*-

# В очередной спешке, проверив приложение с прогнозом погоды, вы выбежали
# навстречу ревью вашего кода, которое ожидало вас в офисе.
# И тут же день стал хуже - вместо обещанной облачности вас встретил ливень.

# Вы промокли, настроение было испорчено, и на ревью вы уже пришли не в духе.
# В итоге такого сокрушительного дня вы решили написать свою программу для прогноза погоды
# из источника, которому вы доверяете.

# Для этого вам нужно:

# Создать модуль-движок с классом WeatherMaker, необходимым для получения и формирования предсказаний.
# В нём должен быть метод, получающий прогноз с выбранного вами сайта (парсинг + re) за некоторый диапазон дат,
# а затем, получив данные, сформировать их в словарь {погода: Облачная, температура: 10, дата:datetime...}

# Добавить класс ImageMaker.
# Снабдить его методом рисования открытки
# (использовать OpenCV, в качестве заготовки брать lesson_016/python_snippets/external_data/probe.jpg):
#   С текстом, состоящим из полученных данных (пригодится cv2.putText)
#   С изображением, соответствующим типу погоды
# (хранятся в lesson_016/python_snippets/external_data/weather_img ,но можно нарисовать/добавить свои)
#   В качестве фона добавить градиент цвета, отражающего тип погоды
# Солнечно - от желтого к белому
# Дождь - от синего к белому
# Снег - от голубого к белому
# Облачно - от серого к белому

# Добавить класс DatabaseUpdater с методами:
#   Получающим данные из базы данных за указанный диапазон дат.
#   Сохраняющим прогнозы в базу данных (использовать peewee)

# Сделать программу с консольным интерфейсом, постаравшись все выполняемые действия вынести в отдельные функции.
# Среди действий, доступных пользователю, должны быть:
#   Добавление прогнозов за диапазон дат в базу данных
#   Получение прогнозов за диапазон дат из базы
#   Создание открыток из полученных прогнозов
#   Выведение полученных прогнозов на консоль
# При старте консольная утилита должна загружать прогнозы за прошедшую неделю.

# Рекомендации:
# Можно создать отдельный модуль для инициализирования базы данных.
# Как далее использовать эту базу данных в движке:
# Передавать DatabaseUpdater url-путь
# https://peewee.readthedocs.io/en/latest/peewee/playhouse.html#db-url
# Приконнектится по полученному url-пути к базе данных
# Инициализировать её через DatabaseProxy()
# https://peewee.readthedocs.io/en/latest/peewee/database.html#dynamically-defining-a-database

import re
import requests
import time
from datetime import datetime, timedelta
import json
import cv2
import os
import numpy as np
from enum import Enum
from PIL import Image
import sys

URL_WETHER = 'https://dark-sky.p.rapidapi.com'
LOCATION = "55.750117,37.774929"
ACTIONS = ("Добавление прогнозов за диапазон дат в базу данных", "Получение прогнозов за диапазон дат из базы")
LEN_CONSOL = 64
IMAGE_PATH = os.path.join(os.path.abspath(os.getcwd()), 'python_snippets' , 'external_data')
CLOUD_PATH = os.path.join(IMAGE_PATH, 'weather_img' , 'cloud.jpg')
RAIN_PATH = os.path.join(IMAGE_PATH,'weather_img','rain.jpg')
SNOW_PATH = os.path.join(IMAGE_PATH,'weather_img', 'snow.jpg')
SUN_PATH = os.path.join(IMAGE_PATH,'weather_img', 'sun.jpg')
PROBE_PATH = os.path.join(IMAGE_PATH, 'probe.jpg')
NULL_PATH = os.path.join(IMAGE_PATH,'weather_img','null.jpg')

def check_date(str_date):
    if str_date != '' and re.match("^(0?[1-9]|[12][0-9]|3[01])[\.\-](0?[1-9]|1[012])[\.\-]\d{4}$", str_date) != None:
        return datetime.strptime(str_date.strip(), '%d.%m.%Y')
    else:
        print('Вводите дату цифрами в формате ДД.ММ.ГГГГ')
        return None


def get_noun(number, one, two, five):
    n = abs(number)
    n %= 100
    if (n >= 5) & (n <= 20):
        return five
    n %= 10
    if n == 1:
        return one
    if (n >= 2) & (n <= 4):
        return two
    return five


class Icon(Enum):
    SNOW = 'snow'
    CLEAR = 'clear-day'
    RAIN = 'rain'
    CLOUDY = ('cloudy', 'partly-cloudy-day')


class WeatherMaker:

    def __init__(self):
        try:
            from secret import TOKEN
            self.token = TOKEN
        except ImportError:
            # settings = None  # Для того, чтобы убрать замечание среду разработки.
            print('Для получения погоды нужно знать токен')
            self.token = ""

    def get_data_from_url(self, sbegin, send):
        dbegin = check_date(sbegin)
        dend = check_date(send)
        # if dbegin == dend:
        #    dend = dbegin + timedelta(days=1)
        print('')
        if dbegin is None and dend is None:
            print('Нужно указать диапазон дат, за которые вас интересует погода')
            return None
        elif dbegin is not None and dend is None:
            print('Укажите конечную дату периода за который вас интересует погода')
            return None
        elif dbegin is None and dend is not None:
            print('Укажите начальную дату периода за который вас интересует погода')
            return None
        elif dbegin > dend:
            print(
                'Начальная дата периода должна быть меньше или равна конечной дате периода за который вас интересует '
                'погода')
            return None
        else:
            # прибавим текущее время к дате
            buf = datetime.now().time()
            dbegin = dbegin + timedelta(hours=buf.hour, minutes=buf.minute, seconds=buf.second)
            dend = dend + timedelta(hours=buf.hour, minutes=buf.minute, seconds=buf.second)

        # цикл между датами
        work_date = dbegin
        wheather = []
        surl = ''
        while work_date <= dend:
            try:
                gmt_time = round(time.mktime(work_date.timetuple()))
                surl = URL_WETHER + "/" + LOCATION + ',' + str(gmt_time)
                headers = {
                    'x-rapidapi-host': "dark-sky.p.rapidapi.com/",
                    'x-rapidapi-key': self.token
                }
                querystring = {"lang": "ru", "exclude": "currently,minutely,hourly", "units": "auto"}
                json_text = requests.request("GET", surl, headers=headers, params=querystring).text
                wheather.append((work_date, json_text))
                work_date += timedelta(days=1)
            except Exception as exc:
                json_text = str(exc)
                print(json_text, f"-Ошибка при попытке получить погоду с сервера {surl} дата:{work_date}")
        return wheather


def empty_img(spath):
    img = np.zeros((100, 100, 3), dtype=np.uint8)
    if not os.path.exists(spath):
        cv2.imwrite(spath, img)
    return spath


class ImageMaker:
    def __init__(self):
        try:
            #spath = IMAGE_PATH
            #  1) используйте специальные инструменты для сборки пути: os.path.join
            #  2)  Имена файлов надо присваивать константам и использовать в основном коде только их.
            #  Имена констант пишутся большими буквами. Располагают константы в начале модуля, сразу после
            #  импортов сторонних модулей.
            #  Может возникнуть необходимость изменить имя файла и через константу это делать удобнее - константа это
            #  единое место изменения, а примениться она может во многих местах. Поэтому вверху её легко найти для
            #  изменения без необходимости перелопачивания кода проекта.
            self.image_cv2 = cv2.imread(PROBE_PATH)
            self.cloud = ((160, 164, 155), CLOUD_PATH)  # Аналогично предыдущему
            self.rain = ((239, 47, 17),    RAIN_PATH )
            self.snow = ((239, 150, 17),   SNOW_PATH )
            self.sun = ((17, 239, 239),    SUN_PATH  )
            self.null = ((255, 255, 255), empty_img(NULL_PATH))
            if (self.image_cv2 is None) or (self.cloud is None) or (self.rain is None) or (self.snow is None) or (
                    self.sun is None):
                raise Exception("Не все картинки для создания открытки найдены")
        except Exception as e:
            print(f"Не хватает изображений для создания открытки {str(e)}")

    def draw_gradient(self, rgb_color):
        rotate = 2
        height, width, channels = self.image_cv2.shape
        frame = np.zeros((width, width, channels), np.uint8)
        rectangle_position = ((0, 0), (width, width))
        frame[:, :, :] = 255
        (xMin, yMin), (xMax, yMax) = rectangle_position
        color = np.array(rgb_color, np.uint8)[np.newaxis, :]
        mask1 = np.rot90(np.repeat(np.tile(np.linspace(1, 0, (rectangle_position[1][1] - rectangle_position[0][1])),
                                           ((rectangle_position[1][0] - rectangle_position[0][0]), 1))[:, :,
                                   np.newaxis], 3, axis=2), rotate)
        frame[yMin:yMax, xMin:xMax, :] = mask1 * frame[yMin:yMax, xMin:xMax, :] + (1 - mask1) * color
        self.image_cv2 = frame
        self.image_cv2 = self.image_cv2[0: height, 0: width]

    def img_drow(self, stext, htext, ntop, pcolor=(0, 0, 0)):
        font = cv2.FONT_HERSHEY_COMPLEX
        textsize = cv2.getTextSize(stext, font, htext, 2)[0]
        text_x = round((self.image_cv2.shape[1] - textsize[0]) / 2)
        cv2.putText(self.image_cv2, stext, (text_x, ntop), font, htext, pcolor, 2, 2)

    @staticmethod
    def concate_img(img_src_path, img_past_path, name_card):
        img_src = Image.open(img_src_path)
        img_past = Image.open(img_past_path)
        width2, height2 = img_past.size
        width1, height1 = img_src.size
        img_src.paste(img_past, (round((width1 - width2) / 2), height1 - height2))
        img_src.save(name_card, quality=95)

    def drow_postcard(self, sicon, stemp, ddata):
        if sicon is None:
            print(f"Не определена погода за {ddata}")
            return
        if sicon == Icon.SNOW.value:
            fground = self.snow
        elif sicon == Icon.RAIN.value:
            fground = self.rain
        elif sicon in Icon.CLOUDY.value:
            fground = self.cloud
        elif sicon == Icon.CLEAR.value:
            fground = self.sun
        elif sicon == '':
            fground = self.null
        else:
            raise Exception(f"Не могу найти параметры для погоды {sicon}")
        sdata = ddata.strftime('%d.%m.%Y')
        self.draw_gradient(fground[0])
        self.img_drow('Погода в Москве на ' + sdata + ':', 0.7, 20, pcolor=(0, 0, 0))
        clr = (0, 0, 0)
        grad = int(float(stemp))
        if -40 < grad <= -20:
            clr = (255, 0, 0)
        elif -20 < grad <= -10:
            clr = (255, 80, 80)
        elif -10 < grad <= 0:
            clr = (255, 102, 204)
        elif 0 < grad <= 10:
            clr = (204, 51, 255)
        elif 10 < grad <= 20:
            clr = (51, 102, 255)
        elif 20 < grad <= 40:
            clr = (0, 0, 255)
        sdesc = get_noun(grad, 'градус', 'градуса', 'градусов')
        self.img_drow(stemp + ' ' + sdesc, 1.7, 80, pcolor=clr)
        spath =  os.path.join(os.path.abspath(os.getcwd()) , 'card_result')+os.sep
            # Cниппеты не относятся к данному проекту, это отрывки кода из лекций, сохраняйте прямо в папке
            #  lesson_016
        if not os.path.exists(spath):
            os.makedirs(spath, True)
        out_img_file = f"{spath}card{sdata.replace('.', '_')}.jpg"

        cv2.imwrite(out_img_file, self.image_cv2)
        self.concate_img(out_img_file, fground[1], out_img_file)
        self.image_cv2 = cv2.imread(out_img_file)
        print('Сформирована открытка ' + out_img_file)


class DatabaseUpdater:
    def __init__(self):
        try:
            from wheather_db import MethodsDb
            self.MethodsDb = MethodsDb()
            self.MethodsDb.create_db()
        except ImportError:
            print('Для работы с базой данных нужно ее подключить')

    def create_table(self):
        self.MethodsDb.create_table()

    def get_data_from_db(self, dbegin, dend):
        if dend < dbegin:
            print(
                f'Необходимо чтобы дата начала периода({dbegin.strftime("%m/%d/%Y")}) была меньше и равнялась дате '
                f'окончания преиода ({dend.strftime("%m/%d/%Y")}) ')
            return None
        else:
            return self.MethodsDb.read_rows(dbegin, dend)

    def put_data_to_db(self, ddate, ntemp, sicon):
        if ddate is not None and str(ntemp) != '':
            self.MethodsDb.ins_row(ddate, ntemp, sicon)
        else:
            print(
                f'Необходимо чтобы дата({ddate.strftime("%m/%d/%Y")}) и температура({str(ntemp)}) были заполнены, для '
                f'внесения информации в базу данных')


def fill_weather_db(sbegin, send):
    loc_weather_maker = WeatherMaker()
    responses = loc_weather_maker.get_data_from_url(sbegin, send)
    db = DatabaseUpdater()
    db.create_table()
    res = []
    if responses is not None:
        for response in responses:
            json_data = json.loads(response[1])
            temp = json_data["daily"]["data"][0]["dewPoint"]
            day = response[0].date()
            try:
                icon = json_data["daily"]["data"][0]["icon"]
            except KeyError:
                icon = ''
                print(f"Нет данных об облачности на {response[0].strftime('%d.%m.%Y')}")
            # day = response[0].strftime('%d.%m.%Y')
            db.put_data_to_db(day, temp, icon)
            res.append((icon, temp, day))
            # print(day, temp)
            # id_number = json_data["daily"]["id_number"]
        return res
    else:
        return None


def read_weather_db(sbegin, send):
    db = DatabaseUpdater()
    dbegin = check_date(sbegin).date()
    dend = check_date(send).date()
    if dbegin is None:
        dbegin = datetime.now().date()
    if dend is None:
        dend = dbegin
    res = []
    aaa = 0
    for weather in db.get_data_from_db(dbegin, dend):
        res.append((weather.icon, weather.temp, weather.dt))
        aaa += 1
    if aaa == 0:
        res.append((None, None, sbegin + '-' + send))
    return res


def abzac(stext):
    n = LEN_CONSOL
    print('*' * n)
    frm = '{:*^' + str(n) + '}'
    print(frm.format(' ' + stext + ' '))
    print('*' * n)


def show_last_week():
    # получение погоды за последнюю неделюы
    d_data = datetime.now().date() - timedelta(days=6)
    db = DatabaseUpdater()
    abzac('ПОГОДА за НЕДЕЛЮ')
    while d_data <= datetime.now().date():
        s_data = d_data.strftime('%d.%m.%Y')
        weather = None
        for query in db.get_data_from_db(d_data, d_data):
            weather = (query.icon, query.temp, query.dt.date())
        if weather is None:
            weather = fill_weather_db(s_data, s_data)[0]
        d_data = d_data + timedelta(days=1)
        print(f'* Погода на {weather[2]} | {weather[0]: ^20} | {weather[1]} градусов *')
    print('*' * LEN_CONSOL)


def make_card(weather_data):
    image_maker = ImageMaker()
    for weather in weather_data:
        image_maker.drow_postcard(weather[0], str(weather[1]), weather[2])


def add_weather2db(s_act):
    print('')
    print(f'Вы выбрали действие "{s_act}"')
    s_begin = input("     Введите дату начала диапазона прогноза в формате dd.mm.yyyy: ")
    s_end = input("     Введите дату окончания диапазона прогноза  в формате dd.mm.yyyy: ")
    b_out = input("     Нужно выводить внесенные результаты на консоль (1 - Да 2- Нет): ")
    b_card = input("     Нужно делать открытки из полученных данных о погоде (1 - Да 2- Нет): ")
    weathers = fill_weather_db(s_begin, s_end)
    if weathers is not None:
        print(f'Данные о погоде успешно внесены в базу. Записано {len(weathers)} строк')
        if b_out.strip() == '1':
            abzac(f'ПОГОДА c {s_begin} по {s_end}')
            for weather in weathers:
                print(f'* Погода на {weather[2].strftime("%d.%m.%Y")} | {weather[0]: ^20} | {weather[1]} градусов *')
        if b_card.strip() == '1':
            make_card(weathers)


def get_weather_from_db(s_act):
    print('')
    print(f'Вы выбрали действие "{s_act}"')
    s_begin = input("    Введите дату начала диапазона прогноза в формате dd.mm.yyyy: ")
    s_end = input("    Введите дату окончания диапазона прогноза  в формате dd.mm.yyyy: ")
    b_card = input("    Нужно делать открытки из полученных данных о погоде (1 - Да 2- Нет): ")
    weathers = read_weather_db(s_begin, s_end)
    if weathers is not None:
        abzac(f'ПОГОДА c {s_begin} по {s_end}')
        for weather in weathers:
            if weather[0] is not None:
                s_data = weather[2].strftime("%d.%m.%Y")
                sicon = weather[0]
                s_temp = weather[1]
            else:
                s_data = str(weather[2])
                sicon = 'нет данных'
                s_temp = 'нет данных'
            print(f'* Погода на {s_data} | {sicon: ^20} | {s_temp} градусов *')
        if b_card.strip() == '1':
            make_card(weathers)
    else:
        print(f'Данные о погоде с {s_begin} по {s_end} отсутствуют в базе данных.')


def start():
    show_last_week()
    print('')
    print('Выбор действий:')
    a = 0
    for act in ACTIONS:
        a += 1
        print(f'{a}. {act}')
    number_act = input("Выберите действие, что вы хотит сделать (1,2)? ")
    if number_act.strip() == '1':
        add_weather2db(ACTIONS[0])
    elif number_act.strip() == '2':
        get_weather_from_db(ACTIONS[1])


if __name__ == '__main__':
    args = sys.argv
    if "--help" in args or len(args) == 1:
        print("Программа для получения погоды")
    start()
