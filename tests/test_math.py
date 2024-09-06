import unittest

from tests.base_test_case import BaseTestCase
from zeraora.math import *


class MathsTest(BaseTestCase):

    def test_Decimal(self):
        self.assertAttribute('E', Decimal)
        self.assertAttribute('PI', Decimal)
        self.assertAttribute('NAN', Decimal)
        self.assertAttribute('ONE', Decimal)
        self.assertAttribute('ZERO', Decimal)
        self.assertTrue(Decimal.NAN.is_nan())
        self.assertTrue(Decimal.ZERO.is_zero())
        self.assertTrue(Decimal.ONE == Decimal('1'))
        self.assertEqual(Decimal('3.14'), Decimal('3.14').remove_exponent())
        self.assertEqual(Decimal('3.14'), Decimal('3.140').remove_exponent())
        self.assertEqual(Decimal('3.14'), Decimal('3.1400').remove_exponent())
        self.assertEqual(Decimal('03.14'), Decimal('03.14').remove_exponent())
        self.assertEqual(Decimal('03.14'), Decimal('03.140').remove_exponent())

    def test_remove_exponent(self):
        self.assertEqual(Decimal('3.14'), remove_exponent(Decimal('3.14')))
        self.assertEqual(Decimal('3.14'), remove_exponent(Decimal('3.140')))
        self.assertEqual(Decimal('3.14'), remove_exponent(Decimal('3.1400')))
        self.assertEqual(Decimal('03.14'), remove_exponent(Decimal('03.14')))
        self.assertEqual(Decimal('03.14'), remove_exponent(Decimal('03.140')))

    def test_absolute(self):
        self.assertTupleEqual((True, 1980), absolute(1980))
        self.assertTupleEqual((False, 1980), absolute(-1980))
        self.assertTupleEqual((True, 0), absolute(0))
        self.assertTupleEqual((True, 0), absolute(-0))
        self.assertTupleEqual((True, 0), absolute(0.0))
        self.assertTupleEqual((True, 0), absolute(-0.0))

    # noinspection PyTypeChecker
    def test_bitstream(self):
        self.assertTupleEqual((1, 2, 64), tuple(bitstream(67)))
        self.assertTupleEqual((-1, -2, -64), tuple(bitstream(-67)))
        self.assertTupleEqual((-1, -2, -8, -32), tuple(bitstream(-43)))
        self.assertTupleEqual(tuple(), tuple(bitstream(0)))
        self.assertTupleEqual(tuple(), tuple(bitstream(-0)))
        self.assertTupleEqual(tuple(), tuple(bitstream(0.0)))
        self.assertTupleEqual(tuple(), tuple(bitstream(3.14)))

    def test_digitstream(self):
        digits = digitstream(1008612, 16)
        mapper = '0123456789abcdef'.__getitem__
        result = ''.join(map(mapper, digits))[::-1]
        control = hex(1008612)[2:]
        self.assertEqual(control, result)
        self.assertTupleEqual(tuple(), tuple(digitstream(1008612, 1)))
        self.assertTupleEqual(tuple(), tuple(digitstream(1008612, 0)))
        self.assertTupleEqual(tuple(), tuple(digitstream(1008612, -1)))


if __name__ == '__main__':
    unittest.main()
