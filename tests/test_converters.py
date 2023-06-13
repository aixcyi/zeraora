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

    def test_wdate(self):
        self.assertEqual(date(2023, 5, 28), wdate(2023, 22, 0, sunday_first=True))
        self.assertEqual(date(2023, 5, 29), wdate(2023, 22, 1))
        self.assertEqual(date(2023, 5, 30), wdate(2023, 22, 2))
        self.assertEqual(date(2023, 5, 31), wdate(2023, 22, 3))
        self.assertEqual(date(2023, 6, 1), wdate(2023, 22, 4))
        self.assertEqual(date(2023, 6, 2), wdate(2023, 22, 5))
        self.assertEqual(date(2023, 6, 3), wdate(2023, 22, 6))
        self.assertEqual(date(2023, 6, 4), wdate(2023, 22, 0))

    def test_get_week_range_and_side(self):
        # Monday First / Sunday First
        dateset_mf = tuple(date(2023, 5, 29) + timedelta(days=i) for i in range(7))
        dateset_sf = tuple(date(2023, 5, 28) + timedelta(days=i) for i in range(7))
        dateset_mf5 = tuple(d for d in dateset_mf if d.month == 5)
        dateset_mf6 = tuple(d for d in dateset_mf if d.month == 6)
        dateset_sf5 = tuple(d for d in dateset_sf if d.month == 5)
        dateset_sf6 = tuple(d for d in dateset_sf if d.month == 6)
        self.assertEqual(dateset_mf, get_week_range(2023, 22))
        self.assertEqual(dateset_sf, get_week_range(2023, 22, sunday_first=True))
        self.assertEqual(dateset_mf5, get_week_range(2023, 22, 5))
        self.assertEqual(dateset_mf6, get_week_range(2023, 22, 6))
        self.assertEqual(dateset_sf5, get_week_range(2023, 22, 5, sunday_first=True))
        self.assertEqual(dateset_sf6, get_week_range(2023, 22, 6, sunday_first=True))
        self.assertEqual((dateset_mf[0], dateset_mf[-1]), get_week_side(2023, 22))
        self.assertEqual((dateset_sf[0], dateset_sf[-1]), get_week_side(2023, 22, sunday_first=True))
        self.assertEqual((dateset_mf5[0], dateset_mf5[-1]), get_week_side(2023, 22, 5))
        self.assertEqual((dateset_mf6[0], dateset_mf6[-1]), get_week_side(2023, 22, 6))
        self.assertEqual((dateset_sf5[0], dateset_sf5[-1]), get_week_side(2023, 22, 5, sunday_first=True))
        self.assertEqual((dateset_sf6[0], dateset_sf6[-1]), get_week_side(2023, 22, 6, sunday_first=True))

    def test_get_week_in_year(self):
        self.assertEqual(22, get_week_in_year(date(2023, 6, 1)))
        self.assertEqual(22, get_week_in_year(datetime(2023, 6, 1, 8, 0, 0)))
        self.assertEqual(22, get_week_in_year(2023, 6, 1))
        self.assertEqual(22, get_week_in_year(2023, 6, 1, 8, 0, 0))
        self.assertEqual(22, get_week_in_year(date(2023, 5, 28), sunday_first=True))
        self.assertEqual(22, get_week_in_year(date(2023, 5, 29)))
        self.assertEqual(22, get_week_in_year(date(2023, 5, 30)))
        self.assertEqual(22, get_week_in_year(date(2023, 5, 31)))
        self.assertEqual(22, get_week_in_year(date(2023, 6, 1)))
        self.assertEqual(22, get_week_in_year(date(2023, 6, 2)))
        self.assertEqual(22, get_week_in_year(date(2023, 6, 3)))
        self.assertEqual(22, get_week_in_year(date(2023, 6, 4)))

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

    def test_trulize(self):
        self.assertEqual(True, true(True))
        self.assertEqual(True, true('True'))
        self.assertEqual(True, true('true'))
        self.assertEqual(True, true('TRUE'))
        self.assertEqual(True, true(1))
        self.assertEqual(True, true('1'))
        self.assertEqual(False, true(False))
        self.assertEqual(False, true('False'))
        self.assertEqual(False, true('false'))
        self.assertEqual(False, true('FALSE'))
        self.assertEqual(False, true(0))
        self.assertEqual(False, true('0'))

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
