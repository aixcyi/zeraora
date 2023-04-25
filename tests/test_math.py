from decimal import Decimal
from unittest import TestCase

from zeraora import remove_exponent


class MathModuleTest(TestCase):

    def test_remove_exponent(self):
        self.assertEqual(Decimal('3.14'), remove_exponent(Decimal('3.14')))
        self.assertEqual(Decimal('3.14'), remove_exponent(Decimal('3.140')))
        self.assertEqual(Decimal('3.14'), remove_exponent(Decimal('3.1400')))
        self.assertEqual(Decimal('03.14'), remove_exponent(Decimal('03.14')))
        self.assertEqual(Decimal('03.14'), remove_exponent(Decimal('03.140')))
