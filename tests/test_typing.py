from datetime import date, datetime, timedelta
from decimal import Decimal
from uuid import UUID

from tests.base_test_case import BaseTestCase
from zeraora import casting, represent, OnionObject, ReprMixin, datasize

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


class Student(ReprMixin):

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
        self.__dict__.update(kwargs)

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


class TypingModuleTest(BaseTestCase):

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

    def test_casting(self):
        self.assertEqual(1234, casting(int, '1234'))
        self.assertEqual(None, casting(int, '12a4'))
        self.assertEqual(None, casting(int, None))
        self.assertEqual(1234, casting(int, '1234', default=5678))
        self.assertEqual(5678, casting(int, '12a4', default=5678))
        self.assertEqual('中文', casting(b'\xd6\xd0\xce\xc4'.decode, 'GBK', default='meow'))
        self.assertEqual('meow', casting(b'\xd6\xd0\xce\xc4'.decode, 'UTF8', default='meow'))
        self.assertEqual(3, casting([3, 14].__getitem__, 0, default=-1))
        self.assertEqual(-1, casting([3, 14].__getitem__, 315, IndexError, default=-1))

    def test_represent(self):
        self.assertEqual('"string"', represent('string'))
        self.assertEqual('[2012-01-23]', represent(date(2012, 1, 23)))
        self.assertEqual('[2012-01-23 08:29:59,000000]', represent(datetime(2012, 1, 23, 8, 29, 59)))
        self.assertEqual('[3d+3599.000000s]', represent(timedelta(days=3, hours=1, seconds=-1)))
        self.assertEqual('[0d+3.141590s]', represent(timedelta(seconds=3, milliseconds=140, microseconds=1590)))
        self.assertEqual('d6d0b9fac9fabbeed4daedc1d0a1d2ed', represent(UUID('d6d0b9fa-c9fa-bbee-d4da-edc1d0a1d2ed')))
        self.assertEqual('(2, 3, 5, 7)', represent((2, 3, 5, 7)))
        self.assertEqual('[2, 3, 5, 7]', represent([2, 3, 5, 7]))
        self.assertEqual('{2, 3, 5, 7}', represent({2, 3, 5, 7}))
        self.assertEqual("{200: 'ok', 404: 'no found'}", represent({200: 'ok', 404: 'no found'}))

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

    def test_datasize(self):
        self.assertEqual(1, datasize('1B'))
        self.assertEqual(1.0, datasize('8b'))
        self.assertEqual(17 * 1000, datasize('17KB'))
        self.assertEqual(17 * 1024, datasize('17KiB'))
        self.assertEqual(17 * 1000 / 8, datasize('17Kb'))
        self.assertEqual(17 * 1024 / 8, datasize('17Kib'))
        self.assertEqual(29 * 1000 * 1000, datasize('29MB'))
        self.assertEqual(29 * 1024 * 1024, datasize('29MiB'))
        self.assertEqual(29 * 1000 * 1000 / 8, datasize('29Mb'))
        self.assertEqual(29 * 1024 * 1024 / 8, datasize('29Mib'))
        self.assertEqual(31 * 1000 * 1000 * 1000, datasize('31 GB'))
        self.assertEqual(31 * 1024 * 1024 * 1024, datasize('31 GiB'))
        self.assertEqual(31 * 1000 * 1000 * 1000 / 8, datasize('31 Gb'))
        self.assertEqual(31 * 1024 * 1024 * 1024 / 8, datasize('31 Gib'))
        self.assertEqual(0, datasize('47'))
        self.assertEqual(0, datasize('47KiBytes'))
