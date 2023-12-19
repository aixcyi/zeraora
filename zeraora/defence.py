"""
与防御式编程有关的工具。
"""
from __future__ import annotations

__all__ = [
    'true',
    'datasize',
    'dsz',
    'dict_',
    'start',
    'deprecate',
]

import re
import sys
import warnings
from functools import wraps
from typing import Any


def true(value) -> bool:
    """
    将HTTP请求中 query 部分的参数值转换为 Python 的逻辑值。

    :param value: query 中的参数值。
    :return: True 或 False。
    """
    return value in ('true', 'True', 'TRUE', 1, True, '1')


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


def start(*version, note: str = None):
    """
    检查 Python 版本是否高于或等于指定值，
    如果低于指定的版本就会抛出 RuntimeError。

    若提供了 ``note`` 参数，则会在末尾输出。
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if sys.version_info < version:
                v = '.'.join(map(str, version))
                raise RuntimeError(
                    # 英文在前保证控制台出现乱码时不会掩盖该错误信息
                    f'Require Python version {v} or above to run. '
                    f'Python运行版本需要在 {v} 或以上。'
                    + ('' if note is None else note)
                )
            return func(*args, **kwargs)

        return wrapper

    return decorator


def deprecate(*since,
              ref=sys.version_info,
              reason: str = 'This function is deprecated since %(since)s .',
              suggestion: str = 'This function will be deprecate at %(since)s .',
              migration: str = None,
              ):
    """
    为一个函数作废弃标记。

    :param since: 自哪个版本开始废弃。
    :param ref: 参照版本。用于确定状态是准备废弃还是已经废弃。
    :param reason: 已废弃的原因。（废弃后的提示）
    :param suggestion: 准备废弃时提供的建议。（废弃前的提示）
    :param migration: 假设废弃之后应该采取的迁移措施或用法变更说明。
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            tips = (suggestion if ref < since else reason) % dict(since='.'.join(map(str, since)))
            tips += ('\n' + migration) if migration else ''
            if ref < since:
                warnings.warn(tips, category=PendingDeprecationWarning, stacklevel=2)
            else:
                warnings.warn(tips, category=DeprecationWarning, stacklevel=2)
            return func(*args, **kwargs)

        return wrapper

    return decorator
