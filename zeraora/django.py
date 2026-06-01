__all__ = [
    'SnakeModel',
    'PrefilterManager',
    'ReprMixin',
]

import re
from datetime import timedelta, datetime, date
from uuid import UUID

from django.apps import apps
from django.db import models


def _camel_to_snake(name: str) -> str:
    """
    将类似 ``CombineOrderSKUModel`` 大小写形式的字符串
    转换为 ``combine_order_sku_model`` 。
    """
    # "CombineOrderSKUModel"
    # -> "Combine OrderSKU Model"
    # -> "Combine Order SKU Model"
    # -> "combine_order_sku_model"
    mid = re.sub('(.)([A-Z][a-z]+)', r'\1 \2', name)
    words = re.sub('([a-z0-9])([A-Z])', r'\1 \2', mid)
    return '_'.join(word.lower() for word in words.split())


class SnakeModel(models.base.ModelBase):
    """
    为模型生成一个下划线分隔的小写的数据表名（即蛇形命名法）。

    - 通过 ``Meta`` 手动指定的表名不会被覆盖。
    - 只会给非抽象模型（``Meta.abstract == False``）生成表名。

    ----

    用法如下： ::

        # ./apps/mall/models.py

        from django.db import models
        from zeraora.django import SnakeModel

        class GoodsSKUInfo(models.Model, metaclass=SnakeModel):
            name = models.CharField(max_length=64)
            price = models.IntegerField()
            stock = models.IntegerField()

            class Meta:
                abstract = False
                # db_table = ""

    以上模型没有设置 ``Meta.db_table``，
    那么 Django 默认生成的是 ``mall_goodsskuinfo``，
    而使用 SnakeModel 之后会默认生成 ``mall_goods_sku_info`` 。
    """

    def __new__(cls, name, bases, attrs, **kwargs):
        module = attrs.get('__module__', None)
        app_config = apps.get_containing_app_config(module)
        if app_config is None:
            return super().__new__(cls, name, bases, attrs, **kwargs)

        app_name = app_config.label
        model_name = _camel_to_snake(name)
        table_name = f'{app_name}_{model_name}'

        if 'Meta' not in attrs:
            attrs['Meta'] = type('Meta', (), dict(db_table=table_name))

        abstract = getattr(attrs["Meta"], 'abstract', False)
        if not hasattr(attrs["Meta"], 'db_table') and not abstract:
            setattr(attrs['Meta'], 'db_table', table_name)

        return super().__new__(cls, name, bases, attrs, **kwargs)


class PrefilterManager(models.Manager):
    """
    预设过滤条件的数据管理器。
    """

    def __init__(self, *args, **kwargs):
        super().__init__()
        self._args_ = args
        self._kwargs_ = kwargs

    def get_queryset(self):
        return super().get_queryset().filter(*self._args_, **self._kwargs_)


def represent(value) -> str:
    """
    将任意值转换为一个易于阅读的字符串。

    也是 ReprMixin 的默认格式化函数。

    默认使用 repr() 函数进行转换。如果自定义的类需要实现被此函数转换，请重写 .__repr__() 方法。

    :param value: 任意值。
    :return: 字符串。
    """
    match value:
        case str():
            return f'"{value}"'
        case timedelta():
            return f'[{value.days}d,{value.seconds}s,{value.microseconds}μs]'
        case datetime():
            return f'[{value:%Y-%m-%d %H:%M:%S,%f}]'
        case date():
            return f'[{value:%Y-%m-%d}]'
        case UUID():
            return value.hex
        case _:
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
