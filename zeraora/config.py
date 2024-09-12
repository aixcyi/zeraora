"""
方便开发者配置设置的工具。
"""
from __future__ import annotations

__all__ = [
    'dict_',
    'datasize',
    'during',
]

import re
from itertools import chain
from typing import Any


def dict_(*pairs: tuple[str, Any], **kwargs: Any) -> dict:
    """
    :class:`dict` 的变种。

    - 会去除“键”尾随的所有 ``_`` 。
    - 接收任意个二元元组（元组形式的键-值对）。
    - 注意，此函数不能完全兼容 :class:`dict` 方法。

    >>> dict_(
    >>>     ('.', {'foo': 'baz'}),
    >>>     ('level', 'DEBUG'),
    >>>     class_='logging.StreamHandler',
    >>>     filters=[],
    >>>     formatter='bear',
    >>> )
    {
        '.': {
            'foo': 'baz'
        },
        'level': 'DEBUG',
        'class': 'logging.StreamHandler',
        'filters': [],
        'formatter': 'bear',
    }
    """
    return dict(chain(
        pairs,
        ((k.rstrip('_'), v) for k, v in kwargs.items()),
    ))


class datasize:
    PATTERN = re.compile(r'^([0-9]+)\s*([KMGTPEZY]?)(i?[Bb])$')
    SEPERATOR = ','

    def __new__(cls, literal: str) -> int | float:
        """
        数据大小字面值 → 字节数目。

        - 字面值由一个或多个部分组成，使用英文逗号 ``,`` 分隔，每个部分是整数+单位，字节数目由所有部分累加求和得到。
          只要不涉及比特 ``b`` ，那么返回结果必定为 :class:`int` 类型，否则必定为 :class:`float` 类型。
        - 整数部分不支持小数点、仅支持十进制、不支持负号。
        - 单位部分严格区分大小写。
        - 任一部分解析失败都会抛出 :class:`ValueError` 以避免潜在的错误。
        - 强烈建议在单位及每个部分之间预留空格，方便开发和运维人员检查！！！

        >>> datasize('10KB')
        10000
        >>> datasize('10KiB')
        10240
        >>> datasize('10 KiB, 1 B')
        10241
        >>> datasize('10 KiB, 1 MiB')
        1058816
        >>> datasize('10 KiB, 1 b')
        10240.125

        支持的单位包括：（mB 这类并非正式缩写，故不支持）

        - B、b
        - KB、KiB、Kb、Kib
        - MB、MiB、Mb、Mib
        - GB、GiB、Gb、Gib
        - TB、TiB、Tb、Tib
        - 以此类推……

        它们之间的进位转换关系如下：

        - 1 B == 8 b
        - 1 MB == 1000 KB
        - 1 MiB == 1024 KiB
        """
        if not isinstance(literal, str):
            raise TypeError(
                'cannot parse an non-string value.'
            )
        return sum(cls._parse(part) for part in literal.split(cls.SEPERATOR))

    @classmethod
    def _parse(cls, literal: str) -> int | float:
        result = re.fullmatch(cls.PATTERN, literal)
        if result is None:
            raise ValueError(
                f'cannot parse data-size literal "{literal}", '
                f'plz check and fix it on your configurations.'
            )
        base = int(result.group(1))
        shift = 'BKMGTPEZY'.index(result.group(2))
        power = (1024 if 'i' in result.group(3) else 1000) ** shift
        power = (power / 8) if 'b' in result.group(3) else power
        return base * power


class during:
    UNITS = dict(s=1, m=60, h=3600, d=86400, w=86400 * 7)
    PATTERN = re.compile(r'^([0-9]+)\s*([wdhms])$')
    SEPERATOR = ','

    def __new__(cls, literal: str) -> int:
        """
        时长字面值 → 秒数。

        - 字面值由一个或多个部分组成，使用英文逗号 ``,`` 分隔，每个部分是整数+单位，字节数目由所有部分累加求和得到。
        - 整数部分不支持小数点、仅支持十进制、不支持负号。
        - 单位部分严格区分大小写。
        - 任一部分解析失败都会抛出 :class:`ValueError` 以避免潜在的错误。
        - 强烈建议在单位及每个部分之间预留空格，方便开发和运维人员检查！！！

        >>> during('1h')
        3600
        >>> during('1d')
        86400
        >>> during('1h,1m,1s')
        3661

        支持的单位及之间的转换关系如下：

        - 1w == 7d
        - 1d == 24h == 86400s
        - 1h == 60m == 3600s
        - 1m == 60s
        """
        if not isinstance(literal, str):
            raise TypeError(
                'cannot parse an non-string value.'
            )
        return sum(cls._parse(part) for part in literal.split(cls.SEPERATOR))

    @classmethod
    def _parse(cls, literal: str) -> int | float:
        result = re.fullmatch(cls.PATTERN, literal)
        if result is None:
            raise ValueError(
                f'cannot parse duration literal "{literal}", '
                f'plz check and fix it on your configurations.'
            )
        base = int(result.group(1))
        power = cls.UNITS[result.group(2)]
        return base * power
