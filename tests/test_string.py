from tests.base_test_case import BaseTestCase
from zeraora.string import *


class StringTest(BaseTestCase):

    def test_randb64(self):
        for length in range(100):
            self.assertEqual(length, len(randb64(length)))
        for length in range(100):
            self.assertEqual(length, len(randb64(length, safe=True)))
        self.assertEqual(0, len(set(randb64(100)) - set(Notations.BASE64)))
        self.assertEqual(0, len(set(randb64(100, safe=True)) - set(Notations.BASE64SAFE)))

    def test_randb64o(self):
        for length in range(100):
            self.assertEqual(length, len(randb64o(length)))
        for length in range(100):
            self.assertEqual(length, len(randb64o(length, safe=True)))
        self.assertEqual(0, len(set(randb64o(100)) - set(Notations.BASE64)))
        self.assertEqual(0, len(set(randb64o(100, safe=True)) - set(Notations.BASE64SAFE)))

    def test_randb62(self):
        self.assertEqual(0, len(set(randb62(100)) - set(Notations.BASE62)))
        for length in range(100):
            self.assertEqual(length, len(randb62(length)))

    def test_randb62o(self):
        for length in range(100):
            self.assertEqual(length, len(randb62o(length)))
        self.assertEqual(0, len(set(randb62o(100)) - set(Notations.BASE62)))

    def test_randb16(self):
        for length in range(100):
            self.assertEqual(length, len(randb16(length)))
        self.assertEqual(0, len(set(randb16(100).upper()) - set(Notations.BASE16)))

    def test_randb16o(self):
        for length in range(100):
            self.assertEqual(length, len(randb16o(length)))
        self.assertEqual(0, len(set(randb16o(100).upper()) - set(Notations.BASE16)))
