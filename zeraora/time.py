__all__ = [
    'FoxStopwatch',
    'BearStopwatch',
]

import logging
import logging.config
import sys
from datetime import datetime, timedelta
from functools import wraps
from typing import NamedTuple


class _Mark(NamedTuple):
    """
    时刻标记。

    用于标定某一个时刻。
    """

    head: datetime
    """开始时刻。即开始计时的时刻。"""

    prev: datetime
    """上一时刻。即上一次标记的时刻。"""

    curr: datetime
    """当前时刻。即这一次标记的时刻。"""

    msg: str
    """相关消息。"""

    @property
    def total(self) -> timedelta:
        """“当前时刻”减去“开始时刻”的值。"""
        return self.curr - self.head

    @property
    def delta(self) -> timedelta:
        """“当前时刻”减去“上一时刻”的值。"""
        return self.curr - self.prev


class FoxStopwatch:

    def __init__(self, name: str = None, *args, **kwargs):
        """
        狸子秒表。

        对代码运行进行正向计时，并通过 ``print()`` 在控制台打印。

        ----

        最简单是使用 ``with`` 语句包裹需要计时的部分：

        >>> with FoxStopwatch() as fox:
        >>>     # 业务逻辑
        >>>     pass

        如需对一整个函数进行计时，可以作为装饰器使用：

        >>> @FoxStopwatch()
        >>> def do_somthing():
        >>>     # 业务逻辑
        >>>     pass

        带有多个装饰器时，秒表放哪里取决于你的计时范围：

        >>> from rest_framework.decorators import api_view
        >>> from zeraora.time import FoxStopwatch
        >>>
        >>> @FoxStopwatch()  # 从请求转发过来那一刻开始计时
        >>> @api_view(['GET'])
        >>> def query_status(request):
        >>>     # 业务逻辑
        >>>     pass
        >>>
        >>> @api_view(['POST'])
        >>> @FoxStopwatch()  # 从login()执行那一刻开始计时
        >>> def login(request):
        >>>     # 业务逻辑
        >>>     pass

        此外还可以实例化一个对象。每个对象都是独立的秒表，互不影响。

        >>> fox = FoxStopwatch()
        >>> fox.start()
        >>> # 业务逻辑
        >>> fox.stop()

        :param name: 秒表的标题，用以标明输出信息归属于哪个秒表。默认从打印消息时的上下文中获取。
        """
        self.name = str(name) or self._get_context_name() or self.__class__.__name__
        self.marks: list[_Mark] = []

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            self.name = func.__name__
            self.start()
            returns = func(*args, **kwargs)
            self.stop()
            return returns

        return wrapper

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type: type[BaseException], exc_val: BaseException, traceback):
        self.stop()

    @classmethod
    def _get_context_name(cls) -> str:
        if not hasattr(sys, '_getframe'):
            return ''
        try:
            # noinspection PyUnresolvedReferences,PyProtectedMember
            return sys._getframe().f_back.f_code.co_name
        except AttributeError:
            return ''

    def _log(self, mark: _Mark):
        """
        记录日志。

        您可以重写该方法，决定打印的格式。

        :param mark: 标记。
        :return: 自身。
        """
        total = mark.total.total_seconds()
        delta = mark.delta.total_seconds()
        print(f'[{self.name}] [{total:.9f} {delta:+.9f}]: {mark.msg}')
        return self

    def start(self, msg='开始计时……') -> _Mark:
        """
        开始计时。

        - 这个方法会清除所有标记，然后标记当前时刻。

        :param msg: 记录消息。
        :return: 新的计时标记。
        """
        mark = _Mark(head := datetime.now(), head, head, msg)
        self.marks.clear()
        self.marks.append(mark)
        self._log(mark)
        return mark

    def lap(self, msg='') -> _Mark:
        """
        标记此刻。

        - 如果计时尚未开始，会改为开始计时。

        :param msg: 记录消息。
        :return: 新的计时标记。
        """
        if not self.marks:
            return self.start(msg or '自动开始计时……')

        mark = _Mark(self.marks[0].head, self.marks[-1].head, datetime.now(), msg or '已标记~')
        self.marks.append(mark)
        self._log(mark)
        return mark

    def stop(self, msg='停止计时。') -> _Mark:
        """
        标记当前时刻，然后停止计时，最后清除所有标记。

        :param msg: 记录消息。
        :return: 新的计时标记。
        """
        if not self.marks:
            mark = _Mark(head := datetime.now(), head, head, msg)
            self._log(mark)
        else:
            mark = _Mark(self.marks[0].head, self.marks[-1].head, datetime.now(), msg)
            self._log(mark)
            self.marks.clear()
        return mark

    def print(self) -> None:
        """
        打印所有计时标记。
        """
        if not self.marks:
            print('<没有标记下任何一个时刻>')
            return
        for mark in self.marks:
            print(
                f'{mark.curr:%H:%M:%S.%f}\t',
                f'{mark.total.total_seconds():.9f}',
                f'{mark.delta.total_seconds():+.9f}',
                mark.msg,
                sep='\x20\x20',
            )


class BearStopwatch(FoxStopwatch):
    LEVEL = 'DEBUG'
    LOGGER = 'zeraora.bear'
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
                'level': LEVEL,
                'class': 'logging.StreamHandler',
                'filters': [],
                'formatter': 'bear',
            },
        },
        loggers={
            LOGGER: dict(
                level=LEVEL,
                handlers=['Console'],
                propagate=False,
            ),
        },
    )

    def __init__(self, name: str = None, *args, **kwargs):
        """
        熊牌秒表。

        对代码运行进行正向计时，并通过日志显示。

        ----

        使用前，需要先启用日志输出： ::

            from zeraora.time import BearStopwatch

            bear = BearStopwatch.configit()

        若是使用装饰器，则可以 ::

            from zeraora.time import BearStopwatch

            @BearStopwatch.configit()
            def main():
                pass

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
                    BearStopwatch.LOGGER: {  # 添加相应的日志记录器
                        'level': 'DEBUG',  # 可以重写 BearStopwatch.log() 来自定义等级
                        'handlers': ['Console'],
                    },
                },
            }

        ----

        最简单是使用 ``with`` 语句包裹需要计时的部分：

        >>> with BearStopwatch() as bear:
        >>>     # 业务逻辑
        >>>     pass

        如需对一整个函数进行计时，可以作为装饰器使用：

        >>> @BearStopwatch()
        >>> def do_somthing():
        >>>     # 业务逻辑
        >>>     pass

        带有多个装饰器时，秒表放哪里取决于你的计时范围：

        >>> from rest_framework.decorators import api_view
        >>> from zeraora.time import BearStopwatch
        >>>
        >>> @BearStopwatch()  # 从请求转发过来那一刻开始计时
        >>> @api_view(['GET'])
        >>> def query_status(request):
        >>>     # 业务逻辑
        >>>     pass
        >>>
        >>> @api_view(['POST'])
        >>> @BearStopwatch()  # 从login()执行那一刻开始计时
        >>> def login(request):
        >>>     # 业务逻辑
        >>>     pass

        此外还可以实例化一个对象。每个对象都是独立的秒表，互不影响。

        >>> bear = BearStopwatch()
        >>> bear.start()
        >>> # 业务逻辑
        >>> bear.stop()

        :param name: 秒表的标题，用以标明输出信息归属于哪个秒表。默认从打印消息时的上下文中获取。
        """
        super().__init__(name, *args, **kwargs)
        self.logger = logging.getLogger(self.LOGGER)

    @classmethod
    def configit(cls, name: str = None, *args, **kwargs) -> "BearStopwatch":
        """
        配置日志系统，并创建一个熊牌秒表；参数与 :class:`BearStopwatch` 一致。
        """
        logging.config.dictConfig(BearStopwatch.CONFIG)
        return cls(name, *args, **kwargs)

    def _log(self, mark: _Mark):
        """
        记录日志。

        - 发送的日志等级默认为 ``BearStopwatch.LEVEL`` 。
        - 日志记录器 Logger 的名称见 ``BearStopwatch.LOGGER`` 。

        :param mark: 标记。
        :return: 自身。
        """
        total = mark.total.total_seconds()
        delta = mark.delta.total_seconds()
        self.logger.log(
            logging.getLevelName(BearStopwatch.LEVEL),
            f'[{self.name}] [{total:.9f} {delta:+.9f}]: {mark.msg}'
        )
        return self
