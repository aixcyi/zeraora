"""
日志相关。
"""
from __future__ import annotations

__all__ = [
    'BearTimer',
]

import logging
import os
import sys
import time
from datetime import datetime, timedelta
from functools import wraps
from logging.handlers import TimedRotatingFileHandler
from threading import Lock

from zeraora.daytime import delta2s
from zeraora.utils import dict_

logger = logging.getLogger('zeraora.bear')


class BearTimer(object):
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
            'Console': dict_(
                level='DEBUG',
                class_='logging.StreamHandler',
                filters=[],
                formatter='bear',
            ),
        },
        loggers={
            'zeraora.bear': dict(
                level='DEBUG',
                handlers=['Console'],
                propagate=False,
            ),
        },
    )

    def __init__(self, label: str = None, *_, **__):
        """
        熊牌秒表。对代码运行进行计时，并向名为 "zeraora.bear" 的logger发送DEBUG等级的日志。

        ----

        使用前，需要先启用日志输出：

        >>> import logging.config
        >>> from zeraora.logx import BearTimer
        >>>
        >>> logging.config.dictConfig(BearTimer.CONFIG)
        >>> bear = BearTimer()

        对于使用 Django 的项目可以改为在 settings.py 中进行如下设置：

        >>> LOGGING = {
        >>>     'version': 1,
        >>>     'formatters': {...},
        >>>     'filters': {...},
        >>>     'handlers': {
        >>>         'Console': {  # 确保有一个控制台输出
        >>>             'level': 'DEBUG',
        >>>             'class': 'logging.StreamHandler',
        >>>         },
        >>>         ...
        >>>     },
        >>>     'loggers': {
        >>>         'zeraora.bear': {  # 添加相应的日志记录器
        >>>             'level': 'DEBUG',
        >>>             'handlers': ['Console'],
        >>>         },
        >>>     },
        >>> }

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
        >>> from zeraora.logx import BearTimer
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
            self._log(delta2s(total), delta2s(delta), msg)
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


# noinspection PyPep8Naming
class CommonTimedRotatingFileHandler(TimedRotatingFileHandler):
    """
    用于记录到文件的处理程序，以特定的时间间隔轮换日志文件。
    如果 ``backupCount`` > 0，则翻转完成后，不会保留超过 ``backupCount`` 个文件 - 最旧的文件将被删除。

    转载自 `解决 Django 多进程下，logging 记录日志错乱问题 <https://zhuanlan.zhihu.com/p/141878111>`_ 。
    """

    @property
    def dfn(self):
        currentTime = int(time.time())
        # get the time that this sequence started at and make it a TimeTuple
        dstNow = time.localtime(currentTime)[-1]
        t = self.rolloverAt - self.interval
        if self.utc:
            timeTuple = time.gmtime(t)
        else:
            timeTuple = time.localtime(t)
            dstThen = timeTuple[-1]
            if dstNow != dstThen:
                if dstNow:
                    addend = 3600
                else:
                    addend = -3600
                timeTuple = time.localtime(t + addend)
        dfn = self.rotation_filename(self.baseFilename + "." + time.strftime(self.suffix, timeTuple))

        return dfn

    def shouldRollover(self, record):
        """
        是否应该执行日志滚动操作：
        1、存档文件已存在时，执行滚动操作
        2、当前时间 >= 滚动时间点时，执行滚动操作
        """
        dfn = self.dfn
        t = int(time.time())
        if t >= self.rolloverAt or os.path.exists(dfn):
            return 1
        return 0

    def doRollover(self):
        """
        执行滚动操作
        1、文件句柄更新
        2、存在文件处理
        3、备份数处理
        4、下次滚动时间点更新
        """
        if self.stream:
            self.stream.close()
            self.stream = None
        # get the time that this sequence started at and make it a TimeTuple

        dfn = self.dfn

        # 存档log 已存在处理
        if not os.path.exists(dfn):
            self.rotate(self.baseFilename, dfn)

        # 备份数控制
        if self.backupCount > 0:
            for s in self.getFilesToDelete():
                os.remove(s)

        # 延迟处理
        if not self.delay:
            self.stream = self._open()

        # 更新滚动时间点
        currentTime = int(time.time())
        newRolloverAt = self.computeRollover(currentTime)
        while newRolloverAt <= currentTime:
            newRolloverAt = newRolloverAt + self.interval

        # If DST changes and midnight or weekly rollover, adjust for this.
        if (self.when == 'MIDNIGHT' or self.when.startswith('W')) and not self.utc:
            dstAtRollover = time.localtime(newRolloverAt)[-1]
            dstNow = time.localtime(currentTime)[-1]
            if dstNow != dstAtRollover:
                if not dstNow:  # DST kicks in before next rollover, so we need to deduct an hour
                    addend = -3600
                else:  # DST bows out before next rollover, so we need to add an hour
                    addend = 3600
                newRolloverAt += addend
        self.rolloverAt = newRolloverAt
