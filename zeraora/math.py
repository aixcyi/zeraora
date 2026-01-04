__all__ = [
    'bitstream',
    'digitstream',
    'remove_exponent',
    'decimalize',
]

from decimal import Context, Decimal, ROUND_FLOOR
from typing import Iterator


def bitstream(integer: int) -> Iterator[int]:
    """
    获取一个整数的所有比特位。

    >>> list(bitstream(67))
    [1, 2, 64]

    >>> list(bitstream(-43))
    [-1, -2, -8, -32]

    >>> list(bitstream(0))
    []
    """
    if not isinstance(absolute := abs(integer), int):
        return
    if integer >= 0:
        for power in range(0, absolute.bit_length()):
            if absolute & (bit := 1 << power):
                yield bit
    else:
        for power in range(0, absolute.bit_length()):
            if absolute & (bit := 1 << power):
                yield -bit


def digitstream(integer: int, base: int) -> Iterator[int]:
    """
    获取一个非负整数在 *base* 进制下的各位数码，**以逆序生成** 。

    生成器无法直接反转顺序，建议调用者处理好生成结果后再取出对象、进行反转。

    >>> digits = digitstream(1008612, 16)
    >>> mapper = '0123456789abcdef'.__getitem__
    >>> ''.join(map(mapper, digits))[::-1]
    'f63e4'
    >>> hex(1008612)
    '0xf63e4'

    :param integer: 十进制整数。参数会被取绝对值，需要提前保留整数的符号。
    :param base: 需要转换为什么进位制。参数不能小于 ``2`` 。
    :return: 一个迭代器，每次迭代会 “从右到左” 输出结果的一位的十进制表示。
    """
    if base < 2:
        return
    integer = abs(integer)
    while integer >= base:
        yield integer % base
        integer //= base
    yield integer


def remove_exponent(d: Decimal) -> Decimal:
    """
    去除十进制小数的尾导零。

    摘录自 `Decimal 常见问题 <https://docs.python.org/zh-cn/3/library/decimal.html#decimal-faq>`_ 。
    """
    return d.quantize(Decimal('1')) if d == d.to_integral() else d.normalize()


def decimalize(value: str | int | float | Decimal, max_digits=12, decimal_places=2) -> Decimal:
    """
    将小数（不含小数点）长度控制在 `max_digits` 位，小数位数控制在 `decimal_places` 位，多余的小数部分将被直接丢弃，不会执行舍入。

    :param value: 字符串、整数、小数或 :class:`Decimal` 对象。
    :param max_digits: 数字中允许的最大位数。请注意，这个数字必须大于或等于 `decimal_places`。
    :param decimal_places: 与数字一起存储的小数位数。
    :return: 一个 :class:`Decimal` 对象。
    """
    if not isinstance(value, Decimal):
        value = Decimal(value)
    return value.quantize(Decimal(f'1e{-decimal_places}'), context=Context(prec=max_digits, rounding=ROUND_FLOOR))
