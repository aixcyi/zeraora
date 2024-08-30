"""
枚举相关工具和类型。
"""
from __future__ import annotations

__all__ = [
    'ItemsMeta',
    'Items',
]

import enum
from typing import Any


class ItemsMeta(enum.EnumMeta):
    """
    一个元类，用于创建带有任意属性的枚举的类。
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
    def items(cls) -> dict[str, Any]:
        """
        所有枚举成员的名称和值。
        """
        its = {"__empty__": None} if hasattr(cls, "__empty__") else {}
        its.update((member.name, member.value) for member in cls)
        return its

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

    def asdict(cls) -> dict[enum.Enum, Any]:
        """
        返回枚举成员与枚举值之间的映射。
        """
        return {member: member.value for member in cls}


class Items(enum.Enum, metaclass=ItemsMeta):
    """
    用于创建带有任意属性的枚举。

    >>> from enum import Enum
    >>>
    >>> class Grade(Items):
    >>>     FRESHMAN = 1, 'FR', 0xE35314, 'Freshman'
    >>>     SOPHOMORE = 2, 'SO', 0xED15B4, 'Sophomore'
    >>>     JUNIOR = 3, 'JR', 0x9B3CED, 'Junior'
    >>>     SENIOR = 4, 'SR', 0xA0408E, 'Senior'
    >>>     GRADUATE = 5, 'GR', 0x518CCC, 'Graduate'
    >>>
    >>>     __properties__ = 'code', 'color', 'label'
    >>>
    >>>     @property
    >>>     def code(self) -> str:
    >>>         return self._code_
    >>>
    >>>     @property
    >>>     def color(self) -> int:
    >>>         return self._color_
    >>>
    >>>     @property
    >>>     def label(self) -> str:
    >>>         return self._label_
    >>>
    >>> Grade.SENIOR.name
    SENIOR

    >>> Grade.SENIOR.value
    4

    >>> Grade.SENIOR.code
    SR

    >>> hex(Grade.SENIOR.color)
    0xa0408e

    >>> Grade.SENIOR.label
    Senior

    >>> Grade.names
    ['FRESHMAN', 'SOPHOMORE', ...]

    >>> Grade.values
    [1, 2, 3, 4, 5]

    >>> Grade.codes
    ['FR', 'SO', 'JR', 'SR', 'GR']

    >>> Grade.colors
    [14897940, 15537588, ...]

    >>> Grade.labels
    ['Freshman', 'Sophomore', ...]
    """

    __properties__ = ()

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f"{self.__class__.__qualname__}.{self._name_}"
