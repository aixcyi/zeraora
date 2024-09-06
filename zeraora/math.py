"""
数学相关工具和常量。
"""
from __future__ import annotations

__all__ = [
    'ZERO',
    'ONE',
    'remove_exponent',
    'absolute',
    'bitstream',
    'digitstream',
]

from decimal import Decimal
from typing import Generator

ZERO = Decimal(0)
"""``Decimal`` 类型的整数 ``0`` 。"""

ONE = Decimal(1)
"""``Decimal`` 类型的整数 ``1`` 。"""


def remove_exponent(d: Decimal) -> Decimal:
    """
    去除十进制小数（Decimal）的尾导零。

    摘录自 `Decimal 常见问题 <https://docs.python.org/zh-cn/3/library/decimal.html#decimal-faq>`_ 。
    """
    return d.quantize(Decimal(1)) if d == d.to_integral() else d.normalize()


def absolute(n: int | float | Decimal) -> tuple[bool, int | float | Decimal]:
    """
    返回一个实数的符号及其绝对值。``True`` 表示正数，``False`` 表示负数。
    """
    return n >= 0, abs(n)


def bitstream(integer: int) -> Generator[int, None, None]:
    """
    获取一个整数的所有比特位。

    >>> list(bitstream(67))
    [1, 2, 64]

    >>> list(bitstream(-43))
    [-1, -2, -8, -32]

    >>> list(bitstream(0))
    []
    """
    sign, positive = absolute(integer)
    if not isinstance(positive, int):
        yield from []
        return
    for power in range(0, positive.bit_length()):
        bit = 1 << power
        if positive & bit:
            yield bit if sign else -bit


def digitstream(integer: int, base: int) -> Generator[int, None, None]:
    """
    获取一个非负整数在 base 进制下的各位数码，**以逆序生成** 。

    生成器无法直接反转顺序，建议调用者处理好生成结果后再取出对象、进行反转。

    >>> digits = digitstream(1008612, 16)
    >>> mapper = '0123456789abcdef'.__getitem__
    >>> ''.join(map(mapper, digits))[::-1]
    'f63e4'

    >>> hex(1008612)
    '0xf63e4'

    :param integer: 十进制整数。参数会被取绝对值，需要提前保留整数的符号。
    :param base: 需要转换为什么进位制。参数不能小于 2 。
    :return: 一个迭代器，每次迭代会 “从右到左” 输出结果的一位的十进制表示。
    """
    if base < 2:
        yield from []
        return
    integer = abs(integer)
    while integer >= base:
        yield integer % base
        integer //= base
    yield integer
