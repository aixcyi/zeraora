from typing import Tuple, Union
from unittest import TestCase


class BaseTestCase(TestCase):

    def assertHasAttribute(self, attr: str, obj):
        self.assertTrue(hasattr(obj, attr))

    def assertNoAttribute(self, attr: str, obj):
        self.assertFalse(hasattr(obj, attr))

    def assertLengthEqual(self, length: int, exp):
        self.assertEqual(length, len(exp))

    def assertMemberTypeIs(self, _type: type, exp):
        self.assertTrue(all(type(member) is _type for member in exp))

    def assertMemberIsInstance(self, _type: Union[type, Tuple[type]], exp):
        self.assertTrue(all(isinstance(member, _type) for member in exp))
