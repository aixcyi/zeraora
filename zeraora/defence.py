"""
与防御式编程有关的工具。
"""
from __future__ import annotations

__all__ = [
    'datasize',
    'dsz',
    'dict_',
]

import re
from typing import Any


def datasize(literal: str) -> int | float:
    """
    将一个字面量转换为字节数目。

    支持的单位包括：
      - B、b
      - KB、KiB、Kb、Kib
      - MB、MiB、Mb、Mib
      - GB、GiB、Gb、Gib
      - TB、TiB、Tb、Tib
      - 以此类推……

    - 1 B == 8 b
    - 1 MB == 1000 KB
    - 1 MiB == 1024 KiB

    :param literal: 一个整数后缀数据大小的单位。
    :return:
    """
    if not isinstance(literal, str):
        raise TypeError('不支持解析一个非字符串类型的值。')

    pattern = re.compile(r'^([0-9]+)\s*([KMGTPEZY]?)(i?[Bb])$')
    result = re.fullmatch(pattern, literal)

    if result is None:
        return 0

    base = int(result.group(1))
    shift = 'BKMGTPEZY'.index(result.group(2))
    power = (1024 if 'i' in result.group(3) else 1000) ** shift
    power = (power / 8) if 'b' in result.group(3) else power

    return base * power


dsz = datasize


def dict_(**kwargs: Any) -> dict:
    """
    去除dict参数名尾随的 "_" 。

    比如

    >>> dict_(
    >>>     level='DEBUG',
    >>>     class_='logging.StreamHandler',
    >>>     filters=[],
    >>>     formatter='bear',
    >>> )

    将会返回

    >>> {
    >>>     "level": "DEBUG",
    >>>     "class": "logging.StreamHandler",
    >>>     "filters": [],
    >>>     "formatter": "bear",
    >>> }

    :param kwargs: 仅限关键字传参。
    :return: 一个字典。
    """
    return dict(
        (k.rstrip('_'), v) for k, v in kwargs.items()
    )
