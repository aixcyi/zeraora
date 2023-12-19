"""
不易归档的工具函数、工具类、类型、结构、枚举、常量等。
"""
from __future__ import annotations

__all__ = [
    'randbytes',
    'randb62',
    'randb64',
    'Gender',
    'Degree',
    'dict_',
    'true',
    'represent',
    'ReprMixin',
    'datasize',
    'dsz',
    'start',
    'deprecate',
]

import os
import re
import sys
import warnings
from datetime import date, datetime, timedelta
from enum import Enum
from functools import wraps
from random import getrandbits
from typing import Any
from uuid import UUID

from zeraora.code import Notations
from zeraora.enums import Items


def randbytes(n: int) -> bytes:
    """
    生成 n 个随机字节。

    此函数用于在 Python 3.9 以前代替 random.randbytes(n) 方法。
    """
    assert n >= 0
    return getrandbits(n * 8).to_bytes(n, 'little')


def randb62(n: int) -> str:
    """
    生成 n 个 base62 随机字符。

    返回结果不受 random 库的 seed() 影响。
    """
    return ''.join(Notations.BASE62[i % 62] for i in os.urandom(n))


def randb64(n: int) -> str:
    """
    生成 n 个 base64 随机字符。

    返回结果不受 random 库的 seed() 影响。
    """
    return ''.join(Notations.BASE64[i >> 2] for i in os.urandom(n))


class Gender(Enum):
    Male = True
    Female = False


class Degree(int, Items):
    """
    描述程度的七个档位。
    """
    HIGHEST = 100, '最高'
    HIGHER = 75, '偏高'
    HIGH = 50, '高'
    NORMAL = 0, '正常'
    LOW = -50, '低'
    LOWER = -75, '偏低'
    LOWEST = -100, '最低'

    __properties__ = 'label',

    @property
    def label(self):
        return self._label_


def dict_(**kwargs: Any) -> dict:
    """
    去除dict参数名尾随的 "_" 。

    比如

    >>> dict_(
    >>>     level='DEBUG',
    >>>     class_='logging.StreamHandler',
    >>>     filters=[],
    >>>     formatter='bear',
    >>> )

    将会返回

    >>> {
    >>>     "level": "DEBUG",
    >>>     "class": "logging.StreamHandler",
    >>>     "filters": [],
    >>>     "formatter": "bear",
    >>> }

    :param kwargs: 仅限关键字传参。
    :return: 一个字典。
    """
    return dict(
        (k.rstrip('_'), v) for k, v in kwargs.items()
    )


def true(value) -> bool:
    """
    将HTTP请求中 query 部分的参数值转换为 Python 的逻辑值。

    :param value: query 中的参数值。
    :return: True 或 False。
    """
    return value in ('true', 'True', 'TRUE', 1, True, '1')


def represent(value: Any) -> str:
    """
    将任意值转换为一个易于阅读的字符串。

    也是 ReprMixin 的默认格式化函数。

    默认使用 repr() 函数进行转换。如果自定义的类需要实现被此函数转换，请重写 .__repr__() 方法。

    :param value: 任意值。
    :return: 字符串。
    """
    if hasattr(value, 'label'):  # 兼容像 Django 的 Choices 那样的枚举
        return value.label
    elif isinstance(value, str):
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


def datasize(literal: str) -> int | float:
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
        raise TypeError('不支持解析一个非字符串类型的值。')

    pattern = re.compile(r'^([0-9]+)\s*([KMGTPEZY]?)(i?[Bb])$')
    result = re.fullmatch(pattern, literal)

    if result is None:
        return 0

    base = int(result.group(1))
    shift = 'BKMGTPEZY'.index(result.group(2))
    power = (1024 if 'i' in result.group(3) else 1000) ** shift
    power = (power / 8) if 'b' in result.group(3) else power

    return base * power


dsz = datasize


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
