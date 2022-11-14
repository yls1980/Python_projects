import re
from lesson_014.bowling_1 import Bowling

BW = Bowling('X4/34--------------')
inmarketstate = BW.set_market()
#inmarketstate = BW.set_local()
BW.get_score()