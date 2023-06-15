from tests.base_test_case import BaseTestCase
from zeraora.typeclasses import *


class TypeclassesTest(BaseTestCase):

    def testOnionObject(self):
        from decimal import Decimal
        data = {
            'code': 1,
            'info': 'done',
            'data': {
                'order_id': '66a5a0612e2089564b35df189ced94a1',
                'payment': Decimal('3.14'),
                'customer': {
                    'username': 'aixcyi',
                    'uuid': {
                        'wx': 'oj0ed5-TechOtakuSaveTheWorld',
                    },
                },
                'goods': [
                    {
                        'id': '1eb44e7486066eb660322dc65a673d88',
                        'img': '/goods/image/1eb44e7486066eb660322dc65a673d88',
                        'name': '龟苓膏 300g 杯装',
                        'qty': 1,
                    },
                    {
                        'id': '2af405fce650f3ea4b92521155a5019c',
                        'img': '/goods/image/2af405fce650f3ea4b92521155a5019c',
                        'name': '金银花茶 750ml 瓶装',
                        'qty': 2,
                    },
                ],
            },
        }
        plus = {
            'pages': [2, 3, 4, 5, 6],
            'carrier_choices': ('EMS', 'UPS', 'USPS'),
            '__previous': None,
            '0x7c': None,
            '标记': None,
            2333: 6666,
        }

        resp0 = OnionObject(data) | plus
        self.assertEqual(data, ~OnionObject(data))
        self.assertEqual(data['code'], resp0.code)
        self.assertEqual(data['info'], resp0.info)
        self.assertEqual(data['data']['order_id'], resp0.data.order_id)
        self.assertEqual(data['data']['payment'], resp0.data.payment)
        self.assertEqual(data['data']['customer']['username'], resp0.data.customer.username)
        self.assertEqual(data['data']['customer']['uuid']['wx'], resp0.data.customer.uuid.wx)
        self.assertEqual(data['data']['goods'][1]['id'], resp0.data.goods[1].id)
        self.assertEqual(plus['pages'], resp0.pages)
        self.assertEqual(list(plus['carrier_choices']), resp0.carrier_choices)
        self.assertNoAttribute('__private', resp0)
        self.assertNoAttribute(f'_{type(resp0).__name__}__private', resp0)
        self.assertNoAttribute('0x7c', resp0)
        self.assertNoAttribute('2333', resp0)
        self.assertHasAttribute('标记', resp0)

        resp3 = OnionObject(data, depth=3)
        self.assertEqual(data['data']['order_id'], resp3.data.order_id)
        self.assertEqual(data['data']['payment'], resp3.data.payment)
        self.assertEqual(data['data']['customer']['username'], resp3.data.customer.username)
        self.assertEqual(data['data']['customer']['uuid']['wx'], resp3.data.customer.uuid['wx'])
        self.assertEqual(data['data']['goods'][1]['id'], resp3.data.goods[1].id)

        resp2 = OnionObject(data, depth=2)
        self.assertEqual(data['data']['order_id'], resp2.data.order_id)
        self.assertEqual(data['data']['payment'], resp2.data.payment)
        self.assertEqual(data['data']['customer']['username'], resp2.data.customer['username'])
        self.assertEqual(data['data']['customer']['uuid']['wx'], resp2.data.customer['uuid']['wx'])
        self.assertEqual(data['data']['goods'][1]['id'], resp2.data.goods[1]['id'])

        resp1 = OnionObject(data, depth=1)
        self.assertEqual(data['data']['order_id'], resp1.data['order_id'])
        self.assertEqual(data['data']['payment'], resp1.data['payment'])
        self.assertEqual(data['data']['customer']['username'], resp1.data['customer']['username'])
        self.assertEqual(data['data']['customer']['uuid']['wx'], resp1.data['customer']['uuid']['wx'])
        self.assertEqual(data['data']['goods'][1]['id'], resp1.data['goods'][1]['id'])

        r0 = "OnionObject(_OnionObject__depth=-1, id=67, username='aixcyi')"
        r1 = "OnionObject(_OnionObject__depth=-1, id=67, fk=OnionObject(...))"
        self.assertEqual(r0, repr(OnionObject(id=67, username='aixcyi')))
        self.assertEqual(r1, repr(OnionObject(id=67, fk=OnionObject())))

        self.assertRaises(TypeError, OnionObject, [1, 2, 3])

    def testRadixInteger(self):
        ri256 = RadixInteger(33882121, 256)
        self.assertEqual(33882121, int.from_bytes(bytes(ri256), 'little'))
        self.assertEqual(256, ri256.radix)

        ri16 = RadixInteger(33882121, 16)
        self.assertEqual('2050009', ri16.map2str('0123456789ABCDEF'))
        self.assertEqual(b'2050009', ri16.map2bytes(b'0123456789ABCDEF'))

        self.assertTupleEqual(ri16, RadixInteger(ri256, 16))
        self.assertTupleEqual(ri16, RadixInteger([9, 0, 0, 0, 5, 0, 2], 16))
        self.assertTupleEqual(ri256, RadixInteger(b'\x09\x00\x05\x02', 256))

        with self.assertRaises(ValueError):
            _ = RadixInteger(33882121, 1)
        with self.assertRaises(ValueError):
            _ = RadixInteger([1, 2, -3], 10)
        with self.assertRaises(ValueError):
            _ = RadixInteger([1, 2, 16], 16)
        with self.assertRaises(TypeError):
            _ = RadixInteger('meow', 16)

    def testItems(self):
        from zeraora.constants.division import Province, Region

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
        self.assertLengthEqual(34, set(Province.names))
        self.assertLengthEqual(34, set(Province.values))
        self.assertLengthEqual(34, set(Province.items))
        self.assertLengthEqual(34, set(Province.choices))
        self.assertLengthEqual(34, set(Province.numerics))
        self.assertLengthEqual(34, set(Province.shorts))
        self.assertLengthEqual(34, set(Province.codes))
        self.assertLengthEqual(34, set(Province.nicks))
        self.assertLengthEqual(34, set(Province.labels))
        self.assertMemberTypeIs(str, Province.names)
        self.assertMemberTypeIs(str, Province.values)
        self.assertMemberTypeIs(str, Province.items)
        self.assertMemberIsInstance(tuple, Province.choices)
        self.assertMemberTypeIs(int, Province.numerics)
        self.assertMemberTypeIs(str, Province.shorts)
        self.assertMemberTypeIs(str, Province.codes)
        self.assertMemberTypeIs(str, Province.nicks)
        self.assertMemberTypeIs(str, Province.labels)
        self.assertNoAttribute('numbers', Province)
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

        self.assertHasAttribute('boxes', SizeLevel)
        with self.assertRaises(AttributeError):
            _ = SizeLevel.choices

    def testItemsMeta(self):
        with self.assertRaises(AttributeError):
            class UrgencyLevel(Items):
                HIGH = 10, 'WARNING'
                NORMAL = 0, 'INFO'
                LOW = -10, 'DEBUG'

        with self.assertRaises(TypeError):
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

        with self.assertRaises(KeyError):
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
