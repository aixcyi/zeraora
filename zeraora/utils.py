"""
偏工具属性的类与函数。
"""
import logging
import sys
from datetime import datetime
from functools import wraps
from typing import Tuple, Optional

from .converters import delta2s, represent

logger_bear = logging.getLogger('zeraora.bear')

bear_config = {
    'version': 1,
    'formatters': {
        'bear': {
            'format': '[%(asctime)s] [%(levelname)s] %(message)s',
        },
        'bear_plus': {
            'format': (
                '[%(asctime)s] [%(levelname)s] '
                '[%(module)s.%(funcName)s:%(lineno)d] '
                '%(message)s'
            )
        },
    },
    'filters': {},
    'handlers': {
        'Console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'filters': [],
            'formatter': 'bear',
        },
    },
    'loggers': {
        'zeraora.bear': {
            'level': 'DEBUG',
            'handlers': ['Console'],
            'propagate': False,
        },
    },
}


class BearTimer(object):

    def __init__(self, label: str = None, printable=True):
        """
        熊牌计时器。对代码运行进行计时，并打印时间和提示。

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
        >>> from zeraora.utils import BearTimer
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

        若需要将计时消息输出到日志而非标准输出时，如果没有使用框架，可以通过以下方法启用日志记录：

        >>> import logging.config
        >>> from zeraora.utils import BearTimer, bear_config
        >>>
        >>> logging.config.dictConfig(bear_config)
        >>> bear = BearTimer(printable=False)

        :param label: 计时器的标题，用以标明输出信息归属于哪个计时器。默认从打印消息时的上下文中获取。
        :param printable: 若为True，消息会打印到系统标准输出；
                          若为False，则向名为 "zeraora.bear" 的Logger发送DEBUG等级的日志。
        """
        self._start = None  # 计时开始时间
        self._point = None  # 中途标记时间（用于计算距离上次标记过去了多久）
        self._print = printable
        self._label = sys._getframe().f_back.f_code.co_name if not label and hasattr(sys, '_getframe') else str(label)

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

    def _record(self, msg: str = '') -> datetime:
        """
        打印一行消息，标明此刻的时间、经历的时长、距上次打印的时长、计时器标题，以及附加的消息。

        :param msg: 要附加的消息。默认为空文本。
        :return: 此时的时刻。
        """
        now = datetime.now()
        total = delta2s(now - self._start) if self._start else 0
        delta = delta2s(now - self._point) if self._point else 0
        if self._print:
            print(f'[{now:%H:%M:%S.%f}] [{self._label}] [{total:.6f} +{delta:.6f}]: {msg}')
        else:
            logger_bear.debug(f'[{self._label}] [{total:.6f} +{delta:.6f}]: {msg}')
        self._point = now
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
        self._record(msg)
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
        curr = self._record(msg)
        return prev, curr

    def stop(self, msg='Stopped.') -> datetime:
        """
        结束计时。

        :param msg: 要附加的消息。
        :return: 此时的时刻。
        """
        curr = self._record(msg)
        self._start = None
        return curr


class ReprMixin(object):
    """
    重写 ``self.__repr__()`` 来生成特定格式的representation。

    `请作为第一父类继承`。

    格式：<类名(主键) 标签1 标签2 ... 属性1=值1 属性2=值2 ...>

    例如：``<User(1) female name="meow" age=12 birth=[2012-01-23]>``

    >>> from datetime import date
    >>> from django.db import models
    >>>
    >>> def _grade(join_date: date) -> str:
    >>>     today = date(2023, 9, 1)
    >>>     years = today.year - join_date.year + 1
    >>>     return str(years)
    >>>
    >>> class Student(ReprMixin, models.Model):
    >>>     '''学生信息'''
    >>>     name = models.CharField(max_length=150)
    >>>     birth = models.DateField()
    >>>     female = models.BooleanField(default=False)
    >>>     leader = models.BooleanField(default=False)
    >>>     joined = models.DateField()
    >>>
    >>>     class TagMeta:
    >>>         female = 'male', 'female'  # 分别为 False、True 时显示
    >>>         leader = 'leader'  # 仅为 True 时显示
    >>>
    >>>     class AttributeMeta:
    >>>         name = 'name'
    >>>         birth = 'birth'
    >>>         joined: _grade = 'grade'  # 相当于 _grade(self.joined)
    >>>
    >>> amy = Student(
    >>>     name='amy', birth=date(2012, 1, 23), id=1,
    >>>     female=True, joined=date(2020, 9, 1),
    >>> )
    >>> print(repr(amy))
    >>> # <Student(1) female name="amy" birth=[2012-01-23] grade=4>
    >>>
    >>> jim = Student(
    >>>     name='jim', birth=date(2013, 6, 1), id=2,
    >>>     leader=True, joined=date(2021, 9, 1),
    >>> )
    >>> print(repr(jim))
    >>> # <Student(2) male leader name="jim" birth=[2013-06-01] grade=3>

    ``TagMeta`` 的变量可以直接赋予映射关系：

    >>> from django.db import models
    >>>
    >>> SUBJECTS = ['工学', '哲学', '法学', '文学', '理学', '农学', '医学',
    >>>             '经济学', '教育学', '历史学', '管理学', '军事学', '艺术学']
    >>>
    >>> class Grade(models.IntegerChoices):
    >>>     FRESHMAN = 1, 'Freshman'
    >>>     SOPHOMORE = 2, 'Sophomore'
    >>>     JUNIOR = 3, 'Junior'
    >>>     SENIOR = 4, 'Senior'
    >>>
    >>> class Student(ReprMixin, models.Model):
    >>>     '''学生信息。'''
    >>>     name = models.CharField(max_length=150)
    >>>     grade = models.IntegerField(choices=Grade.choices)
    >>>     subject = models.IntegerField()
    >>>
    >>>     class TagMeta:
    >>>         grade = dict(Grade.choices)
    >>>         subject = SUBJECTS
    >>>
    >>>     class AttributeMeta:
    >>>         name = 'name'
    >>>
    >>> leo = Student(
    >>>     id=3, name='leo', grade=Grade.JUNIOR, subject=1
    >>> )
    >>> print(repr(leo))
    >>> # <Student(3) Junior 工学 name="leo">
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
