import unittest

from zeraora.logging import *


class LoggingTest(unittest.TestCase):

    def testBearStopwatch(self):
        bear = BearStopwatch()
        with self.assertLogs(BearStopwatch.LOGGER, 'DEBUG'):
            bear.start()
        with self.assertLogs(BearStopwatch.LOGGER, 'DEBUG'):
            bear.lap('Hello, meow.')
        with self.assertLogs(BearStopwatch.LOGGER, 'DEBUG'):
            bear.stop()
        with self.assertLogs(BearStopwatch.LOGGER, 'DEBUG'):
            with BearStopwatch():
                _ = sum(range(10_0000))
        with self.assertLogs(BearStopwatch.LOGGER, 'DEBUG'):
            @BearStopwatch()
            def calc_summary(length: int) -> int:
                return sum(range(length))

            _ = calc_summary(10_0000)
