"""
数据结构包。
"""
from __future__ import annotations

__all__ = [
    'DivisionCode',
    'Division',
]

from typing import NamedTuple, Tuple

from .constants import DivisionLevel


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
        adc = code.ljust(12, '0')
        return cls(adc[:2], adc[2:4], adc[4:6], adc[6:9], adc[9:12])


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
