"""
偏工具属性的类与函数。
"""
from __future__ import annotations

__all__ = [
    'bear_config', 'BearTimer', 'ReprMixin', 'start', 'deprecate',
    'load_ads4', 'warn_empty_ads',
]

import json
import logging
import sys
import warnings
from decimal import Decimal
from functools import wraps
from itertools import groupby
from pathlib import Path
from time import time_ns
from typing import NoReturn

from . import gvs
from .constants import LOG_CONF_BEAR
from .converters import represent
from .structures import DivisionCode

bear_logger = logging.getLogger('zeraora.bear')

bear_config = LOG_CONF_BEAR


class BearTimer(object):

    def __init__(self, label: str = None, *_, **__):
        """
        熊牌计时器。对代码运行进行计时，并向名为 "zeraora.bear" 的Logger发送DEBUG等级的日志。

        ----

        使用前，需要先启用日志输出：

        >>> import logging.config
        >>> from zeraora.constants import LOG_CONF_BEAR
        >>> from zeraora.utils import BearTimer
        >>>
        >>> logging.config.dictConfig(LOG_CONF_BEAR)
        >>> bear = BearTimer()

        对于使用 Django 的项目可以改为在 settings.py 中进行如下设置：

        >>> LOGGING = {
        >>>     'version': 1,
        >>>     'formatters': {...},
        >>>     'filters': {...},
        >>>     'handlers': {
        >>>         'Console': {
        >>>             'level': 'DEBUG',
        >>>             'class': 'logging.StreamHandler',
        >>>         },
        >>>         # ...
        >>>     },
        >>>     'loggers': {
        >>>         'zeraora.bear': {
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

        :param label: 计时器的标题，用以标明输出信息归属于哪个计时器。默认从打印消息时的上下文中获取。
        """
        context = sys._getframe().f_back.f_code.co_name
        self._start: int = 0  # 计时开始时间
        self._point: int = 0  # 中途标记时间（用于计算距离上次标记过去了多久）
        self._label = context if not label and hasattr(sys, '_getframe') else str(label)

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

    def _record(self, msg: str = '') -> int:
        """
        打印一行消息，标明此刻的时间、经历的时长、距上次打印的时长、计时器标题，以及附加的消息。

        :param msg: 要附加的消息。默认为空文本。
        :return: 自纪元以来的当前时间（以纳秒为单位）。
        """
        now = time_ns()
        total = Decimal((now - self._start) if self._start else 0) / 1000000000
        delta = Decimal((now - self._point) if self._point else 0) / 1000000000
        bear_logger.debug(f'[{self._label}] [{total:.9f} +{delta:.9f}]: {msg}')
        self._point = now
        return now

    def start(self, msg='Starting...'):
        """
        开始计时。

        如果计时尚未结束，会重新开始计时，中途记录的标记也会被清除。

        :param msg: 要附加的消息。
        :return: 计时器对象自身。
        """
        self._point = 0
        self._start = time_ns()
        self._record(msg)
        return self

    def step(self, msg='') -> tuple[int, int]:
        """
        中途标记。

        用此方法可以计算出距离上一次标记/开始计时过去了多久。

        如果计时器尚未开始计时，那么过去的时间始终是 0 秒。

        :param msg: 要附加的消息。
        :return: 二元元组。包含上一次标记/开始计时的时刻，和此时的时刻。时刻是自纪元以来的当前时间（以纳秒为单位）。
        """
        prev = self._point
        curr = self._record(msg)
        return prev, curr

    def stop(self, msg='Stopped.') -> int:
        """
        结束计时。

        :param msg: 要附加的消息。
        :return: 返回自纪元以来的当前时间（以纳秒为单位）。
        """
        curr = self._record(msg)
        self._start = 0
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
            for attr, name in attrs.items():
                if attr.startswith('_'):
                    continue
                mapper = annots.get(attr, represent)
                value = getattr(self, attr)
                value = mapper(value) if callable(mapper) else value
                yield f'{name}={value}'

        attrs = self.AttributeMeta.__dict__
        annots = attrs.get('__annotations__', {})
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
            for attr, option in attrs.items():
                if attr.startswith('_'):
                    continue
                mapper = annots.get(attr, None)
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

        attrs = self.TagMeta.__dict__
        annots = attrs.get('__annotations__', {})
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


def start(*version, note: str = None):
    """
    检查 Python 版本是否高于或等于指定值，
    如果低于指定的版本就会抛出 RuntimeError。

    若提供了 ``note`` 参数，则会在末尾输出。
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if sys.version_info < version:
                v = '.'.join(map(str, version))
                raise RuntimeError(
                    # 英文在前保证控制台出现乱码时不会掩盖该错误信息
                    f'Require Python version {v} or above to run. '
                    f'Python运行版本需要在 {v} 或以上。'
                    + ('' if note is None else note)
                )
            return func(*args, **kwargs)

        return wrapper

    return decorator


def deprecate(*since,
              ref=sys.version_info,
              reason: str = 'This function is deprecated since %(since)s .',
              suggestion: str = 'This function will be deprecate at %(since)s .',
              migration: str = None,
              ):
    """
    为一个函数作废弃标记。

    :param since: 自哪个版本开始废弃。
    :param ref: 参照版本。用于确定状态是准备废弃还是已经废弃。
    :param reason: 已废弃的原因。（废弃后的提示）
    :param suggestion: 准备废弃时提供的建议。（废弃前的提示）
    :param migration: 假设废弃之后应该采取的迁移措施或用法变更说明。
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            tips = (suggestion if ref < since else reason) % dict(since='.'.join(map(str, since)))
            tips += ('\n' + migration) if migration else ''
            if ref < since:
                warnings.warn(tips, category=PendingDeprecationWarning, stacklevel=2)
            else:
                warnings.warn(tips, category=DeprecationWarning, stacklevel=2)
            return func(*args, **kwargs)

        return wrapper

    return decorator


def warn_empty_ads():
    """
    在未载入行政区划映射表时发出警告。（您不应该使用此方法，它只在包内使用）
    """
    if not gvs.ad_map or not gvs.ad_tree:
        warnings.warn('未载入行政区划映射表，该方法可能会失效或返回非期望值。', category=UserWarning)


def load_ads4(fp: str | Path, encoding='UTF-8', **kwargs) -> NoReturn:
    """
    读取并过滤前四级行政区划，然后赋值给全局变量 ``zeraora.gvs.ad_map`` 和 ``zeraora.gvs.ad_tree`` 。

    测试数据可以在 `GitHub <https://github.com/aixcyi/zeraora/tree/main/dataset>`_
    或 `码云 <https://github.com/aixcyi/zeraora/tree/main/dataset>`_ 中找到。

    ----

    警告：这会耗费一定的时间并且占用一些内存，同时造成线程阻塞，请在合适的时候再执行调用。

    :param fp: 数据文件地址。
    :param encoding: 文件编码。
    :param kwargs: 其它提供给 ``open()`` 的参数。
    :return: 无
    """
    with open(fp, 'r', encoding=encoding, **kwargs) as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError('提供的数据不是一对一映射。')  # pragma: no cover

    steam = data.items()
    steam = ((c, n) for c, n in steam if isinstance(c, str) and isinstance(n, str))
    steam = ((DivisionCode.fromcode(c), n) for c, n in steam)
    steam = ((c, n) for c, n in steam if c.village == '000')  # 只要前四个级别
    steam = ((c, n) for c, n in steam if (c.county != '00' and c.township == '000') or c.county == '00')

    gvs.ad_map = dict(steam)
    gvs.ad_tree = fork(gvs.ad_map, depth=0, floor=4)


def fork(__steam, depth: int, floor: int):
    if depth >= floor:
        return next(__steam)[-1]
    return {
        k: fork(v, depth + 1, floor)
        for k, v in groupby(__steam, lambda item: item[depth])
    }
