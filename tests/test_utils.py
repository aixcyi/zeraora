from datetime import date, datetime
from random import random
from time import sleep

from tests.base_test_case import BaseTestCase
from zeraora.utils import ReprMixin, BearTimer

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


class UtilsTest(BaseTestCase):

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
