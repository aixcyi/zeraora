"""
数学相关。
"""
__all__ = [
    'remove_exponent',
    'get_digits',
]

from decimal import Decimal
from typing import Iterator


def remove_exponent(d: Decimal) -> Decimal:
    """
    去除十进制小数（Decimal）的尾导零。

    摘录自 `Decimal 常见问题 <https://docs.python.org/zh-cn/3/library/decimal.html#decimal-faq>`_ 。
    """
    return d.quantize(Decimal(1)) if d == d.to_integral() else d.normalize()


def get_digits(number: int, base: int) -> Iterator[int]:
    """
    将整数转换为其它进位制。

    返回一个迭代器，对其迭代将得到目标进制整数从右到左的每一位的十进制表示：

    >>> digits = get_digits(1008611, 16)
    >>> mapper = lambda d: '0123456789abcdef'[d]
    >>> ''.join(map(mapper, digits))
    '3e36f'

    >>> hex(1008611)
    '0xf63e3'

    :param number: 十进制整数。
    :param base: 需要转换为什么进位制。参数不能小于 2 。
    :return: 一个迭代器，每次迭代会 “从右到左” 输出结果的一位的十进制表示。
    :raise AssertionError: 参数不符合要求。
    """
    assert isinstance(number, int), '只能转换整数的进位制。'
    assert isinstance(base, int), '无法处理非整数进位制。'
    assert 2 <= base, '无法处理低于二进制的进位制。'
    while number >= base:
        yield number % base
        number //= base
    yield number
