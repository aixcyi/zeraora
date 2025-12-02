"""
枚举相关工具和类型。
"""
from __future__ import annotations

__all__ = [
    'MoreChoicesMeta',
    'MoreChoices',
    'NamedEnumMeta',
    'NamedEnum',
]

import enum
from typing import Any, get_type_hints


class MoreChoicesMeta(enum.EnumMeta):
    """
    :class:`MoreChoices` 的元类。
    """

    def __new__(metacls, classname, bases, classdict, **kwds):
        # 获取属性名（pks）
        pks = classdict.get('__properties__', ())
        if isinstance(pks, str):
            pks = (pks,)
        for pk in pks:
            if not isinstance(pk, str) or pk.startswith('_'):
                raise ValueError(
                    f'{classname}.__properties__ 包含的值必须是字符串且不以下划线 “_” 开头。'
                )
            # https://docs.python.org/zh-cn/3/library/enum.html#supported-sunder-names
            if pk in ('name', 'value'):
                raise AttributeError(
                    f'不必也不能在 {classname}.__properties__ 中定义 name 和 value，'
                    f'它们是原生枚举就已经支持的属性。'
                )
            if pk in ('generate_next_value',):
                raise KeyError(
                    f'不能在 {classname}.__properties__ 中定义 {pk}，'
                    f'因为它会被转化成 _{pk}_ ，而这属于保留名称。'
                )
        pks = tuple(f'_{pk}_' for pk in pks)
        qty = len(pks) + 1  # 等号右侧所有元素的总数

        # 获取属性值（pvs）和枚举值（value）
        pvs_list = []
        for key in classdict._member_names:
            value = classdict[key]
            pvs = ()
            if isinstance(value, tuple) and len(value) == qty:
                value, *pvs = value
                pvs = tuple(pvs)
            pvs_list.append(pvs)
            dict.__setitem__(classdict, key, value)

        # 为每个枚举添加私有属性
        cls = super().__new__(metacls, classname, bases, classdict, **kwds)
        for member, pvs in zip(cls.__members__.values(), pvs_list):
            member.__dict__.update(zip(pks, pvs))

        return enum.unique(cls)

    def __contains__(cls, member):
        if not isinstance(member, enum.Enum):
            # Allow non-enums to match against member values.
            return any(x.value == member for x in cls)
        return super().__contains__(member)

    def __getattr__(cls, name):
        if not isinstance(name, str):
            raise TypeError  # pragma: no cover
        if name[:-1] in cls.__properties__ and name.endswith('s'):
            return [getattr(member, name[:-1]) for member in cls]
        if name[:-2] in cls.__properties__ and name.endswith('es'):
            return [getattr(member, name[:-2]) for member in cls]
        return object.__getattribute__(cls, name)

    # 对 __empty__ 属性的支持是为了与 Django 的 Choices 相兼容，可参见：
    # https://docs.djangoproject.com/zh-hans/4.2/ref/models/fields/#enumeration-types

    @property
    def names(cls) -> list[str]:
        """
        所有枚举成员的名称（定义枚举成员时的全大写变量名）。
        """
        empty = ["__empty__"] if hasattr(cls, "__empty__") else []
        return empty + [member.name for member in cls]

    @property
    def values(cls) -> list:
        """
        所有枚举成员的值（定义枚举成员时等号右边元组的第一个值）。
        """
        empty = [None] if hasattr(cls, "__empty__") else []
        return empty + [member.value for member in cls]

    @property
    def choices(cls) -> list[tuple[str, Any] | tuple[None, Any]]:
        """
        所有枚举成员的值，和所有枚举成员的属性中的标签（label）。
        """
        if 'label' not in cls.__properties__:
            raise AttributeError(
                '使用 .choices 属性前必须在 __properties__ 中'
                '添加一个名为 "label" 的属性，且必须保证枚举值中有相应的属性值。'
            )
        empty = [(None, cls.__empty__)] if hasattr(cls, "__empty__") else []
        return empty + [(member.value, member.label) for member in cls]


class MoreChoices(enum.Enum, metaclass=MoreChoicesMeta):
    """
    用于创建兼容 Django 的带有任意属性的枚举。

    >>> class SaleChannels(MoreChoices):
    >>>     CASHIER = 1, 'Y', '收银机'
    >>>     APPLET = 2, 'X', '小程序'
    >>>     KIOSK = 4, 'H', '售货机'
    >>>     APP = 8, 'A', '移动端应用'
    >>>     HANDHELD = 16, 'J', '手持机'
    >>>
    >>>     __properties__ = 'code', 'label'
    >>>
    >>>     @property
    >>>     def code(self) -> str:
    >>>         return self._code_
    >>>
    >>>     @property
    >>>     def label(self) -> str:
    >>>         return self._label_
    >>>
    >>> SaleChannels.APP.name
    APP

    >>> SaleChannels.APP.value
    8

    >>> SaleChannels.APP.code
    A

    >>> SaleChannels.APP.label
    移动端应用

    >>> SaleChannels.names
    ['CASHIER', 'APPLET', 'KIOSK', 'APP', 'HANDHELD']

    >>> SaleChannels.values
    [1, 2, 4, 8, 16]

    >>> SaleChannels.codes
    ['Y', 'X', 'H', 'A', 'J']

    >>> SaleChannels.labels
    ['收银机', '小程序', '售货机', '移动端应用', '手持机']

    >>> SaleChannels.choices
    [
        (1, '收银机'),
        (2, '小程序'),
        (4, '售货机'),
        (8, '移动端应用'),
        (16, '手持机'),
    ]
    """

    __properties__ = ()

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f"{self.__class__.__name__}.{self._name_}"


class NamedEnumMeta(enum.EnumMeta):
    """
    :class:`NamedEnum` 的元类。
    """

    names: list[str]
    """
    所有枚举成员的名称。

    如果定义了 ``__empty__`` 则会额外包含这个名称。
    """

    values: list[Any]
    """
    所有枚举成员的值。

    如果定义了 ``__empty__`` 则会额外包含一个 ``None``。
    """

    labels: list[str]
    """
    所有枚举成员的标签。

    如果定义了 ``__empty__`` 则会额外包含它的值。
    """

    choices: list[tuple[Any, str]]
    """
    所有枚举成员的值，和所有枚举成员的属性中的标签（label）。

    如果定义了 ``__empty__`` 则会额外包含一组 ``('__empty__', cls.__empty__)``。
    """

    def __new__(metacls, classname, bases, classdict, **kwds):
        cls = super().__new__(metacls, classname, bases, classdict, **kwds)

        if not classdict._member_names:
            return enum.unique(cls)
        if not len(ts := [t for t in bases if issubclass(t, tuple) and hasattr(t, '__annotations__')]):
            return enum.unique(cls)

        __annotations__ = get_type_hints(t := ts[0])
        if 'label' not in __annotations__ or __annotations__['label'] is not str:
            raise AttributeError(
                f'作为 {classname} 的枚举类型，{t.__qualname__} 必须拥有一个名为 "label" 的 str 类型的属性。'
            )
        if 'value' not in __annotations__:
            raise AttributeError(
                f'作为 {classname} 的枚举类型，{t.__qualname__} 必须拥有一个名为 "value" 的属性。'
            )

        cls._nameless_value2member_map_ = {member.value: member for member in cls}

        # 对 __empty__ 属性的支持是为了与 Django 的 Choices 相兼容，可参见：
        # https://docs.djangoproject.com/zh-hans/4.2/ref/models/fields/#enumeration-types
        if hasattr(cls, '__empty__'):
            __empty__ = getattr(cls, '__empty__')
            cls.names = ['__empty__'] + list(member.name for member in cls)
            cls.values = [None] + list(member.value for member in cls)
            cls.labels = [__empty__] + list(member.label for member in cls)
            cls.choices = [(None, __empty__)] + list((member.value, member.label) for member in cls)
        else:
            cls.names = list(member.name for member in cls)
            cls.values = list(member.value for member in cls)
            cls.labels = list(member.label for member in cls)
            cls.choices = list((member.value, member.label) for member in cls)

        for _name_ in __annotations__:
            if _name_ in {'name', 'value', 'label', 'choice'}:
                continue
            if _name_.startswith('_') or _name_.endswith('_'):
                continue
            setattr(cls, f'{_name_}s', [getattr(member, _name_) for member in cls])

        return enum.unique(cls)

    def __call__(cls, value, *args, **kwargs):
        if value in cls._nameless_value2member_map_:
            return cls._nameless_value2member_map_[value]
        return super().__call__(value, *args, **kwargs)

    def __contains__(cls, member):
        if not isinstance(member, enum.Enum):
            # Allow non-enums to match against member values.
            return any(x.value == member for x in cls)
        return super().__contains__(member)


class NamedEnum(enum.Enum, metaclass=NamedEnumMeta):
    """
    用于创建兼容 Django 的具名元组类型的枚举。

    >>> from typing import NamedTuple
    >>>
    >>> class SaleChannel(NamedTuple):
    >>>     value: int
    >>>     code: str
    >>>     label: str
    >>>
    >>> class SaleChannels(SaleChannel, NamedEnum):
    >>>     CASHIER = 1, 'Y', '收银机'
    >>>     APPLET = 2, 'X', '小程序'
    >>>     KIOSK = 4, 'H', '售货机'
    >>>     APP = 8, 'A', '移动端应用'
    >>>     HANDHELD = 16, 'J', '手持机'
    >>>
    >>> SaleChannels.APP.name
    APP

    >>> SaleChannels.APP.value
    8

    >>> SaleChannels.APP.code
    A

    >>> SaleChannels.APP.label
    移动端应用

    >>> SaleChannels.names
    ['CASHIER', 'APPLET', 'KIOSK', 'APP', 'HANDHELD']

    >>> SaleChannels.values
    [1, 2, 4, 8, 16]

    >>> SaleChannels.codes
    ['Y', 'X', 'H', 'A', 'J']

    >>> SaleChannels.labels
    ['收银机', '小程序', '售货机', '移动端应用', '手持机']

    >>> SaleChannels.choices
    [
        (1, '收银机'),
        (2, '小程序'),
        (4, '售货机'),
        (8, '移动端应用'),
        (16, '手持机'),
    ]
    """

    __empty__: str
    """
    Django `空白标签 <https://docs.djangoproject.com/zh-hans/5.2/ref/models/fields/#field-choices-blank-label>`_。
    """

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f"{self.__class__.__name__}.{self._name_}"
