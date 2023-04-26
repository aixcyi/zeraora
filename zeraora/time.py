"""
时间相关的处理。包括日期时间类型转换和计时。
"""

import sys
from datetime import timedelta, datetime
from functools import wraps
from io import TextIOWrapper
from logging import Logger, DEBUG, getLevelName
from typing import Tuple, Optional, Union, NoReturn, TextIO


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


class BearTimer(object):
    fmt = '[{head:%H:%M:%S.%f}] [{level}] [{title}] [{total:.6f} +{delta:.6f}]: {msg}'
    level = DEBUG

    def __init__(self, title: str = None, output: Union[TextIOWrapper, TextIO, Logger] = None):
        """
        熊牌计时器。对代码运行进行计时，并打印时间和提示。

        比较简单的用法是使用 with 语句包裹需要计时的部分，
        它会在开始执行前启动计时，在执行完毕或出现异常而离开with后停止计时。

        >>> with BearTimer() as bear:
        >>>     summary = 0
        >>>     for i in range(1000):
        >>>         if not i % 67:
        >>>             bear.step(f'loop to {i} now.')
        >>>         summary += i

        如果需要对一整个函数的运行进行计时，那么可以将计时器作为装饰器使用：

        >>> @BearTimer()
        >>> def prepare_order(request, *args, **kwargs):
        >>>     # 业务逻辑
        >>>     pass

        如果不方便使用 with 包裹，可以直接实例化一个类对象。
        每一个对象都是独立的计时器，互不影响。

        >>> bear = BearTimer()
        >>> bear.start()
        >>> bear.stop()

        :param title: 计时器的标题，用以标明输出信息归属于哪个计时器。默认从打印消息时的上下文中获取。
        :param output: 消息打印到哪里去。默认是系统标准输出。可以是一个文件IO对象，也可以是一个日志记录器。
        """
        self._start = None  # 计时开始时间
        self._point = None  # 中途标记时间（用于计算距离上次标记过去了多久）
        self._title = title
        self.output = output
        if not self._title:
            if hasattr(sys, '_getframe'):
                self._title = sys._getframe().f_back.f_code.co_name
            else:
                self._title = '<UNTITLED>'

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            self._title = func.__name__
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

    def handle(self, full_message: str) -> NoReturn:
        """
        将消息发送到指定位置。这个位置允许是文件IO对象，或者是日志记录器。

        不应直接使用此方法。

        :param full_message: 完整的消息内容。
        :return: 无。
        """
        if hasattr(self.output, 'log') and callable(self.output.log):
            self.output: Logger
            self.output.log(self.level, full_message)

        elif hasattr(self.output, 'write') and callable(self.output.write):
            self.output: TextIOWrapper
            print(full_message, file=self.output)

        else:
            print(full_message)

    def record(self, msg: str = '', *args, **kwargs) -> datetime:
        """
        打印一行消息，标明此刻的时间、经历的时长、距上次打印的时长、计时器标题，以及附加的消息。

        不应直接使用这个方法。

        :param msg: 要附加的消息。默认为空文本。
        :param args: 其它需要打印的位置参数。
        :param kwargs: 其它需要打印的关键字参数。
        :return: 此时的时刻。
        """
        now = datetime.now()
        total = delta2s(now - self._start) if self._start else 0
        delta = delta2s(now - self._point) if self._point else 0
        title = self._title if self._title else ''
        message = self.fmt.format(
            head=now, total=total, delta=delta, title=title, msg=msg,
            level=getLevelName(self.level), *args, **kwargs,
        )
        self._point = now
        self.handle(message)
        return now

    def start(self, msg='Starting...'):
        """
        开始计时。

        如果计时尚未结束，会重新开始计时，中途记录的标记也会被清除。

        :param msg: 要附加的消息。
        :return: 计时器对象自身。
        """
        self._point = None
        self._start = datetime.now()
        self.record(msg)
        return self

    def step(self, msg='') -> Tuple[Optional[datetime], datetime]:
        """
        中途标记。

        用此方法可以计算出距离上一次标记/开始计时过去了多久。

        如果计时器尚未开始计时，那么过去的时间始终是 0 秒。

        :param msg: 要附加的消息。
        :return: 二元元组。包含上一次标记/开始计时的时刻，和此时的时刻。
        """
        prev = self._point
        curr = self.record(msg)
        return prev, curr

    def stop(self, msg='Stopped.') -> datetime:
        """
        结束计时。

        :param msg: 要附加的消息。
        :return: 此时的时刻。
        """
        curr = self.record(msg)
        self._start = None
        return curr
