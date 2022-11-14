import unittest
from lesson_014.bowling import *


def test_exc(sexc):
    Inlocal(sexc).get_score()
    Inmarket(sexc).get_score()


# В названии класса первая буква должна быть заглавной.
class BowlingTest(unittest.TestCase):

    def test_normal(self):
        bw = Inlocal('XXXXXXXXXX')
        #bw.set_local()
        result = bw.get_score()
        self.assertEqual(result, 200)

    def test_normal1(self):
        result = Inlocal('4/------------------').get_score()
        self.assertEqual(result, 15)

    def test_empty(self):
        self.assertRaises(EmptyEx, test_exc, '')

    def test_unknown(self):
        self.assertRaises(UnknownEx, test_exc, 'sddf')

    def test_CountFreym(self):
        self.assertRaises(CountFreymEx, test_exc, '----X')

    def test_FirstSpeir(self):
        self.assertRaises(FirstSpeirEx, test_exc, '/--X4563')

    def test_many(self):
        self.assertRaises(ManyEx, test_exc, '856546975467948567985456546')

    def test_normal2(self):
        result = Inlocal('62--4/12257/--32352-').get_score()
        self.assertEqual(result, 63)

    def test_normal3(self):
        result = Inlocal('52X7/23X71615145X').get_score()
        self.assertEqual(result, 117)

    def test_normal2_1(self):
        bw = Inmarket('XXX347/21--------')
        result = bw.get_score()
        self.assertEqual(result, 92)

    def test_normal4(self):
        bwo = Inmarket('X4/34--------------')
        result = bwo.get_score()
        self.assertEqual(result, 40)


def test_run():
    unittest.main()


if __name__ == '__main__':
    unittest.main()
