import re

#a = re.search('tm\d+','Location_2_tm33300')[0].replace('tm','')
a = re.search('_exp\d+_','Mob_exp10_tm40')[0][4:].replace('_','')
print ((a))