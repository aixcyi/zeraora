from datetime import date, timedelta, datetime
from unittest import TestCase

from zeraora.daytime import delta2hms, delta2ms, delta2s, get_week_in_year, get_week_range, get_week_side, wdate


class DaytimeTest(TestCase):
    delta_t0 = timedelta()
    delta_t1 = timedelta(seconds=3, milliseconds=140, microseconds=1590)
    delta_t2 = timedelta(seconds=18030, milliseconds=140, microseconds=1590)

    def test_delta2hms(self):
        self.assertTupleEqual((0, 0, 0), delta2hms(self.delta_t0))
        self.assertTupleEqual((0, 0, 3.14159), delta2hms(self.delta_t1))
        self.assertTupleEqual((5, 0, 30.14159), delta2hms(self.delta_t2))

    def test_delta2ms(self):
        self.assertTupleEqual((0, 0), delta2ms(self.delta_t0))
        self.assertTupleEqual((0, 3.14159), delta2ms(self.delta_t1))
        self.assertTupleEqual((300, 30.14159), delta2ms(self.delta_t2))

    def test_delta2s(self):
        self.assertEqual(0, delta2s(self.delta_t0))
        self.assertEqual(3.14159, delta2s(self.delta_t1))
        self.assertEqual(18030.14159, delta2s(self.delta_t2))

    def test_wdate(self):
        self.assertEqual(date(2023, 5, 28), wdate(2023, 22, 0, sunday_first=True))
        self.assertEqual(date(2023, 5, 29), wdate(2023, 22, 1))
        self.assertEqual(date(2023, 5, 30), wdate(2023, 22, 2))
        self.assertEqual(date(2023, 5, 31), wdate(2023, 22, 3))
        self.assertEqual(date(2023, 6, 1), wdate(2023, 22, 4))
        self.assertEqual(date(2023, 6, 2), wdate(2023, 22, 5))
        self.assertEqual(date(2023, 6, 3), wdate(2023, 22, 6))
        self.assertEqual(date(2023, 6, 4), wdate(2023, 22, 0))

    def test_get_week_range(self):
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
        self.assertRaises(ValueError, get_week_range, 2023, 21, 6)
        self.assertRaises(ValueError, get_week_range, 2023, 23, 5)
        self.assertEqual((dateset_mf[0], dateset_mf[-1]), get_week_side(2023, 22))
        self.assertEqual((dateset_sf[0], dateset_sf[-1]), get_week_side(2023, 22, sunday_first=True))
        self.assertEqual((dateset_mf5[0], dateset_mf5[-1]), get_week_side(2023, 22, 5))
        self.assertEqual((dateset_mf6[0], dateset_mf6[-1]), get_week_side(2023, 22, 6))
        self.assertEqual((dateset_sf5[0], dateset_sf5[-1]), get_week_side(2023, 22, 5, sunday_first=True))
        self.assertEqual((dateset_sf6[0], dateset_sf6[-1]), get_week_side(2023, 22, 6, sunday_first=True))
        self.assertRaises(ValueError, get_week_side, 2023, 21, 6)
        self.assertRaises(ValueError, get_week_side, 2023, 23, 5)

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
        self.assertRaises(ValueError, get_week_in_year, timedelta(days=1))
        self.assertRaises(ValueError, get_week_in_year, 2023.6, 1)
        self.assertRaises(ValueError, get_week_in_year, '2023', '6', '1')
