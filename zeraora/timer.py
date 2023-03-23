__all__ = [
    'BearTimer',
]

import sys
from datetime import datetime
from io import TextIOWrapper

from zeraora.times import delta2ms


class BearTimer(object):
    """
    熊牌计时器。

    这个类可以让你对代码进行计时功能并输出提示。

    最简单的用法是使用 with 语句包裹需要计时的代码：
    >>> with BearTimer():
    >>>     for i in range(1000000):
    >>>         print(i)

    如果不方便使用 with 包裹，可以直接实例化一个类对象：
    >>> bear = BearTimer()
    >>> bear.start()
    >>> bear.stop()

    计时开始后，如果需要打印提示，请使用 .step() 方法，例如：
    >>> with BearTimer() as bear:
    >>>     summary = 0
    >>>     for i in range(1000000):
    >>>         bear.step(f'loop to {i} now.')
    >>>         summary += i
    又或者是
    >>> bear = BearTimer()
    >>> bear.start()
    >>> bear.step('operate somethings now.')
    >>> bear.stop()
    """

    @staticmethod
    def get_context_name():
        try:
            return sys._getframe().f_back.f_code.co_name
        except AttributeError:
            raise RuntimeError(
                'Current system NOT support this class.\n'
                '当前操作系统不支持使用该工具类。'
            ) from None

    def __init__(self, title: str = None):
        """
        :param title: 计时器的标题，用以标明输出信息归属于哪个计时器。默认从上下文中获取。
        :raise RuntimeError: 当前操作系统不支持使用该工具类。仅当没有提供title且无法从上下文中获取时抛出。
        """
        self._start = None  # 计时开始时间
        self._point = None  # 中途标记时间（用于计算距离上次标记过去了多久）
        self._title = title if title else self.get_context_name()

    def __call__(self, function):
        def inner(*args, **kwargs):
            self.start()
            returns = function(*args, **kwargs)
            self.stop()
            return returns

        return inner

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, traceback):
        self.stop()

    def output(
            self,
            msg: str = '',
            fmt: str = '{head:%H:%M:%S.%f}, {minutes:d}:{seconds:f}, {title} | {msg}',
            *args,
            end: str = '\n',
            file: TextIOWrapper = sys.stdout,
            **kwargs,
    ) -> datetime:
        """
        打印一行消息，标明此刻的时间、经历的时长、计时器标题，以及附加的消息。

        你不应该使用这个方法，它只应在自定义这个类时被重写。

        :param msg: 要附加的消息。默认为空文本。
        :param fmt: 字符串的格式。具体参数见默认值。
        :param end: 要以什么结尾。因为一般是单行打印的，故有此参数。默认是 ”\n“ 。
        :param file: 打印到哪里去。默认是系统标准输出。
        :param args: 其它需要打印的位置参数。
        :param kwargs: 其它需要打印的关键字参数。
        :return: 此时的时刻。
        """
        now = datetime.now()
        m, s = delta2ms(now - self._start) if self._start else (0, 0)
        print(
            fmt.format(*args, head=now, minutes=m, seconds=s,
                       title=self._title, msg=msg, **kwargs),
            file=file,
            end=end,
        )
        return now

    def start(self, msg='Starting...'):
        """
        开始计时。

        如果计时器还没结束，会重新开始计时，中途的标记也会被清除。

        :param msg: 要附加的消息。
        :return: 计时器对象自身。
        """
        self._point = None
        self._start = self.output(msg + ('＜计时已重新开始＞' if self._start else ''))
        return self

    def step(self, msg=None):
        """
        中途标记。

        用此方法可以计算出距离上一次标记/开始计时过去了多久。

        如果计时器尚未开始计时，那么过去的时间始终是 0 秒。

        :param msg: 要附加的消息。留空则显示过了多久。
        :return: 一个元组，包含上一次标记/开始计时的时刻，和此时的时刻。
        """
        if self._start is not None:
            if self._point is None:
                self._point = self._start
            m, s = delta2ms(datetime.now() - self._point)
        else:
            m, s = 0, 0
        prev = self._point
        curr = self.output(msg if msg else f'(+{m:d}:{s:f})')
        self._point = curr
        return prev, curr

    def stop(self, msg='Stopped.') -> datetime:
        """
        结束计时。

        :param msg: 要附加的消息。
        :return: 此时的时刻。
        """
        curr = self.output(msg + ('' if self._start else '＜计时还未开始＞'))
        self._start = None
        return curr
