from bowling import Bowling

def play():
    res = ''
    for i in range(10):
        saldo = 10
        tries = ''
        for j in range(2):
            hits = random.randint(0, saldo)
            if saldo == hits and j == 0:
                tries += 'X'
                break
            elif saldo == hits and j == 1:
                tries += '/'
            elif hits == 0:
                tries += '-'
            else:
                tries += str(hits)
            saldo -= hits
        res += tries
    return res

pl = play()
print(pl)

# example: python run_score.py "XXX"
#python run_score.py "52X7/23X71615145X"
