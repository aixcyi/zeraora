from __future__ import annotations

import unittest


class BaseTestCase(unittest.TestCase):

    def assertEmpty(self, sequence: list | tuple | set | dict):
        """
        检查序列是否为空。
        """
        self.assertEqual(0, len(sequence), 'Sequence is not empty.')

    def assertMemberTypeIs(self, _type: type, sequence: list | tuple | set | dict):
        """
        检查序列成员是不是全都是（``is``）指定的类型。
        """
        self.assertTrue(
            all(type(member) is _type for member in sequence),
            'Sequence members are not all object of "{_type.__name__}".'
        )

    def assertAttribute(self, name: str, obj: object):
        """
        检查对象是否存在特定的属性。
        """
        self.assertTrue(hasattr(obj, name), f"Attribute '{name}' is not defined")
