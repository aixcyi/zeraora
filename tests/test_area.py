from unittest import TestCase

from zeraora.area import Division, DivisionCode, DivisionLevel


class AreaTest(TestCase):

    def testDivisionCode(self):
        t1 = ('52', '00', '00', '000', '000')
        t2 = ('52', '05', '00', '000', '000')
        t3 = ('52', '05', '02', '000', '000')
        t4 = ('52', '05', '02', '111', '000')
        t5 = ('52', '05', '02', '111', '006')
        self.assertTupleEqual(t1, DivisionCode(*t1))
        self.assertTupleEqual(t2, DivisionCode(*t2))
        self.assertTupleEqual(t3, DivisionCode(*t3))
        self.assertTupleEqual(t4, DivisionCode(*t4))
        self.assertTupleEqual(t5, DivisionCode(*t5))
        self.assertTupleEqual(t1, DivisionCode.fromcode(''.join(t1[:1])))
        self.assertTupleEqual(t2, DivisionCode.fromcode(''.join(t2[:2])))
        self.assertTupleEqual(t3, DivisionCode.fromcode(''.join(t3[:3])))
        self.assertTupleEqual(t4, DivisionCode.fromcode(''.join(t4[:4])))
        self.assertTupleEqual(t5, DivisionCode.fromcode(''.join(t5[:5])))
        self.assertEqual(1, DivisionCode(*t1).level)
        self.assertEqual(2, DivisionCode(*t2).level)
        self.assertEqual(3, DivisionCode(*t3).level)
        self.assertEqual(4, DivisionCode(*t4).level)
        self.assertEqual(5, DivisionCode(*t5).level)
        self.assertTupleEqual(t1, DivisionCode(*t5).tocode(1))
        self.assertTupleEqual(t2, DivisionCode(*t5).tocode(2))
        self.assertTupleEqual(t3, DivisionCode(*t5).tocode(3))
        self.assertTupleEqual(t4, DivisionCode(*t5).tocode(4))
        self.assertTupleEqual(t5, DivisionCode(*t5).tocode(5))
        self.assertEqual(''.join(t1), DivisionCode(*t5).tostr(1))
        self.assertEqual(''.join(t2), DivisionCode(*t5).tostr(2))
        self.assertEqual(''.join(t3), DivisionCode(*t5).tostr(3))
        self.assertEqual(''.join(t4), DivisionCode(*t5).tostr(4))
        self.assertEqual(''.join(t5), DivisionCode(*t5).tostr(5))

        p1 = ('', '52', '0502111006')
        p2 = ('52', '05', '02111006')
        p3 = ('5205', '02', '111006')
        p4 = ('520502', '111', '006')
        p5 = ('520502111', '006', '')
        self.assertTupleEqual(p1, DivisionCode(*t5).partition(1))
        self.assertTupleEqual(p2, DivisionCode(*t5).partition(2))
        self.assertTupleEqual(p3, DivisionCode(*t5).partition(3))
        self.assertTupleEqual(p4, DivisionCode(*t5).partition(4))
        self.assertTupleEqual(p5, DivisionCode(*t5).partition(5))

    def testDivision(self):
        rep = '<Division5 520502111006 猫猫洞 years=[]>'
        div = Division('猫猫洞', DivisionCode('52', '05', '02', '111', '006'), DivisionLevel.VILLAGE)
        self.assertEqual(rep, repr(div))
