# -*- coding: utf-8 -*-
import os, re
from collections import defaultdict
import operator


# Названия классов нужно делать в формате CamelCase.
class BowlingResult:
    def __init__(self, in_file, out_file):
        self.in_file = in_file
        self.out_file = out_file
        self.reyting_games = defaultdict(int)
        self.reyting_wins = defaultdict(int)
        if not os.path.exists(self.in_file):
            raise FileExistsError(self.in_file)
        if not self.in_file.endswith('txt'):
            raise Exception(f'файл {self.in_file} должен иметь расширение txt')

    def print_reyting(self):
        s1 = '+----------+------------------+--------------+'
        s2 = '| Игрок    |  сыграно матчей  |  всего побед |'
        print(s1)
        print(s2)
        print(s1)
        buf = sorted(self.reyting_wins.items(), key=operator.itemgetter(1), reverse=True)
        for sname, wins in buf:
            plays = self.reyting_games[sname]
            s3 = '|{:^10s}|{:^18d}|{:^14d}|'.format(sname, plays, wins)
            print(s3)
        print(s1)

    def skan_file(self, Bowling):
        with open(self.in_file, 'r', encoding='utf-8') as ft:
            # переменная для определения начала игры
            start = False
            # словарь для определения победителя
            res_tour = defaultdict(int)
            out_file = open(self.out_file, 'w', encoding='utf-8')
            for line in ft:
                try:
                    out_str = ''
                    if line[0:3] == '###':
                        start = True
                        continue
                    if line.find('winner is', 0) >= 0:
                        start = False
                        buf = sorted(res_tour.items(), key=operator.itemgetter(1), reverse=True)
                        for name, score in buf:
                            out_str = f'winner is {name}\n\n'
                            self.reyting_wins[name] += 1
                            break
                        res_tour = defaultdict(int)

                    if start:
                        sname = ''.join(re.findall(r'[А-Яа-я]', line[0:7]))
                        field_list = line[:-1].split('\t')
                        play_result = field_list[1]
                        try:
                            bw = Bowling(play_result)
                            single_result = bw.get_score()
                            out_str = '{:7s}\t{:20s}\t{:3d}\n'.format(sname, play_result, single_result)
                        except Exception as e:
                            single_result = 0
                            out_str = '{:7s}\t{:20s}\t{:3d}\tОшибка:{:100s}\n'.format(sname, play_result, single_result,
                                                                                      str(e))
                        res_tour[sname] = single_result
                        self.reyting_games[sname] += 1
                        if self.reyting_wins[sname] == 0:
                            self.reyting_wins[sname] = 0
                    if out_str != '':
                        out_file.write(out_str)
                # Нужно обязательно добавлять тип исключения, в самом общем случае Exception.
                #  Если не указывать тип исключения, то могут быть перехвачены базовые исключения,
                #  используемые в нормальной работе. Например StopIteration
                except Exception as e:
                    print(e)
                    break
            out_file.close()
