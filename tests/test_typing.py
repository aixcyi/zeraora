import json
from datetime import date, datetime, timedelta
from unittest import TestCase
from uuid import UUID

from zeraora import casting, represent, OnionObject, ReprMixin

SUBJECT_CATEGORY = {
    1: '工学', 8: '经济学',
    2: '哲学', 9: '教育学',
    3: '法学', 10: '历史学',
    4: '文学', 11: '管理学',
    5: '理学', 12: '军事学',
    6: '农学', 13: '艺术学',
    7: '医学',
}


def _age(birth: datetime) -> int:
    return datetime.now().year - birth.year


class Student(ReprMixin,  # 必须作为第一个父类
              OnionObject):

    def __init__(self, **kwargs):
        self.number = '10086020'
        self.name = '叶秋然'
        self.gender = False
        self.birthday = date(2000, 3, 15)
        self.join_date = datetime(2018, 8, 29, 16, 29)
        self.graduated = False
        self.grade = 3
        self.subject = 1
        self.leader = False
        super().__init__(**kwargs)

    @property
    def join_year(self):
        return self.join_date.year

    class AttributeMeta:
        name = '姓名'
        birthday: _age = '年龄'
        join_year = '入学年份'
        join_date = '报道时间'

    class TagMeta:
        gender = '男', '女'  # 前面表示False，后面表示True
        subject = SUBJECT_CATEGORY
        grade = ['大一', '大二', '大三', '大四', '大五']
        graduated = '已毕业'  # False不显示，True则显示
        leader = '', '班长'
        number = object()  # 非法值


class TypingModuleTest(TestCase):
    def test_casting(self):
        self.assertEqual(1234, casting(int, '1234'))
        self.assertEqual(None, casting(int, '12a4'))
        self.assertEqual(None, casting(int, None))
        self.assertEqual(1234, casting(int, '1234', default=5678))
        self.assertEqual(5678, casting(int, '12a4', default=5678))
        self.assertEqual(5678, casting(None, '1234', default=5678))
        self.assertEqual('中文', casting(b'\xd6\xd0\xce\xc4'.decode, 'GBK', default='meow'))
        self.assertEqual('meow', casting(b'\xd6\xd0\xce\xc4'.decode, 'UTF8', default='meow'))
        self.assertEqual(3, casting([3, 14].__getitem__, 0, default=-1))
        self.assertEqual(-1, casting([3, 14].__getitem__, 315, IndexError, default=-1))

    def test_represent(self):
        self.assertEqual('"string"', represent('string'))
        self.assertEqual('[2012-01-23]', represent(date(2012, 1, 23)))
        self.assertEqual('[2012-01-23 08:29:59,000000]', represent(datetime(2012, 1, 23, 8, 29, 59)))
        self.assertEqual('[3d,3599s,0μs]', represent(timedelta(days=3, hours=1, seconds=-1)))
        self.assertEqual('d6d0b9fac9fabbeed4daedc1d0a1d2ed', represent(UUID('d6d0b9fa-c9fa-bbee-d4da-edc1d0a1d2ed')))
        self.assertEqual('(2, 3, 5, 7)', represent((2, 3, 5, 7)))
        self.assertEqual('[2, 3, 5, 7]', represent([2, 3, 5, 7]))
        self.assertEqual('{2, 3, 5, 7}', represent({2, 3, 5, 7}))
        self.assertEqual("{200: 'ok', 404: 'no found'}", represent({200: 'ok', 404: 'no found'}))

    def test_onion_object(self):
        raw = {
            'code': 0,
            'message': 'done',
            'data': {
                'order': {
                    'id': '66a5a0612e2089564b35df189ced94a1',
                    'carrier': 'EMS',
                    'tracking': '948687112837587323',
                    'customer_id': 'edd39a6919447fe904fc762229293f77',
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
            },
        }

        plus = {
            '0x7c': None,
            '__private': None,
            'carrier_choices': ('EMS', 'UPS', 'USPS'),
            'template': 'templates/order/detail.html',
            'pages': [2, 3, 4, 5, 6],
            'page': {
                'current': 1,
                'prev': None,
                'next': '?page=2',
            }
        }

        resp0 = OnionObject(raw)
        self.assertEqual(raw['code'], resp0.code)
        self.assertEqual(raw['message'], resp0.message)
        self.assertEqual(raw['data']['order']['id'], resp0.data.order.id)
        self.assertEqual(raw['data']['order']['goods'][1]['id'], resp0.data.order.goods[1].id)

        data = {**raw, **plus}

        resp1 = OnionObject(data)
        self.assertEqual(False, hasattr(resp1, '__private'))
        self.assertEqual(False, hasattr(resp1, f'_{type(resp1).__name__}__private'))

        resp2 = OnionObject(data, page=1, link={'prev': None, 'next': '?page=2'})
        self.assertEqual(['EMS', 'UPS', 'USPS'], resp2.carrier_choices)
        self.assertEqual(1, resp2.page)
        self.assertEqual(None, resp2.link.prev)
        self.assertEqual('?page=2', resp2.link.next)

        resp3 = OnionObject(data, recurse=False, page=1, link={'prev': None, 'next': '?page=2'})
        self.assertEqual(data['code'], resp3.code)
        self.assertEqual(data['message'], resp3.message)
        self.assertEqual(data['data']['order']['id'], resp3.data['order']['id'])
        self.assertEqual(data['data']['order']['goods'][1]['id'], resp3.data['order']['goods'][1]['id'])
        self.assertEqual(1, resp3.page)
        self.assertEqual(None, resp3.link['prev'])
        self.assertEqual('?page=2', resp3.link['next'])

        resp4 = OnionObject(raw)
        jsons = json.dumps(raw, ensure_ascii=False)
        self.assertEqual(raw, ~resp4)
        self.assertEqual(jsons, str(resp4))

        resp4 |= plus
        self.assertEqual(repr(resp1), repr(resp4))

    def test_repr_mixin(self):
        r00 = '<Student 男 工学 大四 姓名="叶秋然" 年龄=23 入学年份=2018 报道时间=[2018-08-29 16:29:00,000000]>'
        r01 = '<Student 女 工学 大四 姓名="叶嫣然" 年龄=23 入学年份=2018 报道时间=[2018-08-29 16:29:00,000000]>'
        r02 = '<Student 男 哲学 大四 姓名="叶秋然" 年龄=23 入学年份=2018 报道时间=[2018-08-29 16:29:00,000000]>'
        r03 = '<Student 男 工学 大四 姓名="叶秋然" 年龄=24 入学年份=2018 报道时间=[2018-08-29 16:29:00,000000]>'
        r04 = '<Student 男 工学 大二 姓名="叶秋然" 年龄=23 入学年份=2018 报道时间=[2018-08-29 16:29:00,000000]>'
        r05 = '<Student 男 工学 大四 已毕业 姓名="叶秋然" 年龄=23 入学年份=2018 报道时间=[2018-08-29 16:29:00,000000]>'
        r06 = '<Student 男 工学 大四 班长 姓名="叶秋然" 年龄=23 入学年份=2018 报道时间=[2018-08-29 16:29:00,000000]>'
        self.assertEqual(r00, repr(Student()))
        self.assertEqual(r01, repr(Student(name='叶嫣然', gender=True)))
        self.assertEqual(r02, repr(Student(subject=2)))
        self.assertEqual(r03, repr(Student(birthday=date(1999, 3, 15))))
        self.assertEqual(r04, repr(Student(grade=1)))
        self.assertEqual(r05, repr(Student(graduated=True)))
        self.assertEqual(r06, repr(Student(leader=True)))

        r10 = '<Student(1) 男 工学 大四 姓名="叶秋然" 年龄=23 入学年份=2018 报道时间=[2018-08-29 16:29:00,000000]>'
        r11 = '<Student(10086020) 男 工学 大四 姓名="叶秋然" 年龄=23 入学年份=2018 报道时间=[2018-08-29 16:29:00,000000]>'
        r12 = '<Student(10086020) 男 工学 大四 姓名="叶秋然" 年龄=23 入学年份=2018 报道时间=[2018-08-29 16:29:00,000000]>'
        self.assertEqual(r10, repr(Student(id=1)))
        self.assertEqual(r11, repr(Student(pk='10086020')))
        self.assertEqual(r12, repr(Student(id=1, pk='10086020')))
