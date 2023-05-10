from decimal import Decimal

from tests.base_test_case import BaseTestCase
from zeraora import OnionObject, RadixInteger


class TypeclassesTest(BaseTestCase):

    def test_onion_object(self):
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

    def test_radix_integer(self):
        ri256 = RadixInteger(2217343354, 256)
        self.assertEqual(2217343354, int.from_bytes(bytes(ri256), 'little'))

        ri16 = RadixInteger(2217343354, 16)
        self.assertEqual('8429F97A', ri16.map2str('0123456789ABCDEF'))
        self.assertEqual(b'8429F97A', ri16.map2bytes(b'0123456789ABCDEF'))
