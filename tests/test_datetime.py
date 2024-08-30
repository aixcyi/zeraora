from datetime import date, timedelta
from unittest import TestCase

from zeraora.datetime import DateTime, DateRange, BearTimer


class DateTimeTest(TestCase):

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
                _ = sum(range(100_0000))
        with self.assertLogs('zeraora.datetime', 'DEBUG'):
            @BearTimer()
            def calc_summary(length: int) -> int:
                return sum(range(length))

            _ = calc_summary(100_0000)

    def testDateTime_of_week(self):
        self.assertEqual(date(2023, 5, 28), DateTime.of_week(2023, 22, 0, sunday_first=True))
        self.assertEqual(date(2023, 5, 29), DateTime.of_week(2023, 22, 1))
        self.assertEqual(date(2023, 5, 30), DateTime.of_week(2023, 22, 2))
        self.assertEqual(date(2023, 5, 31), DateTime.of_week(2023, 22, 3))
        self.assertEqual(date(2023, 6, 1), DateTime.of_week(2023, 22, 4))
        self.assertEqual(date(2023, 6, 2), DateTime.of_week(2023, 22, 5))
        self.assertEqual(date(2023, 6, 3), DateTime.of_week(2023, 22, 6))
        self.assertEqual(date(2023, 6, 4), DateTime.of_week(2023, 22, 0))

    def testDateTime_get_week_in_year(self):
        self.assertEqual(22, DateTime(2023, 5, 28).get_week_in_year(sunday_first=True))
        self.assertEqual(22, DateTime(2023, 5, 29).get_week_in_year())
        self.assertEqual(22, DateTime(2023, 5, 30).get_week_in_year())
        self.assertEqual(22, DateTime(2023, 5, 31).get_week_in_year())
        self.assertEqual(22, DateTime(2023, 6, 1).get_week_in_year())
        self.assertEqual(22, DateTime(2023, 6, 2).get_week_in_year())
        self.assertEqual(22, DateTime(2023, 6, 3).get_week_in_year())
        self.assertEqual(22, DateTime(2023, 6, 4).get_week_in_year())

    def testDateRangeTest_by_week(self):
        # Monday First / Sunday First
        self.assertTupleEqual(
            tuple(date(2023, 5, 29) + timedelta(days=i) for i in range(7)),
            tuple(DateRange.by_week(2023, 22)),
        )
        self.assertTupleEqual(
            tuple(date(2023, 5, 28) + timedelta(days=i) for i in range(7)),
            tuple(DateRange.by_week(2023, 22, sunday_first=True)),
        )
