"""
不易归档的工具函数、工具类、类型、结构、枚举、常量等。
"""
from __future__ import annotations

__all__ = [
    'Gender',
    'Degree',
    'represent',
    'ReprMixin',
]

from datetime import date, datetime, timedelta
from enum import Enum
from typing import Any
from uuid import UUID

from zeraora.enums import Items


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
