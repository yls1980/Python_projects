# -*- coding: utf-8 -*-


# Заполнить все поля в билете на самолет.
# Создать функцию, принимающую параметры: ФИО, откуда, куда, дата вылета,
# и заполняющую ими шаблон билета Skillbox Airline.
# Шаблон взять в файле lesson_013/images/ticket_template.png
# Пример заполнения lesson_013/images/ticket_sample.png
# Подходящий шрифт искать на сайте ofont.ru
import os

from PIL import Image, ImageDraw, ImageFont, ImageColor
import argparse


class TicketMaker:

    def __init__(self, template=None, font_path=None):
        # Используйте системные средства формирования путей.
        self.template = os.path.join('images','ticket_template.png') if template is None else template
        if font_path is None:
            # Если используете свои шрифты, то приложите их в репозиторий.
            self.font_path = 'ofont.ru_Prata.ttf'
        else:
            self.font_path = font_path

    def make_ticket(self, param_fio, param_from, param_to, param_datefly, out_path=None):
        if param_fio == '':
            raise Exception(f"ФИО<{param_fio}> должно быть заполнено корректно")
        if param_from == '':
            raise Exception(f"Место отправления<{param_from}> должно быть заполнено корректно")
        if param_to == '':
            raise Exception(f"Место прибытия<{param_to}> должно быть заполнено корректно")
        if param_datefly == '' and param_datefly.find('.') == 0 and len(param_datefly.split('.')) != 2:
            raise Exception(f"Дата вылета<{param_to}> должна быть заполнена корректно __.__")

        if not os.path.exists(self.template):
            raise Exception(f"Не найден файл<{self.template}>")
        if not os.path.exists(self.template):
            raise Exception(f"Не найден файл шрифта<{self.font_path}>")

        ticket_img = Image.open(self.template)
        draw = ImageDraw.Draw(ticket_img)
        font = ImageFont.truetype(self.font_path, size=13)

        draw.text((48, 138 - font.size), param_fio.upper(), font=font, fill=ImageColor.colormap['black'])
        draw.text((49, 208 - font.size), param_from.upper(), font=font, fill=ImageColor.colormap['black'])
        draw.text((49, 274 - font.size), param_to.upper(), font=font, fill=ImageColor.colormap['black'])
        font = ImageFont.truetype(self.font_path, size=12)
        draw.text((289, 275 - font.size), param_datefly.upper(), font=font, fill=ImageColor.colormap['black'])

        # ticket_img.show()
        out_path = out_path if out_path else 'ticket_' + str(
            abs(hash(param_fio + param_from + param_to + param_datefly))) + '.' + self.template.split('.')[-1]
        ticket_img.save(out_path)
        print(f'Ticket save as {out_path}')


def parser_sets():
    pars = argparse.ArgumentParser(description='Print ticket')
    pars.add_argument('fio', type=str, help='Input fio')
    pars.add_argument('pfrom', type=str, help='Input from fly')
    pars.add_argument('to', type=str, help='Input to fly')
    pars.add_argument('date', type=str, help='Input date fly')
    pars.add_argument('--save_to', type=str, default=None, help='Input save_to (full path with name)', required=False)
    return pars.parse_args()


def make_ticket(fio, from_, to, date_, save_to_=None):
    # здесь ваш код
    ticket = TicketMaker()
    ticket.make_ticket(param_fio=fio, param_from=from_, param_to=to, param_datefly=date_, out_path=save_to_)


# Усложненное задание (делать по желанию).
# Написать консольный скрипт c помощью встроенного python-модуля argparse.
# Скрипт должен принимать параметры:
#   --fio - обязательный, фамилия.
#   --from - обязательный, откуда летим.
#   --to - обязательный, куда летим.
#   --date - обязательный, когда летим.
#   --save_to - необязательный, путь для сохранения заполненнего билета.
# и заполнять билет.

# Следующие строки с настройкой парсера лучше поместить в функцию,
#  и вызывать её при запуске
#  модуля.
if __name__ == "__main__":
    args = parser_sets()
    make_ticket(fio=args.fio, from_=args.pfrom, to=args.to, date_=args.date, save_to_=args.save_to)

# example python 02_ticket.py "Иванов А.И." Москва Воронеж 08.10
