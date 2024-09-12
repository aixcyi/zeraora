import unittest
from datetime import datetime

from zeraora.datetime import *


class DatetimeTest(unittest.TestCase):

    def testBearTimer(self):
        bear = BearTimer()
        with self.assertLogs('zeraora.datetime', 'DEBUG'):
            bear.start()
        with self.assertLogs('zeraora.datetime', 'DEBUG'):
            bear.lap('Hello, meow.')
        with self.assertLogs('zeraora.datetime', 'DEBUG'):
            bear.stop()
        with self.assertLogs('zeraora.datetime', 'DEBUG'):
            with BearTimer():
                _ = sum(range(10_0000))
        with self.assertLogs('zeraora.datetime', 'DEBUG'):
            @BearTimer()
            def calc_summary(length: int) -> int:
                return sum(range(length))

            _ = calc_summary(10_0000)

    def test_is_leap(self):
        self.assertFalse(is_leap(1700), '1700 is not a leap year.')
        self.assertFalse(is_leap(1800), '1800 is not a leap year.')
        self.assertFalse(is_leap(1970), '1970 is not a leap year.')
        self.assertTrue(is_leap(2000), '2000 is a leap year.')
        self.assertTrue(is_leap(2020), '2020 is a leap year.')
        self.assertFalse(is_leap(2021), '2021 is not a leap year.')
        self.assertFalse(is_leap(2022), '2022 is not a leap year.')
        self.assertFalse(is_leap(2023), '2023 is not a leap year.')
        self.assertTrue(is_leap(2024), '2024 is a leap year.')

    def test_get_last_monthday(self):
        self.assertEqual(28, get_last_monthday(1970, 2))
        self.assertEqual(29, get_last_monthday(2020, 2))
        self.assertEqual(28, get_last_monthday(2021, 2))
        self.assertEqual(28, get_last_monthday(2022, 2))
        self.assertEqual(28, get_last_monthday(2023, 2))
        self.assertEqual(31, get_last_monthday(2024, 1))
        self.assertEqual(29, get_last_monthday(2024, 2))
        self.assertEqual(31, get_last_monthday(2024, 3))
        self.assertEqual(30, get_last_monthday(2024, 4))
        self.assertEqual(31, get_last_monthday(2024, 5))
        self.assertEqual(30, get_last_monthday(2024, 6))
        self.assertEqual(31, get_last_monthday(2024, 7))
        self.assertEqual(31, get_last_monthday(2024, 8))
        self.assertEqual(30, get_last_monthday(2024, 9))
        self.assertEqual(31, get_last_monthday(2024, 10))
        self.assertEqual(30, get_last_monthday(2024, 11))
        self.assertEqual(31, get_last_monthday(2024, 12))

    def testDatetime(self):
        self.assertEqual(datetime(2011, 1, 29), Datetime.fromcalendar(2011, 4, 6))
        self.assertEqual(datetime(2011, 1, 30), Datetime.fromcalendar(2011, 4, 0))
        self.assertEqual(datetime(2011, 1, 31), Datetime.fromcalendar(2011, 5, 1))
        self.assertEqual(datetime(2011, 2, 1), Datetime.fromcalendar(2011, 5, 2))
        self.assertEqual(datetime(2011, 2, 2), Datetime.fromcalendar(2011, 5, 3))
        self.assertEqual(datetime(2011, 2, 3), Datetime.fromcalendar(2011, 5, 4))
        self.assertEqual(datetime(2011, 2, 4), Datetime.fromcalendar(2011, 5, 5))
        self.assertEqual(datetime(2011, 2, 5), Datetime.fromcalendar(2011, 5, 6))
        self.assertEqual(datetime(2011, 2, 6), Datetime.fromcalendar(2011, 5, 0))
        self.assertEqual(datetime(2011, 2, 7), Datetime.fromcalendar(2011, 6, 1))
        self.assertEqual(datetime(2011, 2, 8), Datetime.fromcalendar(2011, 6, 2))

        self.assertEqual(datetime(2011, 1, 29), Datetime.fromcalendar(2011, 4, 6, sunday_first=True))
        self.assertEqual(datetime(2011, 1, 30), Datetime.fromcalendar(2011, 5, 0, sunday_first=True))
        self.assertEqual(datetime(2011, 1, 31), Datetime.fromcalendar(2011, 5, 1, sunday_first=True))
        self.assertEqual(datetime(2011, 2, 1), Datetime.fromcalendar(2011, 5, 2, sunday_first=True))
        self.assertEqual(datetime(2011, 2, 2), Datetime.fromcalendar(2011, 5, 3, sunday_first=True))
        self.assertEqual(datetime(2011, 2, 3), Datetime.fromcalendar(2011, 5, 4, sunday_first=True))
        self.assertEqual(datetime(2011, 2, 4), Datetime.fromcalendar(2011, 5, 5, sunday_first=True))
        self.assertEqual(datetime(2011, 2, 5), Datetime.fromcalendar(2011, 5, 6, sunday_first=True))
        self.assertEqual(datetime(2011, 2, 6), Datetime.fromcalendar(2011, 6, 0, sunday_first=True))
        self.assertEqual(datetime(2011, 2, 7), Datetime.fromcalendar(2011, 6, 1, sunday_first=True))
        self.assertEqual(datetime(2011, 2, 8), Datetime.fromcalendar(2011, 6, 2, sunday_first=True))

        self.assertTupleEqual((2011, 4, 6), Datetime(2011, 1, 29).calendar())
        self.assertTupleEqual((2011, 4, 0), Datetime(2011, 1, 30).calendar())
        self.assertTupleEqual((2011, 5, 1), Datetime(2011, 1, 31).calendar())
        self.assertTupleEqual((2011, 5, 2), Datetime(2011, 2, 1).calendar())
        self.assertTupleEqual((2011, 5, 3), Datetime(2011, 2, 2).calendar())
        self.assertTupleEqual((2011, 5, 4), Datetime(2011, 2, 3).calendar())
        self.assertTupleEqual((2011, 5, 5), Datetime(2011, 2, 4).calendar())
        self.assertTupleEqual((2011, 5, 6), Datetime(2011, 2, 5).calendar())
        self.assertTupleEqual((2011, 5, 0), Datetime(2011, 2, 6).calendar())
        self.assertTupleEqual((2011, 6, 1), Datetime(2011, 2, 7).calendar())
        self.assertTupleEqual((2011, 6, 2), Datetime(2011, 2, 8).calendar())

        self.assertTupleEqual((2011, 4, 6), Datetime(2011, 1, 29).calendar(sunday_first=True))
        self.assertTupleEqual((2011, 5, 0), Datetime(2011, 1, 30).calendar(sunday_first=True))
        self.assertTupleEqual((2011, 5, 1), Datetime(2011, 1, 31).calendar(sunday_first=True))
        self.assertTupleEqual((2011, 5, 2), Datetime(2011, 2, 1).calendar(sunday_first=True))
        self.assertTupleEqual((2011, 5, 3), Datetime(2011, 2, 2).calendar(sunday_first=True))
        self.assertTupleEqual((2011, 5, 4), Datetime(2011, 2, 3).calendar(sunday_first=True))
        self.assertTupleEqual((2011, 5, 5), Datetime(2011, 2, 4).calendar(sunday_first=True))
        self.assertTupleEqual((2011, 5, 6), Datetime(2011, 2, 5).calendar(sunday_first=True))
        self.assertTupleEqual((2011, 6, 0), Datetime(2011, 2, 6).calendar(sunday_first=True))
        self.assertTupleEqual((2011, 6, 1), Datetime(2011, 2, 7).calendar(sunday_first=True))

        today = datetime(2011, 2, 3)
        self.assertEqual(today, Datetime.fromdatetime(today))
        self.assertEqual(today, Datetime.of(today))
        self.assertEqual(today, Datetime.of(today).replace(standard=True))
        self.assertIs(Datetime, type(Datetime.fromdatetime(today)))
        self.assertIs(Datetime, type(Datetime.of(today)))
        self.assertIs(datetime, type(Datetime.of(today).replace(standard=True)))
