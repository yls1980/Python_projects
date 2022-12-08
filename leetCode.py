def romanToInt(s: str) -> int:
    Rrc_dict = {'I':1,'V':5,'X':10,'L':50,'C':100,'D':500,'M':1000,'R':40,'N':90,'U':400,'Y':900,'J':4,'K':9}
    s=s.replace('IV','J')
    s=s.replace('IX', 'K')
    s=s.replace('XL', 'R')
    s=s.replace('XC', 'N')
    s=s.replace('CD', 'U')
    s=s.replace('CM', 'Y')
    rc = list(s)
    res = 0
    for r in rc:
        n = Rrc_dict[r]
        res+=n
    print (res)

romanToInt('MCMXCIV')