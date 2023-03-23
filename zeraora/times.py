__all__ = [
    'delta2hms',
    'delta2ms',
]

from datetime import timedelta


def delta2hms(delta: timedelta) -> tuple:
    """
    将时间增量转换为时分秒格式。

    :param delta: 时间增量。
    :return: 包含三个整数的元组，分别对应小时数、分钟数、秒钟数。
    """
    h = delta.seconds // 3600
    m = delta.seconds % 3600 // 60
    s = delta.seconds % 60 + delta.microseconds / 1000000
    return h, m, s


def delta2ms(delta: timedelta) -> tuple:
    """
    将时间增量转换为分秒格式。

    :param delta: 时间增量。
    :return: 包含两个整数的元组，分别对应分钟数和秒钟数。
    """
    m = delta.seconds // 60
    s = delta.seconds % 60 + delta.microseconds / 1000000
    return m, s
