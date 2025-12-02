from typing import NamedTuple

from tests.base_test_case import BaseTestCase
from zeraora.enum import MoreChoices, NamedEnum


class EnumTest(BaseTestCase):

    def testNamedEnum(self):
        class SaleChannel(NamedTuple):
            value: int
            code: str
            label: str

        class SaleChannels(SaleChannel, NamedEnum):
            CASHIER = 1, 'Y', '收银机'
            APPLET = 2, 'X', '小程序'
            KIOSK = 4, 'H', '售货机'
            APP = 8, 'A', '移动端应用'
            HANDHELD = 16, 'J', '手持机'

        self.assertEqual('APP', SaleChannels.APP.name)
        self.assertEqual(8, SaleChannels.APP.value)
        self.assertEqual('A', SaleChannels.APP.code)
        self.assertEqual('移动端应用', SaleChannels.APP.label)
        self.assertEqual('8', str(SaleChannels.APP))
        self.assertEqual('SaleChannels.APP', repr(SaleChannels.APP))
        self.assertIs(SaleChannels.APP, SaleChannels(8))
        self.assertListEqual(['CASHIER', 'APPLET', 'KIOSK', 'APP', 'HANDHELD'], SaleChannels.names)
        self.assertListEqual([1, 2, 4, 8, 16], SaleChannels.values)
        self.assertListEqual(['Y', 'X', 'H', 'A', 'J'], SaleChannels.codes)
        self.assertListEqual(['收银机', '小程序', '售货机', '移动端应用', '手持机'], SaleChannels.labels)
        self.assertListEqual(
            [
                (1, '收银机'),
                (2, '小程序'),
                (4, '售货机'),
                (8, '移动端应用'),
                (16, '手持机'),
            ],
            SaleChannels.choices
        )

    def testMoreChoicesMeta(self):
        class UrgencyLevel2(MoreChoices):
            HIGH = 10, 'WARNING'
            NORMAL = 0, 'INFO'
            LOW = -10, 'DEBUG'
            __properties__ = 'loglevel'

        with self.assertRaises(ValueError):
            class UrgencyLevel3(MoreChoices):
                HIGH = 10, 'WARNING'
                NORMAL = 0, 'INFO'
                LOW = -10, 'DEBUG'
                __properties__ = '_loglevel',

        with self.assertRaises(AttributeError):
            class UrgencyLevel4(MoreChoices):
                HIGH = 10, 'WARNING'
                NORMAL = 0, 'INFO'
                LOW = -10, 'DEBUG'
                __properties__ = 'value', 'loglevel'

        with self.assertRaises(KeyError):
            class UrgencyLevel5(MoreChoices):
                HIGH = 10, 'WARNING'
                NORMAL = 0, 'INFO'
                LOW = -10, 'DEBUG'
                __properties__ = 'generate_next_value',
