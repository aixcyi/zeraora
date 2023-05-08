"""
纯工具类。
"""
import sys
from datetime import datetime
from functools import wraps
from io import TextIOWrapper
from logging import Logger, DEBUG, getLevelName
from typing import Tuple, Optional, Union, NoReturn, TextIO

from .converters import delta2s, represent


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


class ReprMixin(object):
    """
    生成通用representation的工具类。

    格式类似于 ``<User(1) female name="meow" age=12 birth=[2012-01-23]>``，
    包含自身类名、主键、标签、属性名和值。

    直接或间接继承时请放在第一父类。
    """

    def __repr__(self) -> str:
        kls = self._obtain_kls()
        pkv = self._obtain_pk()
        tags = self._obtain_tags()
        attrs = self._obtain_attrs()
        content = (
                (f'({pkv})' if pkv else '') +
                (f' {tags}' if tags else '') +
                (f' {attrs}' if attrs else '')
        )
        return f'<{kls}{content}>'

    class AttributeMeta:
        """
        用于控制生成 representation 时需要带上哪些属性。

        注意：这个内部类不会被实例化！

        AttributeMeta 的变量代表你的类对象在运行时已经存在的属性，
        变量值应当是一个字符串，表示生成 representation 时这个属性的名称是什么。

        AttributeMeta 的变量允许接收一个返回值为字符串的函数作为类型注解，
        用于转换你的类对象的属性值，并直接作为 representation 里这个属性的值。
        """

    def _obtain_attrs(self) -> str:
        def obtain():
            for attr, name in attributes.items():
                if attr.startswith('_'):
                    continue
                mapper = annotations.get(attr, represent)
                value = getattr(self, attr)
                value = mapper(value) if callable(mapper) else value
                yield f'{name}={value}'

        attributes = self.AttributeMeta.__dict__
        annotations = attributes.get('__annotations__', {})
        return ' '.join(filter(None, obtain()))

    class TagMeta:
        """
        用于控制生成 representation 时需要带上哪些标签。

        注意：这个内部类不会被实例化！

        TagMeta 的变量代表你的类对象在运行时已经存在的属性，变量值可以是
          - 一个字符串，表示这个属性为 ``True`` 时 representation 里才会出现的标签的名称；
            如果属性为 ``False`` 则不会出现这个标签。
          - 一个元组且仅有两个字符串，表示这个属性分别为
            ``False`` 和 ``True`` 时 representation 里会出现的标签的名称。
          - 一个列表或一个字典，则使用属性值对这个列表或字典进行取值，
            以此作为 representation 里出现的标签的名称。

        TagMeta 的变量允许接收一个返回值为字符串的函数作为类型注解，
        用于进一步转换你的类对象的属性值，若未提供，默认使用 bool() 来转换。
        """

    def _obtain_tags(self) -> str:
        def obtain():
            for attr, option in attributes.items():
                if attr.startswith('_'):
                    continue
                mapper = annotations.get(attr, None)
                value = getattr(self, attr)
                value = mapper(value) if callable(mapper) else value
                if isinstance(option, str) and value:
                    yield option
                elif isinstance(option, tuple):
                    yield option[bool(value)]
                elif isinstance(option, (list, dict)):
                    yield option[value]
                else:
                    pass  # pragma: no cover

        attributes = self.TagMeta.__dict__
        annotations = attributes.get('__annotations__', {})
        return ' '.join(filter(None, obtain()))

    def _obtain_pk(self) -> str:
        if hasattr(self, 'pk'):
            pk = self.pk
        elif hasattr(self, 'id'):
            pk = self.id
        else:
            return ''
        return pk if isinstance(pk, str) else represent(pk)

    def _obtain_kls(self) -> str:
        return self.__class__.__name__
