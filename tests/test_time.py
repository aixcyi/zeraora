from datetime import timedelta
from random import random
from time import sleep
from unittest import TestCase

from zeraora import delta2hms, delta2ms, delta2s, BearTimer


class TimeModuleTest(TestCase):

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

    def test_bear_timer_via_object(self):
        bear = BearTimer()
        bear.start()
        for _ in range(3):
            st = random()
            sleep(st)
            bear.step(st)
        bear.stop()
        self.assertEqual(1, 1)

    def test_bear_timer_via_context(self):
        with BearTimer():
            return sum(range(100_0000))

    def test_bear_timer_via_decorator(self):

        @BearTimer()
        def calc_summary(length: int) -> int:
            return sum(range(length))

        _ = calc_summary(100_0000)
