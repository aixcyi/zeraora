"""
数据结构包。
"""
from __future__ import annotations

__all__ = [
    'DivisionCode',
    'Division',
]

from typing import NamedTuple, Tuple

from zeraora.constants import DivisionLevel


class DivisionCode(NamedTuple):
    """
    统计用行政区划代码。
    """
    province: str
    prefecture: str = '00'
    county: str = '00'
    township: str = '000'
    village: str = '000'

    def __str__(self):
        return ''.join(self)

    @classmethod
    def fromcode(cls, code: str) -> DivisionCode:
        """
        从一个代码字符串生成 ``DivisionCode`` 。

        会对 ``code`` 参数用 "0" 补齐到 12 位字符串，比如

        >>> dc = DivisionCode.fromcode('520502000000')

        与

        >>> dc = DivisionCode.fromcode('520502')

        是等价的。

        ----

        :param code: 字符串形式的行政区划代码。
        :return: 一个具名元组。
        """
        adc = code.ljust(12, '0')
        return cls(adc[:2], adc[2:4], adc[4:6], adc[6:9], adc[9:12])

    @property
    def level(self) -> int:
        """
        区划代码所在的层级。

        使用整数 1 到 5 分别代表省、市、县、乡、村五个层级。

        该层级仅根据代码分析。比如，
        ``(52,05,02,000,000)`` 的层级在县，因为乡和村的代码为全 0 字符串。
        """
        # (xx,xx,xx,xxx,xxx) -> level 5
        # (xx,xx,xx,xxx,000) -> level 4
        # (xx,xx,xx,000,000) -> level 3
        # (xx,xx,00,000,000) -> level 2
        # (xx,00,00,000,000) -> level 1
        if self.village != '000':
            return 5
        if self.township != '000':
            return 4
        if self.county != '00':
            return 3
        if self.prefecture != '00':
            return 2
        return 1

    def tocode(self, level: int = None) -> DivisionCode:
        """
        提取某个层级的代码。

        >>> dc3 = DivisionCode('52','05','02')
        >>> dc5 = DivisionCode('52','05','02','111','006')
        >>>
        >>> assert dc5.tocode(3) == str(dc3)

        :param level: 使用整数 1 到 5 分别代表省、市、县、乡、村五个层级。
        :return: 该层级的 12 位代码字符串。
        """
        lv = self.level if level is None else level
        defaults = ('00',) + tuple(self._field_defaults.values())
        assert 0 < lv <= 5
        return type(self)(*(self[:lv] + defaults[lv:]))

    def tostr(self, level: int = None) -> str:
        """
        提取某个层级的代码。

        >>> dc3 = DivisionCode('44','01','06')
        >>> dc5 = DivisionCode('44','01','06','006','007')
        >>>
        >>> assert dc5.tostr(3) == str(dc3)

        :param level: 使用整数 1 到 5 分别代表省、市、县、乡、村五个层级。
        :return: 该层级的 12 位代码字符串。
        """
        lv = self.level if level is None else level
        assert 0 < lv <= 5
        return ''.join(self[:lv]).ljust(12, '0')

    def partition(self, level: int = None) -> tuple[str, str, str]:
        """
        按照层级切割为三个部分。

        >>> dc = DivisionCode('52', '05', '02', '111', '006')
        >>>
        >>> dc.partition(1)  # -> ('', '52', '0502111006')
        >>> dc.partition(2)  # -> ('52', '05', '02111006')
        >>> dc.partition(3)  # -> ('5205', '02', '111006')
        >>> dc.partition(4)  # -> ('520502', '111', '006')
        >>> dc.partition(5)  # -> ('520502111', '006', '')

        :param level: 使用整数 1 到 5 分别代表省、市、县、乡、村五个层级。
        :return: 左、中、右三个部分。
        """
        lv = self.level if level is None else level
        assert 0 < level <= 5
        return ''.join(self[:lv - 1]), self[lv - 1], ''.join(self[lv:])


class Division(NamedTuple):
    """
    行政区划。
    """
    name: str
    code: DivisionCode
    level: DivisionLevel
    years: Tuple[int] = ()

    def __repr__(self):
        return '<Division%i %s %s years=[%s]>' % (
            self.level.value,
            self.code, self.name,
            ','.join(map(str, self.years)),
        )
