"""
日期时间相关工具。
"""
from __future__ import annotations

__all__ = [
    'BearTimer',
    'is_leap',
    'get_last_monthday',
    'TimeFrame',
    'Datetime',
    'Timedelta',
    'daterange',
    'weekrange',
]

import logging
import sys
from datetime import datetime, timedelta, MINYEAR, MAXYEAR, date, time, tzinfo
from enum import IntEnum
from functools import wraps
from threading import Lock
from typing import Generator, Optional

logger = logging.getLogger('zeraora.datetime')


class BearTimer:
    __slots__ = '_label', '_marks', '_point'

    CONFIG = dict(
        version=1,
        formatters={
            'bear': dict(
                format='[%(asctime)s] [%(levelname)s] %(message)s',
            ),
            'bear_plus': dict(
                format='[%(asctime)s] [%(levelname)s] '
                       '[%(module)s.%(funcName)s:%(lineno)d] '
                       '%(message)s',
            ),
        },
        filters={},
        handlers={
            'Console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'filters': [],
                'formatter': 'bear',
            },
        },
        loggers={
            'zeraora.datetime': dict(
                level='DEBUG',
                handlers=['Console'],
                propagate=False,
            ),
        },
    )

    def __init__(self, label: str = None, *_, **__):
        """
        熊牌秒表。对代码运行进行计时，并向名为 "zeraora.datetime" 的 Logger 发送 DEBUG 等级的日志。

        ----

        使用前，需要先启用日志输出： ::

            import logging.config
            from zeraora.datetime import BearTimer

            logging.config.dictConfig(BearTimer.CONFIG)
            bear = BearTimer()

        对于使用 Django 的项目可以改为在 settings.py 中进行如下设置： ::

            LOGGING = {
                'version': 1,
                'formatters': {...},
                'filters': {...},
                'handlers': {
                    'Console': {  # 确保有一个控制台输出
                        'level': 'DEBUG',
                        'class': 'logging.StreamHandler',
                    },
                    ...
                },
                'loggers': {
                    'zeraora.datetime': {  # 添加相应的日志记录器
                        'level': 'DEBUG',
                        'handlers': ['Console'],
                    },
                },
            }

        ----

        最简单是使用 ``with`` 语句包裹需要计时的部分：

        >>> with BearTimer() as bear:
        >>>     # 业务逻辑
        >>>     pass

        如需对一整个函数进行计时，可以作为装饰器使用：

        >>> @BearTimer()
        >>> def do_somthing(*args, **kwargs):
        >>>     # 业务逻辑
        >>>     pass

        带有多个装饰器时，计时器放哪里取决于你的计时范围：

        >>> from rest_framework.decorators import api_view
        >>> from zeraora.datetime import BearTimer
        >>>
        >>> @BearTimer()  # 从请求转发过来那一刻开始计时
        >>> @api_view(['GET'])
        >>> def query_status(request, *args, **kwargs):
        >>>     # 业务逻辑
        >>>     pass
        >>>
        >>> @api_view(['POST'])
        >>> @BearTimer()  # 从login()执行那一刻开始计时
        >>> def login(request, *args, **kwargs):
        >>>     # 业务逻辑
        >>>     pass

        此外还可以实例化一个对象。每个对象都是独立的计时器，互不影响。

        >>> bear = BearTimer()
        >>> bear.start()
        >>> # 业务逻辑
        >>> bear.stop()

        :param label: 计时器的标题，用以标明输出信息归属于哪个计时器。默认从打印消息时的上下文中获取。
        """
        try:
            # noinspection PyUnresolvedReferences,PyProtectedMember
            context = sys._getframe().f_back.f_code.co_name
        except AttributeError:
            context = ''
        self._label = context if not label and hasattr(sys, '_getframe') else str(label)
        self._marks: list[tuple[datetime, timedelta]] = []
        self._point: int = 0

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            self._label = func.__name__
            self.start()
            returns = func(*args, **kwargs)
            self.stop()
            return returns

        return wrapper

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, traceback):
        self.stop()

    @property
    def records(self) -> list[tuple[datetime, timedelta]]:
        """
        每一次记录的时刻，以及距上一次记录的时间差。
        """
        return self._marks[:]

    def _log(self, total: float, delta: float, msg=''):
        logger.debug(f'[{self._label}] [{total:.9f} +{delta:.9f}]: {msg}')

    def start(self, msg='Starting...'):
        """
        清除之前的所有标记，并重新开始计时。

        :param msg: 要输出的消息。
        :return: 当前秒表。
        """
        self._marks = [(datetime.now(), timedelta())]
        self._log(0, 0, msg)
        return self

    def lap(self, msg='') -> tuple[datetime, datetime, datetime, timedelta, timedelta]:
        """
        记下当前的时刻。

        :param msg: 要输出的消息。
        :return: 开始时刻、上次记录时刻、当前时刻、距开始时间、距上次时间。
        """
        with Lock():
            if not self._marks:
                self.start('Automatically start...')

            head = self._marks[0][0]
            prev = self._marks[-1][0]
            curr = datetime.now()
            total = curr - head
            delta = curr - prev
            self._log(total.total_seconds(), delta.total_seconds(), msg)
            self._marks.append((curr, delta))
            return head, prev, curr, total, delta

    def stop(self, msg='Stopped.') -> datetime:
        """
        停止计时，但不清除所有标记。

        :param msg: 要输出的消息。
        :return: 当前时刻。
        """
        _, _, curr, _, _ = self.lap(msg)
        return curr


def is_leap(year: int) -> bool:
    """
    判断一个年份是否为闰年。
    """
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def get_last_monthday(year: int, month: int) -> int:
    """
    计算某年某月的最后一天是哪一天。
    """
    if month == 2 and is_leap(year):
        return 29
    return Datetime.DAYS_IN_MONTH[month]


class TimeFrame(IntEnum):
    YEAR = 0
    MONTH = 1
    DAY = 2
    HOUR = 3
    MINUTE = 4
    SECOND = 5
    MICROSECOND = 6


class Datetime(datetime):
    """
    增强型日期时间对象。
    """

    DAYS_IN_MONTH = (-1, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)

    # ---- 构造器 ----

    @classmethod
    def fromcalendar(cls, year: int, week: int, day: int, sunday_first=False) -> Datetime:
        """
        将某一年某一周的星期几转换为一个具体的日期。

        - ``sunday_first=False`` 时一年内第一个周一之前的日子都属于第 ``0`` 周。
        - ``sunday_first=True`` 时一年内第一个周日之前的日子都属于第 ``0`` 周。

        :param year: 具体年份。比如 2012、2023 等。
        :param week: 第几周。从 ``0`` 开始。
        :param day: 星期几。``0`` 表示周日、``1`` 表示周一，以此类推。
        :param sunday_first: 是否将周日作为一周的开始。
        :return: 一个具体的日期。
        """
        return cls.strptime(
            f'{year:04d}-{week:02d}-{day:1d}',
            '%Y-%U-%w' if sunday_first else '%Y-%W-%w',
        )

    @classmethod
    def fromdatetime(cls, _datetime: datetime) -> Datetime:
        """
        用 :class:`datetime` 构造对象。
        """
        return cls(
            _datetime.year, _datetime.month, _datetime.day,
            _datetime.hour, _datetime.minute, _datetime.second,
            _datetime.microsecond, _datetime.tzinfo, fold=_datetime.fold,
        )

    of = fromdatetime

    # ---- 转换器 ----

    def replace(
            self,
            year: Optional[int] = None,
            month: Optional[int] = None,
            day: Optional[int] = None,
            hour: Optional[int] = None,
            minute: Optional[int] = None,
            second: Optional[int] = None,
            microsecond: Optional[int] = None,
            _tzinfo: Optional[tzinfo] = ...,
            *,
            fold: Optional[int] = None,
            standard: bool = False,
    ) -> Datetime | datetime:
        """
        修改部分字段并返回一个新的日期时间。

        如果 ``standard=True`` 则固定返回 :class:`datetime` 对象。
        """
        return (datetime if standard else type(self))(
            year or self.year,
            month or self.month,
            day or self.day,
            hour or self.hour,
            minute or self.minute,
            second or self.second,
            microsecond or self.microsecond,
            self.tzinfo if _tzinfo is ... else _tzinfo,
            fold=fold or self.fold,
        )

    @classmethod
    def combine(
            cls,
            a: date | datetime,
            b: time | datetime | timedelta,
            _tzinfo: Optional[tzinfo] = ...
    ) -> Datetime:
        """
        将 a 的日期部分和 b 的时间部分组合为一个新的日期时间。

        :param a: 支持 :class:`data` 或 :class:`datetime` 及其子类的对象。
        :param b: 支持 :class:`time`、:class:`datetime` 或 :class:`timedelta` 及其子类的对象。
        :param _tzinfo: 时区。默认使用 b 的时区设置，如不需要可设置为 ``None`` 。
        :return: 组合得到的日期时间。
        """
        if _tzinfo is ...:
            _tzinfo = b.tzinfo
        if not isinstance(a, (date, datetime)):
            raise TypeError("argument 'a' must be a date or datetime instance")
        if not isinstance(b, (time, datetime, timedelta)):
            raise TypeError("argument 'b' must be a time, datetime, or timedelta instance")
        if isinstance(b, timedelta):
            b = Timedelta.of(b).base()

        return cls(
            a.year, a.month, a.day,
            b.hour, b.minute, b.second, b.microsecond,
            _tzinfo, fold=b.fold,
        )

    def empty(
            self,
            keeping_level: TimeFrame = TimeFrame.DAY,
            year: Optional[int] = None,
            month: Optional[int] = None,
            day: Optional[int] = None,
            hour: Optional[int] = None,
            minute: Optional[int] = None,
            second: Optional[int] = None,
            microsecond: Optional[int] = None,
    ) -> Datetime:
        """
        将某个层级以下（不含）的部分归零。

        >>> now = Datetime.now()
        >>> for frame in TimeFrame:
        >>>     print(
        >>>         now.empty(frame), frame, sep='\\t'
        >>>     )
        2024-01-01 00:00:00         TimeFrame.YEAR
        2024-09-01 00:00:00         TimeFrame.MONTH
        2024-09-17 00:00:00         TimeFrame.DAY
        2024-09-17 11:00:00         TimeFrame.HOUR
        2024-09-17 11:22:00         TimeFrame.MINUTE
        2024-09-17 11:22:33         TimeFrame.SECOND
        2024-09-17 11:22:33.245678  TimeFrame.MICROSECOND

        可以将时间的某个部分固定为指定值，比如将小时固定为凌晨四点：

        >>> for frame in TimeFrame:
        >>>     print(
        >>>         now.empty(frame, hour=4), frame, sep='\\t'
        >>>     )
        2024-01-01 04:00:00         TimeFrame.YEAR
        2024-09-01 04:00:00         TimeFrame.MONTH
        2024-09-17 04:00:00         TimeFrame.DAY
        2024-09-17 04:00:00         TimeFrame.HOUR
        2024-09-17 04:22:00         TimeFrame.MINUTE
        2024-09-17 04:22:33         TimeFrame.SECOND
        2024-09-17 04:22:33.245678  TimeFrame.MICROSECOND
        """
        index = keeping_level + 1
        origin = (
            year or self.year,
            month or self.month,
            day or self.day,
            hour or self.hour,
            minute or self.minute,
            second or self.second,
            microsecond or self.microsecond,
        )
        specified = (
            year or MINYEAR,
            month or 1,
            day or 1,
            hour or 0,
            minute or 0,
            second or 0,
            microsecond or 0,
        )
        return type(self)(
            *(origin[:index] + specified[index:]),
            tzinfo=self.tzinfo, fold=self.fold,
        )

    def fill(
            self,
            keeping_level: TimeFrame = TimeFrame.DAY,
            year: Optional[int] = None,
            month: Optional[int] = None,
            day: Optional[int] = None,
            hour: Optional[int] = None,
            minute: Optional[int] = None,
            second: Optional[int] = None,
            microsecond: Optional[int] = None,
    ) -> Datetime:
        """
        将某个层级以下（不含）的部分填满。

        >>> now = Datetime.now()
        >>> for frame in TimeFrame:
        >>>     print(
        >>>         now.fill(frame), frame, sep='\\t'
        >>>     )
        2024-12-31 23:59:59.999999    TimeFrame.YEAR
        2024-09-30 23:59:59.999999    TimeFrame.MONTH
        2024-09-09 23:59:59.999999    TimeFrame.DAY
        2024-09-09 11:59:59.999999    TimeFrame.HOUR
        2024-09-09 11:22:59.999999    TimeFrame.MINUTE
        2024-09-09 11:22:33.999999    TimeFrame.SECOND
        2024-09-09 11:22:33.245678    TimeFrame.MICROSECOND

        可以将时间的某个部分固定为给定值，比如将小时固定为凌晨四点：

        >>> for frame in TimeFrame:
        >>>     print(
        >>>         now.fill(frame), frame, sep='\\t'
        >>>     )
        2024-12-31 04:59:59.999999    TimeFrame.YEAR
        2024-09-30 04:59:59.999999    TimeFrame.MONTH
        2024-09-09 04:59:59.999999    TimeFrame.DAY
        2024-09-09 04:59:59.999999    TimeFrame.HOUR
        2024-09-09 04:22:59.999999    TimeFrame.MINUTE
        2024-09-09 04:22:33.999999    TimeFrame.SECOND
        2024-09-09 04:22:33.245678    TimeFrame.MICROSECOND
        """
        index = keeping_level + 1
        origin = [
            year or self.year,
            month or self.month,
            day or self.day,
            hour or self.hour,
            minute or self.minute,
            second or self.second,
            microsecond or self.microsecond,
        ]
        specified = [
            year or MAXYEAR,
            month or 12,
            day or 31,
            hour or 23,
            minute or 59,
            second or 59,
            microsecond or 999999,
        ]
        result = origin[:index] + specified[index:]
        result[2] = min(result[2], get_last_monthday(result[0], result[1]))
        return type(self)(*result, tzinfo=self.tzinfo, fold=self.fold)

    def calendar(self, sunday_first=False) -> tuple[int, int, int]:
        """
        计算当前日期是哪一年哪一周的周几。

        - ``sunday_first=False`` 时一年内第一个周一之前的日子都属于第 ``0`` 周。
        - ``sunday_first=True`` 时一年内第一个周日之前的日子都属于第 ``0`` 周。

        :param sunday_first: 是否将周日作为一周的开始。
        :return: 一个三元组，分别表示哪一、哪一周、周几。
        """
        return tuple(map(int, self.strftime('%Y-%U-%w' if sunday_first else '%Y-%W-%w').split('-')))

    # ---- 判断 ----

    def is_leap(self) -> bool:
        """
        当年是否为闰年。
        """
        return self.year % 4 == 0 and (self.year % 100 != 0 or self.year % 400 == 0)

    # ---- 属性 ----

    @property
    def last_monthday(self) -> int:
        """
        当月的最后一天是哪一天。
        """
        if self.month == 2 and self.is_leap():
            return 29
        return self.DAYS_IN_MONTH[self.month]


class Timedelta(timedelta):
    """
    增强型时间差对象。
    """

    # ---- 构造器 ----

    @classmethod
    def fromtime(cls, _time: time) -> Timedelta:
        """
        用 :class:`time` 构造时间差对象。

        换句话说就是 fromtime(_time) = _time - 00:00:00
        """
        return cls(
            seconds=_time.hour * 3600 + _time.minute * 60 + _time.second,
            microseconds=_time.microsecond,
        )

    @classmethod
    def fromtimedelta(cls, delta: timedelta) -> Timedelta:
        """
        用 :class:`timedelta` 构造时间差对象。
        """
        return cls(days=delta.days, seconds=delta.seconds, microseconds=delta.microseconds)

    of = fromtimedelta

    # ---- 转换 ----

    def replace(
            self,
            days: Optional[int] = None,
            seconds: Optional[int] = None,
            microseconds: Optional[int] = None,
            standard: bool = False,
    ) -> Timedelta | timedelta:
        """
        修改部分字段并返回一个新的时间差对象。

        如果 ``standard=True`` 则固定返回 :class:`timedelta` 对象。
        """
        return (timedelta if standard else type(self))(
            days or self.days,
            seconds or self.seconds,
            microseconds or self.microseconds,
        )

    def base(self, _time: Optional[time] = None) -> time:
        """
        基于某个时间叠加得到另一个时间。

        **该方法可能会在将在被废弃**！
        """
        if _time is None:
            s = self.seconds
            ms = self.microseconds
        else:
            ms = _time.microsecond + self.microseconds
            s = ms // 10 ** 6 + self.seconds
            ms = ms % 10 ** 6
        return time(
            hour=s // 3600 % 24,
            minute=s % 3600 // 60,
            second=s % 60,
            microsecond=ms,
        )


def daterange(start: date, stop: date, step: int = 1, closed=False) -> Generator[date, None, None]:
    """
    在一个日期范围内，按指定的步长迭代生成 :class:`date` 对象。

    :param start: 开始日期。
    :param stop: 结束日期。
    :param step: 步长。提供负数时，请确保开始日期晚于（即大于）结束日期。如果为 ``0`` 会引发 :class:`datetime` 。
    :param closed: 结束日期是否可以到达。
    :return: 生成 :class:`date` 对象的生成器。
    """
    if closed:
        ordinals = range(start.toordinal(), stop.toordinal() + step, step)
    else:
        ordinals = range(start.toordinal(), stop.toordinal(), step)

    return (date.fromordinal(o) for o in ordinals)


def weekrange(year: int, week: int, sunday_first=False) -> Generator[date, None, None]:
    """
    枚举生成某一周的所有日期。

    :param year: 具体年份。比如 2012、2023 等。
    :param week: 一年中的第几周。从 ``0`` 开始。
    :param sunday_first: 是否以周日为一周的开始。
    :return: 生成 :class:`date` 对象的生成器。
    """
    start = datetime.strptime(
        f'{year:04d}-{week:02d}-{0 if sunday_first else 1}',
        '%Y-%U-%w' if sunday_first else '%Y-%W-%w',
    ).date()
    return (start + timedelta(days=i) for i in range(7))
