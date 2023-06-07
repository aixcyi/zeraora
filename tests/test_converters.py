from datetime import date, timedelta, datetime
from decimal import Decimal
from unittest import TestCase
from uuid import UUID

from zeraora.converters import *


class ConvertersTest(TestCase):

    def test_remove_exponent(self):
        self.assertEqual(Decimal('3.14'), remove_exponent(Decimal('3.14')))
        self.assertEqual(Decimal('3.14'), remove_exponent(Decimal('3.140')))
        self.assertEqual(Decimal('3.14'), remove_exponent(Decimal('3.1400')))
        self.assertEqual(Decimal('03.14'), remove_exponent(Decimal('03.14')))
        self.assertEqual(Decimal('03.14'), remove_exponent(Decimal('03.140')))

    def test_delta2hms(self):
        self.assertEqual((0, 0, 0), delta2hms(timedelta()))
        self.assertEqual((0, 0, 3.14159), delta2hms(timedelta(seconds=3, milliseconds=140, microseconds=1590)))
        self.assertEqual((5, 0, 30.14159), delta2hms(timedelta(seconds=18030, milliseconds=140, microseconds=1590)))

    def test_delta2ms(self):
        self.assertEqual((0, 0), delta2ms(timedelta()))
        self.assertEqual((0, 3.14159), delta2ms(timedelta(seconds=3, milliseconds=140, microseconds=1590)))
        self.assertEqual((300, 30.14159), delta2ms(timedelta(seconds=18030, milliseconds=140, microseconds=1590)))

    def test_delta2s(self):
        self.assertEqual(0, delta2s(timedelta()))
        self.assertEqual(3.14159, delta2s(timedelta(seconds=3, milliseconds=140, microseconds=1590)))
        self.assertEqual(18030.14159, delta2s(timedelta(seconds=18030, milliseconds=140, microseconds=1590)))

    def test_represent(self):
        self.assertEqual('"string"', represent('string'))
        self.assertEqual('[2012-01-23]', represent(date(2012, 1, 23)))
        self.assertEqual('[0d+3.141590s]', represent(timedelta(seconds=3, milliseconds=140, microseconds=1590)))
        self.assertEqual('[3d+3599.000000s]', represent(timedelta(days=3, hours=1, seconds=-1)))
        self.assertEqual('[2012-01-23 08:29:59,000000]', represent(datetime(2012, 1, 23, 8, 29, 59)))
        self.assertEqual('d6d0b9fac9fabbeed4daedc1d0a1d2ed', represent(UUID('d6d0b9fa-c9fa-bbee-d4da-edc1d0a1d2ed')))
        self.assertEqual('(2, 3, 5, 7)', represent((2, 3, 5, 7)))
        self.assertEqual('[2, 3, 5, 7]', represent([2, 3, 5, 7]))
        self.assertEqual('{2, 3, 5, 7}', represent({2, 3, 5, 7}))
        self.assertEqual("{200: 'ok', 404: 'no found'}", represent({200: 'ok', 404: 'no found'}))

    def test_datasize(self):
        self.assertEqual(1, datasize('1B'))
        self.assertEqual(1.0, datasize('8b'))
        self.assertEqual(17 * 1000, datasize('17KB'))
        self.assertEqual(17 * 1024, datasize('17KiB'))
        self.assertEqual(17 * 1000 / 8, datasize('17Kb'))
        self.assertEqual(17 * 1024 / 8, datasize('17Kib'))
        self.assertEqual(29 * 1000 * 1000, datasize('29MB'))
        self.assertEqual(29 * 1024 * 1024, datasize('29MiB'))
        self.assertEqual(29 * 1000 * 1000 / 8, datasize('29Mb'))
        self.assertEqual(29 * 1024 * 1024 / 8, datasize('29Mib'))
        self.assertEqual(31 * 1000 * 1000 * 1000, datasize('31 GB'))
        self.assertEqual(31 * 1024 * 1024 * 1024, datasize('31 GiB'))
        self.assertEqual(31 * 1000 * 1000 * 1000 / 8, datasize('31 Gb'))
        self.assertEqual(31 * 1024 * 1024 * 1024 / 8, datasize('31 Gib'))
        self.assertEqual(0, datasize('47'))
        self.assertEqual(0, datasize('47KiBytes'))

    def test_safecast(self):
        self.assertEqual(1234, safecast(int, '1234'))
        self.assertEqual(None, safecast(int, '12a4'))
        self.assertEqual(None, safecast(int, None))
        self.assertEqual(1234, safecast(int, '1234', default=5678))
        self.assertEqual(5678, safecast(int, '12a4', default=5678))
        self.assertEqual('中文', safecast(b'\xd6\xd0\xce\xc4'.decode, 'GBK', default='meow'))
        self.assertEqual('meow', safecast(b'\xd6\xd0\xce\xc4'.decode, 'UTF8', default='meow'))
        self.assertEqual(3, safecast([3, 14].__getitem__, 0, default=-1))
        self.assertEqual(-1, safecast([3, 14].__getitem__, 315, IndexError, default=-1))
