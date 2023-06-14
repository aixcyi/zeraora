from unittest import TestCase

from zeraora.constants.division import DivisionLevel
from zeraora.structures import *


class ConvertersTest(TestCase):

    def test_division_code_structure(self):
        parts = ('44', '01', '06', '015', '000')
        addr = ''.join(parts)
        self.assertTupleEqual(parts, DivisionCode(*parts))
        self.assertTupleEqual(parts, DivisionCode.fromcode(addr))
        self.assertEqual(addr, str(DivisionCode(*parts)))

    def test_division_structure(self):
        rep = '<Division4 440106015000 元岗 years=[]>'
        div = Division('元岗', DivisionCode('44', '01', '06', '015', '000'), DivisionLevel.TOWNSHIP)
        self.assertEqual(rep, repr(div))
