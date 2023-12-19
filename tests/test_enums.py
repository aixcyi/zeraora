from tests.base_test_case import BaseTestCase
from zeraora.enums import Items


class EnumsTest(BaseTestCase):

    def testItems(self):
        from zeraora.area import Province, Region

        qty_provinces = len(Province)
        self.assertEqual(34, qty_provinces)
        self.assertEqual('ANHUI', Province.ANHUI.name)
        self.assertEqual('34', Province.ANHUI.value)
        self.assertEqual(34, Province.ANHUI.numeric)
        self.assertEqual('皖', Province.ANHUI.short)
        self.assertEqual('AH', Province.ANHUI.code)
        self.assertEqual('安徽', Province.ANHUI.nick)
        self.assertEqual('安徽省', Province.ANHUI.label)
        self.assertEqual(Region.EAST, Province.ANHUI.region)
        self.assertEqual('300000', Province.ANHUI.id_code)
        self.assertEqual('300000000000', Province.ANHUI.statistics_code)
        self.assertEqual(qty_provinces, len(set(Province.names)))
        self.assertEqual(qty_provinces, len(set(Province.values)))
        self.assertEqual(qty_provinces, len(set(Province.items)))
        self.assertEqual(qty_provinces, len(set(Province.choices)))
        self.assertEqual(qty_provinces, len(set(Province.numerics)))
        self.assertEqual(qty_provinces, len(set(Province.shorts)))
        self.assertEqual(qty_provinces, len(set(Province.codes)))
        self.assertEqual(qty_provinces, len(set(Province.nicks)))
        self.assertEqual(qty_provinces, len(set(Province.labels)))
        self.assertEqual(qty_provinces, len(set(Province.asdict())))
        self.assertMemberTypeIs(str, Province.names)
        self.assertMemberTypeIs(str, Province.values)
        self.assertMemberTypeIs(str, Province.items)
        self.assertListEqual(list(zip(Province.values, Province.labels)), Province.choices)
        self.assertMemberTypeIs(int, Province.numerics)
        self.assertMemberTypeIs(str, Province.shorts)
        self.assertMemberTypeIs(str, Province.codes)
        self.assertMemberTypeIs(str, Province.nicks)
        self.assertMemberTypeIs(str, Province.labels)
        self.assertMemberTypeIs(Province, Province.asdict().keys())
        self.assertMemberTypeIs(str, Province.asdict().values())
        self.assertFalse(hasattr(Province, 'numbers'))
        self.assertEqual(len(Region.items), len(set(Province.regions)))
        self.assertEqual('34', str(Province.ANHUI))
        self.assertEqual('Province.ANHUI', repr(Province.ANHUI))
        self.assertTrue(Province.GUANGDONG in Province)
        self.assertTrue('34' in Province)
        self.assertFalse(Region.EAST in Province)
        self.assertFalse(34 in Province)

        class SizeLevel(Items):
            NORMAL = 0, 'bag'
            BIG = 10, 'carton'
            LARGE = 100, 'container'
            __properties__ = 'box',

            @property
            def box(self):
                return self._box_

        self.assertTrue(hasattr(SizeLevel, 'boxes'))
        with self.assertRaises(AttributeError):
            _ = SizeLevel.choices

    def testItemsMeta(self):
        class UrgencyLevel2(Items):
            HIGH = 10, 'WARNING'
            NORMAL = 0, 'INFO'
            LOW = -10, 'DEBUG'
            __properties__ = 'loglevel'

        with self.assertRaises(ValueError):
            class UrgencyLevel3(Items):
                HIGH = 10, 'WARNING'
                NORMAL = 0, 'INFO'
                LOW = -10, 'DEBUG'
                __properties__ = '_loglevel',

        with self.assertRaises(AttributeError):
            class UrgencyLevel4(Items):
                HIGH = 10, 'WARNING'
                NORMAL = 0, 'INFO'
                LOW = -10, 'DEBUG'
                __properties__ = 'value', 'loglevel'

        with self.assertRaises(KeyError):
            class UrgencyLevel5(Items):
                HIGH = 10, 'WARNING'
                NORMAL = 0, 'INFO'
                LOW = -10, 'DEBUG'
                __properties__ = 'generate_next_value',
