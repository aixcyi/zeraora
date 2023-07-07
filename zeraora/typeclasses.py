"""
类型包。包含数据类型类、枚举类、枚举元类、类型别名等。
"""

__all__ = [
    'Throwable', 'UNSET', 'OnionObject', 'RadixInteger',
    'ItemsMeta', 'Items',
]

import enum
import typing as t

Throwable = t.Union[BaseException, t.Type[BaseException]]


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
            raise TypeError
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
class RadixInteger(t.Tuple[int, ...]):

    def __new__(cls,
                x: t.Union[int, t.Tuple[int, ...], t.List[int], bytes, bytearray],
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
            radix = max(x) + 1
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

    def map2str(self, mapping: t.Union[str, t.Dict[int, str]], be=True) -> str:
        """
        按照规则将每一位数映射到一个字符串中。
        """
        return ''.join(map(lambda i: mapping[i], self[::-1] if be else self))

    def map2bytes(self, mapping: t.Union[bytes, t.Dict[int, bytes]], be=True) -> bytes:
        """
        按照规则将每一位数映射到一个字节串中。
        """
        return bytes(map(lambda i: mapping[i], self[::-1] if be else self))


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
                f'{classname}.__properties__ 只允许是一个 tuple 或 list 。'
            )
        if not all(isinstance(pk, str) and not pk.startswith('_') for pk in pks):
            raise ValueError(
                f'{classname}.__properties__ 的值必须是字符串且不以下划线 “_” 开头。'
            )
        for pk in pks:
            # https://docs.python.org/zh-cn/3/library/enum.html#supported-sunder-names
            if pk in ('name', 'value'):
                raise KeyError(
                    f'不能也不必在 {classname}.__properties__ 中定义 name 和 value，'
                    f'它们是原生枚举就已经支持的。'
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
    def names(cls) -> t.List[str]:
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
    def items(cls) -> t.Dict[str, t.Any]:
        """
        所有枚举成员的名称和值。
        """
        its = {"__empty__": None} if hasattr(cls, "__empty__") else {}
        its.update((member.name, member.value) for member in cls)
        return its

    @property
    def choices(cls) -> t.List[t.Union[t.Tuple[str, t.Any], t.Tuple[None, t.Any]]]:
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

    def asdict(cls) -> t.Dict[enum.Enum, t.Any]:
        """
        返回枚举成员与枚举值之间的映射。
        """
        return {member: member.value for member in cls}

    def value_of(cls, value: str) -> enum.Enum:
        raise NotImplementedError(
            f'该方法是多余的，请使用 {cls.__name__}(value) 代替。'
        )  # pragma: no cover


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
    >>> print(Grade.SENIOR.name)  # 'SENIOR'
    >>> print(Grade.SENIOR.value)  # 4
    >>> print(Grade.SENIOR.code)  # 'SR'
    >>> print(hex(Grade.SENIOR.color))  # '0xa0408e'
    >>> print(Grade.SENIOR.label)  # 'Senior'
    >>>
    >>> print(Grade.names)  # ['FRESHMAN', 'SOPHOMORE', ...]
    >>> print(Grade.values)  # [1, 2, 3, 4, 5]
    >>> print(Grade.codes)  # ['FR', 'SO', 'JR', 'SR', 'GR']
    >>> print(Grade.colors)  # [14897940, 15537588, ...]
    >>> print(Grade.labels)  # ['Freshman', 'Sophomore', ...]
    """

    __properties__ = ()

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f"{self.__class__.__qualname__}.{self._name_}"
