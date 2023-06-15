from unittest import TestCase


class BaseTestCase(TestCase):

    def assertMemberTypeIs(self, _type: type, exp):
        t0 = (_type,) * len(exp)
        t2 = tuple(type(member) for member in exp)
        self.assertTupleEqual(t0, t2)
