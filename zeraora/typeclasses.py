"""
数据类型类、枚举类、空类、类型别名等。
"""
import enum
from types import DynamicClassAttribute
from typing import Type, Union, Tuple, Dict, List

Throwable = Union[BaseException, Type[BaseException]]


class UNSET:
    pass


class OnionObject(object):

    def __translate_list(self, items: list) -> list:
        return list(
            self.__translate_list(list(item)) if isinstance(item, tuple)
            else self.__translate_list(item) if isinstance(item, list)
            else type(self)(item, self.__depth - 1) if isinstance(item, dict)
            else item
            for item in items
        )

    # OnionObject()
    def __new__(cls, dictionary: dict = None, depth: int = -1, **kvs):
        """
        将字典转化为对象，使得可以用点分法代替下标访问内容。

        支持还原为字典：

        >>> data: dict = ~OnionObject()

        支持直接更新字典：

        >>> obj: OnionObject = OnionObject()
        >>> obj: OnionObject = obj | dict()  # 等价于 obj |= dict()

        :param dictionary: 包含数据的字典。不符合标识符命名要求，
                           或者以双下划线 “__” 开头的键不会被收录。
        :param depth: 递归转化的层数。负数表示无限递归转化，正数表示递归层数，0无意义。
        :return: OnionObject 的对象。
        :raise TypeError: 属性名称必须是字符串。
        """
        if dictionary is None:
            dictionary = {}
        if not isinstance(dictionary, dict):
            raise TypeError  # pragma: no cover
        if depth == 0:
            return dictionary
        dictionary.update(kvs)

        self = object.__new__(cls)
        self.__depth = depth
        self.__ior__(dictionary)
        return self

    # OnionObject() | dict()
    def __or__(self, dictionary: dict) -> 'OnionObject':
        for k, v in dictionary.items():
            k = str(k)
            if not k.isidentifier() or k.startswith('__'):
                continue
            if isinstance(v, tuple):
                self.__setattr__(k, self.__translate_list(list(v[:])))
            elif isinstance(v, list):
                self.__setattr__(k, self.__translate_list(v[:]))
            elif isinstance(v, dict) and self.__depth:
                self.__setattr__(k, self.__class__(v, self.__depth - 1))
            else:
                self.__setattr__(k, v)
        return self

    # obj = OnionObject()
    # obj |= dict()
    __ior__ = __or__

    # ~OnionObject()
    def __invert__(self) -> dict:
        def obtain():
            prefix = f'_{type(self).__name__}__'
            for k, v in self.__dict__.items():
                if k.startswith('__') or k.startswith(prefix):
                    continue
                if isinstance(v, (list, tuple)):
                    yield k, [
                        ~i if isinstance(i, OnionObject) else i
                        for i in v
                    ]
                elif isinstance(v, OnionObject):
                    yield k, ~v
                else:
                    yield k, v

        return dict(obtain())

    # repr(OnionObject())
    def __repr__(self) -> str:
        prefix = f'_{type(self).__name__}__'
        attrs = ', '.join(
            f'{attr}={type(value).__name__}(...)'
            if isinstance(value, OnionObject) else
            f'{attr}={value!r}'
            for attr, value in self.__dict__.items()
            if not attr.startswith('__') or attr.startswith(prefix)
        )
        return f'OnionObject({attrs})'


# Little Endian
class RadixInteger(Tuple[int, ...]):

    def __new__(cls,
                x: Union[int, Tuple[int, ...], List[int], bytes, bytearray],
                n: int,
                be=False,
                negative=False) -> 'RadixInteger':
        """
        一个以元组表述各个数位的 N 进制整数。

        :param x: 一个int类型的整数，一个包含非负整数的元组，或者一个字节串。
        :param n: 进位制（的基数）。必须是一个大于等于 2 的正整数。
        :param be: 表示给定元组是否使用大端字节序。
        :param negative: 表示给定元组是否应当表示一个负数，或给定字节串是否使用二进制补码表示整数。
        """

        def dec2seq(i: int):
            while i >= n:
                yield i % n
                i //= n
            yield i

        if n < 2:
            raise ValueError('无法表述基数比 2 更低的进位制。')

        if isinstance(x, int):
            self = tuple.__new__(cls, dec2seq(abs(x)))
            self._radix = n
            self._integer = x

        elif isinstance(x, cls):
            self = tuple.__new__(cls, dec2seq(abs(x.numeric)))
            self._radix = n
            self._integer = x.numeric

        elif isinstance(x, (bytes, bytearray)):
            self = tuple.__new__(cls, x[::-1] if be else x)
            self._radix = 256
            self._integer = (
                int.from_bytes(x, 'big', signed=negative)
                if be else
                int.from_bytes(x, 'little', signed=negative)
            )

        elif isinstance(x, (tuple, list)):
            if min(x) < 0:
                raise ValueError('x 只能包含非负整数。')
            radix = max(x)
            if not radix <= n:
                raise ValueError(
                    f'x 的进位制最低是 {radix}，高于给定的 {n} 。'
                )
            pairs = zip(x, reversed(range(len(x))))
            self = tuple.__new__(cls, x[::-1] if be else x)
            self._radix = n
            self._integer = sum(map(lambda pair: pair[0] * n ** pair[1], pairs))
            self._integer = -self._integer if negative else self._integer

        else:
            raise TypeError(
                f'{cls.__name__}() 不接受 {type(x).__name__} 类型的参数。'
            )

        return self

    @property
    def radix(self):
        """整数的进位制。"""
        return self._radix

    @property
    def numeric(self):
        """对应的以阿拉伯数字表述的十进制整数。"""
        return self._integer

    def map2str(self, mapping: Union[str, Dict[int, str]], be=True) -> str:
        """
        按照规则将每一位数映射到一个字符串中。
        """
        return ''.join(map(lambda i: mapping[i], self[::-1] if be else self))

    def map2bytes(self, mapping: Union[bytes, Dict[int, bytes]], be=True) -> bytes:
        """
        按照规则将每一位数映射到一个字节串中。
        """
        return bytes(map(lambda i: mapping[i], self[::-1] if be else self))


# copy from https://github.com/django/django/blob/stable/4.2.x/django/db/models/enums.py
class ChoicesMeta(enum.EnumMeta):
    """用于创建带有标签文本的枚举的类（元类）。"""

    def __new__(metacls, classname, bases, classdict, **kwds):
        labels = []
        for key in classdict._member_names:
            value = classdict[key]
            if (
                    isinstance(value, (list, tuple))
                    and len(value) > 1
                    and isinstance(value[-1], (str,))
            ):
                *value, label = value
                value = tuple(value)
            else:
                label = key.replace("_", " ").title()
            labels.append(label)
            # Use dict.__setitem__() to suppress defenses against double
            # assignment in enum's classdict.
            dict.__setitem__(classdict, key, value)
        cls = super().__new__(metacls, classname, bases, classdict, **kwds)
        for member, label in zip(cls.__members__.values(), labels):
            member._label_ = label
        return enum.unique(cls)

    def __contains__(cls, member):
        if not isinstance(member, enum.Enum):
            # Allow non-enums to match against member values.
            return any(x.value == member for x in cls)
        return super().__contains__(member)

    @property
    def names(cls):
        empty = ["__empty__"] if hasattr(cls, "__empty__") else []
        return empty + [member.name for member in cls]

    @property
    def choices(cls):
        empty = [(None, cls.__empty__)] if hasattr(cls, "__empty__") else []
        return empty + [(member.value, member.label) for member in cls]

    @property
    def labels(cls):
        return [label for _, label in cls.choices]

    @property
    def values(cls):
        return [value for value, _ in cls.choices]


# copy from https://github.com/django/django/blob/stable/4.2.x/django/db/models/enums.py
class Choices(enum.Enum, metaclass=ChoicesMeta):
    """用于创建带有标签文本的枚举。"""

    @DynamicClassAttribute
    def label(self):
        return self._label_

    @property
    def do_not_call_in_templates(self):
        return True

    def __str__(self):
        """
        Use value when cast to str, so that Choices set as model instance
        attributes are rendered as expected in templates and similar contexts.
        """
        return str(self.value)

    # A similar format was proposed for Python 3.10.
    def __repr__(self):
        return f"{self.__class__.__qualname__}.{self._name_}"


# copy from https://github.com/django/django/blob/stable/4.2.x/django/db/models/enums.py
class IntegerChoices(int, Choices):
    """用于创建值是整数的带有标签文本的枚举。"""

    pass


# copy from https://github.com/django/django/blob/stable/4.2.x/django/db/models/enums.py
class TextChoices(str, Choices):
    """用于创建值是字符串的带有标签文本的枚举。"""

    def _generate_next_value_(name, start, count, last_values):
        return name


class ItemsMeta(enum.EnumMeta):
    """用于创建带有任意属性的枚举的类（元类）。"""

    def __new__(metacls, classname, bases, classdict, **kwds):
        # 获取属性名（pks）
        if '__properties__' not in classdict:
            raise AttributeError(
                f'{classname} 使用了 {metacls.__name__}，'
                f'因此必须定义一个名为 __properties__ 的属性。'
            )
        pks = classdict['__properties__']
        if not isinstance(pks, (tuple, list)):
            raise TypeError(
                f'{classname}.__properties__ 的值只允许是 tuple 或 list 。'
            )
        if not all(isinstance(pk, str) and not pk.startswith('_') for pk in pks):
            raise TypeError(
                f'{classname}.__properties__ 的值必须是字符串且不以下划线 “_” 开头。'
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
            raise TypeError
        if name[:-1] in cls.__properties__ and name.endswith('s'):
            return [getattr(member, name[:-1]) for member in cls]
        if name[:-2] in cls.__properties__ and name.endswith('es'):
            return [getattr(member, name[:-2]) for member in cls]
        return object.__getattribute__(cls, name)

    @property
    def names(cls):
        empty = ["__empty__"] if hasattr(cls, "__empty__") else []
        return empty + [member.name for member in cls]

    @property
    def values(cls):
        empty = [None] if hasattr(cls, "__empty__") else []
        return empty + [member.value for member in cls]

    @property
    def choices(cls):
        if 'label' not in cls.__properties__:
            raise AttributeError(
                '如需使用 .choices 属性，必须在 __properties__ 中'
                '添加一个名为 "label" 的属性，且必须保证枚举值中有相应的属性值。'
            )
        empty = [(None, cls.__empty__)] if hasattr(cls, "__empty__") else []
        return empty + [(member.value, member.label) for member in cls]


class Items(enum.Enum, metaclass=ItemsMeta):
    """
    用于创建带有任意属性的枚举。

    >>> from enum import Enum
    >>>
    >>> class YearInSchool(Items):
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
    >>> print(YearInSchool.SENIOR.name)  # 'SENIOR'
    >>> print(YearInSchool.SENIOR.value)  # 4
    >>> print(YearInSchool.SENIOR.code)  # 'SR'
    >>> print(hex(YearInSchool.SENIOR.color))  # '0xa0408e'
    >>> print(YearInSchool.SENIOR.label)  # 'Senior'
    >>>
    >>> print(YearInSchool.names)  # ['FRESHMAN', 'SOPHOMORE', ...]
    >>> print(YearInSchool.values)  # [1, 2, 3, 4, 5]
    >>> print(YearInSchool.codes)  # ['FR', 'SO', 'JR', 'SR', 'GR']
    >>> print(YearInSchool.colors)  # [14897940, 15537588, ...]
    >>> print(YearInSchool.labels)  # ['Freshman', 'Sophomore', ...]
    """
    __properties__ = ()

    def __repr__(self):
        # 枚举也算一种常量，直接按路径查找即可，故舍去附加的属性
        return f"{self.__class__.__qualname__}.{self._name_}"
