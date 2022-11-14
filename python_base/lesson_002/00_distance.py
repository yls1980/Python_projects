#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Есть словарь координат городов

sites = {
    'Moscow': (550, 370),
    'London': (510, 510),
    'Paris': (480, 480),
}

# Составим словарь словарей расстояний между ними
# расстояние на координатной сетке - ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

distances = {}
Mos = sites['Moscow']
Lond = sites['London']
Pars = sites['Paris']
Moscow_London = ((Mos[0] - Lond[0]) ** 2 + (Mos[1] - Lond[1]) ** 2) ** 0.5
Moscow_Paris = ((Mos[0] - Pars[0]) ** 2 + (Mos[1] - Pars[1]) ** 2) ** 0.5
London_Paris = ((Lond[0] - Pars[0]) ** 2 + (Lond[1] - Pars[1]) ** 2) ** 0.5

distances['Moscow'] = {}
distances['Moscow']['London'] = Moscow_London
distances['Moscow']['Paris'] = Moscow_Paris

distances['London'] = {}
distances['London']['Moscow'] = Moscow_London
distances['London']['Paris'] = London_Paris

distances['Paris'] = {}
distances['Paris']['Moscow'] = Moscow_Paris
distances['Paris']['London'] = London_Paris

print(distances)

# зачет!
