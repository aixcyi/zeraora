"""
用于将一种值转换为另一种值的转换器。
"""
import re
from datetime import timedelta, datetime, date
from decimal import Decimal
from typing import Callable, Any, Tuple, Union
from uuid import UUID

from .typeclasses import Throwable, UNSET


def remove_exponent(d: Decimal):
    """
    去除十进制小数（Decimal）的尾导零。

    非原创代码，出自：
    https://docs.python.org/zh-cn/3/library/decimal.html#decimal-faq
    """
    return d.quantize(Decimal(1)) if d == d.to_integral() else d.normalize()


def delta2hms(delta: timedelta) -> Tuple[int, int, float]:
    """
    将时间增量转换为时分秒格式，其中秒钟以小数形式包含毫秒和微秒。

    :param delta: 时间增量。
    :return: 一个三元元组。
    """
    h = delta.seconds // 3600
    m = delta.seconds % 3600 // 60
    s = delta.seconds % 60 + delta.microseconds / 1000000
    return h, m, s


def delta2ms(delta: timedelta) -> Tuple[int, float]:
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


def represent(value) -> str:
    """
    将任意值转换为一个易于阅读的字符串。

    也是 ReprMixin 的默认格式化函数。

    默认使用 repr() 函数进行转换。如果自定义的类需要实现被此函数转换，请重写 .__repr__() 方法。

    :param value: 任意值。
    :return: 字符串。
    """
    if isinstance(value, str):
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


def datasize(literal: str) -> Union[int, float]:
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
        raise TypeError(
            '不支持解析一个非字符串类型的值。'  # pragma: no cover
        )

    pattern = re.compile(r'^([0-9]+)\s*([KMGTPEZY]?)(i?[Bb])$')
    result = re.fullmatch(pattern, literal)

    if result is None:
        return 0

    base = int(result.group(1))
    shift = 'BKMGTPEZY'.index(result.group(2))
    power = (1024 if 'i' in result.group(3) else 1000) ** shift
    power = (power / 8) if 'b' in result.group(3) else power

    return base * power


def true(value) -> bool:
    """
    将HTTP请求中 query 部分的参数值转换为 Python 的逻辑值。

    :param value: query 中的参数值。
    :return: True 或 False。
    """
    return value in ('true', 'True', 'TRUE', 1, True)


def safecast(mapper: Callable, raw, *errs: Throwable, default=None) -> Any:
    """
    转换一个值，转换失败时返回default，确保不会发生指定异常。

    默认捕获以下异常，可以通过errs参数追加更多异常：
        - TypeError
        - ValueError
        - KeyboardInterrupt

    :param mapper: 用来转换raw的转换器。如果转换器不可调用，将直接返回默认值。
    :param raw: 被转换的值。
    :param errs: 需要捕获的其它异常类或异常对象。应当提供可被 except 语句接受的值。
    :param default: 默认值。即使不提供也会默认返回 None 而不会抛出异常。
    :return: 转换后的值。如若捕获到特定异常将返回默认值。
    """
    exceptions = tuple(
        exc for exc in errs
        if exc.__class__ is type
        and issubclass(exc, BaseException)
        or isinstance(exc, BaseException)
    )
    if not callable(mapper):
        return default  # pragma: no cover
    try:
        return mapper(raw)
    except (TypeError, ValueError, KeyboardInterrupt) + exceptions:
        return default


class SafeCaster:

    def __init__(self, raw: Any = UNSET):
        """
        创建一个安全转换器，用于转换某个值而不发生特定异常。若不提供初值，则第一个转换器也必须允许无参调用。
        """
        self._value = raw
        self._default = None
        self._converters = tuple()
        self._exceptions = tuple()

    def __call__(self, raw: Any = UNSET) -> 'SafeCaster':
        self._value = raw
        return self

    def catch(self, *exceptions: Throwable) -> 'SafeCaster':
        """
        置入需要捕获的异常。应当提供可被 except 语句接受的值。
        """
        self._exceptions = tuple(
            exc for exc in exceptions
            if exc.__class__ is type
            and issubclass(exc, BaseException)
            or isinstance(exc, BaseException)
        )
        return self

    def by(self, *mappers: Callable) -> 'SafeCaster':
        """
        置入转换器。若未提供初值，则第一个转换器也必须允许无参调用。
        """
        self._converters = tuple(
            mapper for mapper in mappers
            if callable(mapper)
        )
        return self

    def get(self, default=None) -> Any:
        """
        执行转换并返回转换结果。若触发置入的异常或没有置入转换器则返回默认值；若触发未被置入的异常将原样抛出。
        """
        if len(self._converters) <= 0:
            return default

        if self._value is UNSET:
            result = self._converters[0]()
            converters = self._converters[1:]
        else:
            result = self._value
            converters = self._converters

        try:
            for converter in converters:
                result = converter(result) if callable(converter) else result
            return result
        except self._exceptions:
            return default


safecasts = SafeCaster().catch(TypeError, ValueError, KeyboardInterrupt)
