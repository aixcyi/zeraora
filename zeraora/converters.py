"""
用于将一种值转换为另一种值的转换器。
"""
from __future__ import annotations

__all__ = [
    'dict_',
    'remove_exponent',
    'get_digits',
    'delta2hms',
    'delta2ms',
    'delta2s',
    'wdate',
    'get_week_range',
    'get_week_side',
    'get_week_in_year',
    'represent',
    'datasize',
    'dsz',
    'true',
]

import re
from datetime import date, datetime, timedelta
from decimal import Decimal
from typing import Any, Iterator
from uuid import UUID


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


def remove_exponent(d: Decimal):
    """
    去除十进制小数（Decimal）的尾导零。

    非原创代码，出自：
    https://docs.python.org/zh-cn/3/library/decimal.html#decimal-faq
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


def delta2hms(delta: timedelta) -> tuple[int, int, float]:
    """
    将时间增量转换为时分秒格式，其中秒钟以小数形式包含毫秒和微秒。

    :param delta: 时间增量。
    :return: 一个三元元组。
    """
    h = delta.seconds // 3600
    m = delta.seconds % 3600 // 60
    s = delta.seconds % 60 + delta.microseconds / 1000000
    return h, m, s


def delta2ms(delta: timedelta) -> tuple[int, float]:
    """
    将时间增量转换为分秒格式，其中秒钟以小数形式包含毫秒和微秒。

    :param delta: 时间增量。
    :return: 二元元组。前者用一个整数表示分钟数，
             后者用一个小数表示秒钟数和纳秒数。
    """
    m = delta.seconds // 60
    s = delta.seconds % 60 + delta.microseconds / 1000000
    return m, s


def delta2s(delta: timedelta) -> float:
    """
    将时间增量转换为秒钟数，以小数形式包含毫秒和微秒。

    :param delta: 时间增量。
    :return: 一个小数。
    """
    return delta.seconds + delta.microseconds / 1000000


# 仿构造器命名
def wdate(year: int, week_in_year: int, day_in_week: int, sunday_first=False) -> date:
    """
    将某一年的某一周的星期几转换为一个具体的日期。

    :param year: 具体年份。比如 2012、2023 等。
    :param week_in_year: 一年中的第几周。从 0 开始。
    :param day_in_week: 星期几。0 表示周日、1 表示周一，以此类推。
    :param sunday_first: 是否以周日为一周的开始。
    :return: 一个日期。
    """
    day = f'{year:04d}-{week_in_year:02d}-{day_in_week:1d}'
    fmt = '%Y-%U-%w' if sunday_first else '%Y-%W-%w'
    return datetime.strptime(day, fmt).date()


def get_week_range(year: int,
                   week_in_year: int,
                   month: int = None,
                   sunday_first=False) -> tuple[date, ...]:
    """
    计算一年中某一周对应的所有日期。

    :param year: 具体年份。比如 2012、2023 等。
    :param week_in_year: 一年中的第几周。从 0 开始。
    :param month: 具体月份。若指定了这个参数，则只计算这个月的那一部分日期。
    :param sunday_first: 是否以周日为一周的开始。
    :return: 若指定了不恰当的月份，有可能返回空列表。
    :raise ValueError: year 年的 week_in_year 周不在当年的 month 月里。
    """
    fmt = '%Y-%U-%w' if sunday_first else '%Y-%W-%w'
    start = f'{year:04d}-{week_in_year:02d}-{0 if sunday_first else 1}'
    start = datetime.strptime(start, fmt).date()
    days = tuple(start + timedelta(days=i) for i in range(7))
    days = days if month is None else tuple(day for day in days if day.month == month)
    if not days:
        raise ValueError(
            f'{year} 年的 {week_in_year} 周不在当年的 {month} 月里。'
        )
    return days


def get_week_side(year: int,
                  week_in_year: int,
                  month: int = None,
                  sunday_first=False) -> tuple[date, date]:
    """
    计算一年中某一周对应的第一天和最后一天。

    :param year: 具体年份。比如 2012、2023 等。
    :param week_in_year: 一年中的第几周。从 0 开始。
    :param month: 具体月份。若指定了这个参数，则只计算这个月的那一部分日期。
    :param sunday_first: 是否以周日为一周的开始。
    :return: 两个日期，表示（这个月的）这一周的第一天和最后一天。
    :raise ValueError: year 年的 week_in_year 周不在当年的 month 月里。
    """
    days = get_week_range(year, week_in_year, month, sunday_first)
    return days[0], days[-1]


def get_week_in_year(*args, sunday_first=False) -> int:
    """
    计算一个具体日期自一年开始的周序号。

    如果 ``sunday_first=False`` ，那么一年中第一个星期一之前的日子都算作第 0 周。
    如果 ``sunday_first=True`` ，那么一年中第一个星期日之前的日子都算作第 0 周。

    - ``get_week_in_year(date)`` ，提供一个日期。
    - ``get_week_in_year(datetime)`` ，提供一个时刻。
    - ``get_week_in_year(int, int, int)`` ，分别提供年月日。

    :param args: 参数。
    :param sunday_first: 是否以周日作为一周的开始。
    :return: 一个从 0 开始递增的整数。
    """
    if len(args) == 1 and isinstance(args[0], date):
        day = args[0]
    elif len(args) >= 3 and all(isinstance(a, int) for a in args):
        day = date(*args[:3])
    else:
        raise ValueError
    week = day.strftime('%U') if sunday_first else day.strftime('%W')
    return int(week)


def represent(value: Any) -> str:
    """
    将任意值转换为一个易于阅读的字符串。

    也是 ReprMixin 的默认格式化函数。

    默认使用 repr() 函数进行转换。如果自定义的类需要实现被此函数转换，请重写 .__repr__() 方法。

    :param value: 任意值。
    :return: 字符串。
    """
    if hasattr(value, 'label'):  # 兼容像 Django 的 Choices 那样的枚举
        return value.label
    elif isinstance(value, str):
        return f'"{value}"'
    elif isinstance(value, timedelta):
        return f'[{value.days}d+{value.seconds}.{value.microseconds:06d}s]'
    elif isinstance(value, datetime):
        return f'[{value:%Y-%m-%d %H:%M:%S,%f}]'
    elif isinstance(value, date):
        return f'[{value:%Y-%m-%d}]'
    elif isinstance(value, UUID):
        return value.hex
    else:
        return repr(value)


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


def true(value) -> bool:
    """
    将HTTP请求中 query 部分的参数值转换为 Python 的逻辑值。

    :param value: query 中的参数值。
    :return: True 或 False。
    """
    return value in ('true', 'True', 'TRUE', 1, True, '1')
