from unittest import TestCase

from zeraora.datetime import BearTimer


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
