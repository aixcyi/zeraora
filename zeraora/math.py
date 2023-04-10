"""
数学数字处理。
"""

from decimal import Decimal


def remove_exponent(d: Decimal):
    """
    去除十进制小数（Decimal）的尾导零。

    非原创代码，出自：
    https://docs.python.org/zh-cn/3/library/decimal.html#decimal-faq
    """
    return d.quantize(Decimal(1)) if d == d.to_integral() else d.normalize()
