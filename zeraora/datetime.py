"""
日期时间相关工具。
"""
from __future__ import annotations

__all__ = [
    'DateTime',
    'DateRange',
    'BearTimer',
]

import logging
import sys
from datetime import date, datetime, timedelta
from functools import wraps
from threading import Lock
from typing import Generator

logger = logging.getLogger('zeraora.datetime')


class DateTime(datetime):
    """
    增强型日期时间对象。
    """

    # -------- 装箱拆箱 --------

    @classmethod
    def of(cls, dt: datetime) -> DateTime:
        return cls(
            dt.year, dt.month, dt.day,
            dt.hour, dt.minute, dt.second,
            dt.microsecond, dt.tzinfo, fold=dt.fold
        )

    def to(self) -> datetime:
        return datetime(
            self.year, self.month, self.day,
            self.hour, self.minute, self.second,
            self.microsecond, self.tzinfo, fold=self.fold
        )

    # -------- 快速变换 --------

    def start_of_year(self) -> DateTime:
        """
        将日期部分固定为当年的1月1日。
        """
        return self.replace(month=1, day=1)

    def end_of_year(self) -> DateTime:
        """
        将日期部分固定为当年的12月31日。
        """
        return self.replace(month=12, day=31)

    def start_of_day(self) -> DateTime:
        """
        将时间部分固定为 ``00:00:00.000000`` 。
        """
        return self.replace(hour=0, minute=0, second=0, microsecond=0)

    def end_of_day(self) -> DateTime:
        """
        将时间部分固定为 ``23:59:59.999999`` 。
        """
        return self.replace(hour=23, minute=59, second=59, microsecond=10 ** 6 - 1)

    # -------- 计算方法 --------

    @classmethod
    def of_week(cls, year: int, week_in_year: int, day_in_week: int, sunday_first=False) -> DateTime:
        """
        将某一年的某一周的星期几转换为一个具体的日期。

        :param year: 具体年份。比如 2012、2023 等。
        :param week_in_year: 一年中的第几周。从 0 开始。
        :param day_in_week: 星期几。0 表示周日、1 表示周一，以此类推。
        :param sunday_first: 是否以周日为一周的开始。
        :return: 一个 DateTime 对象。
        """
        day = f'{year:04d}-{week_in_year:02d}-{day_in_week:1d}'
        fmt = '%Y-%U-%w' if sunday_first else '%Y-%W-%w'
        return cls.strptime(day, fmt)

    def get_week(self, sunday_first=False) -> int:
        """
        计算自当年开始的周序号。

        一年中第一个星期一（如果 ``sunday_first`` 为 ``True`` 则是星期日）之前的日子都算作第 ``0`` 周。

        :param sunday_first: 是否以周日作为一周的开始。
        :return: 一个从 0 开始递增的整数。
        """
        return int(self.strftime('%U') if sunday_first else self.strftime('%W'))

    get_week_in_year = get_week

    def get_week_in_month(self, sunday_first=False) -> int:
        """
        计算自当月开始的周序号。

        一个月中第一个星期一（如果 ``sunday_first`` 为 ``True`` 则是星期日）之前的日子都算作第 ``0`` 周。

        :param sunday_first: 是否以周日作为一周的开始。
        :return: 一个从 0 开始递增的整数。
        """
        # TODO: 待办


class DateRange:
    """
    日期范围工具类。
    """

    @staticmethod
    def walk(start: date, stop: date, step: int = 1, closed=False) -> Generator[date, None, None]:
        """
        根据起始日期确定一个日期范围。

        :param start: 开始日期。
        :param stop: 结束日期。
        :param step: 步长。提供负数时，请确保开始日期晚于（即大于）结束日期。如果为 ``0`` 会引发 ``ValueError`` 。
        :param closed: 结束日期是否可以到达。
        :return: 迭代元素类型为 ``date`` 的可迭代对象。
        """
        if closed:
            ordinals = range(start.toordinal(), stop.toordinal() + step, step)
        else:
            ordinals = range(start.toordinal(), stop.toordinal(), step)

        return (date.fromordinal(o) for o in ordinals)

    @staticmethod
    def by_week(year: int, week_in_year: int, sunday_first=False) -> Generator[date, None, None]:
        """
        计算一年中某一周对应的日期范围。

        :param year: 具体年份。比如 2012、2023 等。
        :param week_in_year: 一年中的第几周。从 0 开始。
        :param sunday_first: 是否以周日为一周的开始。
        :return: 迭代元素类型为 ``date`` 的可迭代对象。
        """
        start = datetime.strptime(
            f'{year:04d}-{week_in_year:02d}-{0 if sunday_first else 1}',
            '%Y-%U-%w' if sunday_first else '%Y-%W-%w',
        ).date()
        return (start + timedelta(days=i) for i in range(7))


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
