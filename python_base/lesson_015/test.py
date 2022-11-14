import re
from decimal import Decimal,ROUND_HALF_UP
a = 'Location_12_tm0.0987654320'
npos = Decimal(re.search('tm(\d|\.)+',a)[0].replace('tm',''))
npos = npos.quantize(Decimal("1"), ROUND_HALF_UP)
print(npos)