from math import ceil
from typing import Set

from tests.base_test_case import BaseTestCase
from zeraora.string import *


class StringTest(BaseTestCase):

    def checkRandomChars(self, charset: Set[str], length, string: str):
        """
        检查随机生成的字符串是否对应字符集及长度。
        """
        self.assertEqual(length, len(string))
        self.assertEmpty(set(string) - charset)

    def test_randb64(self):
        charset64 = set(Notations.BASE64)
        charset64s = set(Notations.BASE64SAFE)
        for n in range(100):
            self.checkRandomChars(charset64, n, randb64(n))
            self.checkRandomChars(charset64, n, randb64(n, use_os=True))
            self.checkRandomChars(charset64s, n, randb64(n, safe=True))
            self.checkRandomChars(charset64s, n, randb64(n, safe=True, use_os=True))

    def test_randb64y(self):
        charset64 = set(Notations.BASE64 + '=')
        charset64s = set(Notations.BASE64SAFE + '=')
        for n in range(100):
            qChar = ceil(n / 3) * 4
            self.checkRandomChars(charset64, qChar, randb64y(n))
            self.checkRandomChars(charset64, qChar, randb64y(n, use_os=True))
            self.checkRandomChars(charset64s, qChar, randb64y(n, safe=True))
            self.checkRandomChars(charset64s, qChar, randb64y(n, safe=True, use_os=True))

    def test_randb62(self):
        charset62 = set(Notations.BASE62)
        for n in range(100):
            self.checkRandomChars(charset62, n, randb62(n))
            self.checkRandomChars(charset62, n, randb62(n, use_os=True))

    def test_randb16(self):
        charset16 = set(Notations.BASE16)
        for n in range(100):
            self.checkRandomChars(charset16, n, randb16(n).upper())
            self.checkRandomChars(charset16, n, randb16(n, use_os=True).upper())
