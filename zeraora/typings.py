"""
类型相关。
"""

import datetime
import re
import typing as t
from uuid import UUID

Throwable = t.Union[BaseException, t.Type[BaseException]]


class _UNSET:
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


def safecast(mapper: t.Callable, raw, *errs: Throwable, default=None) -> t.Any:
    """
    转换一个值，转换失败时返回default，确保不会发生指定异常。

    默认捕获以下异常，可以通过errs参数追加更多异常：
        - TypeError
        - ValueError
        - KeyboardInterrupt

    :param mapper: 用来转换raw的转换器。如果转换器不可调用，将直接返回默认值。
    :param raw: 被转换的值。
    :param errs: 需要捕获的其它异常类或异常对象。应当提供可被 except 语句接受的值。
    :param default: 默认值。即使不提供也会默认返回 None 而不会抛出异常。
    :return: 转换后的值。如若捕获到特定异常将返回默认值。
    """
    exceptions = tuple(
        exc for exc in errs
        if exc.__class__ is type
        and issubclass(exc, BaseException)
        or isinstance(exc, BaseException)
    )
    if not callable(mapper):
        return default  # pragma: no cover
    try:
        return mapper(raw)
    except (TypeError, ValueError, KeyboardInterrupt) + exceptions:
        return default


class SafeCaster:

    def __init__(self, *exceptions: Throwable):
        """
        创建一个安全转换器。

        :param exceptions: 可能发生的异常。应当提供可被 except 语句接受的值。
        """
        self._exceptions = tuple(
            exc for exc in exceptions
            if exc.__class__ is type
            and issubclass(exc, BaseException)
            or isinstance(exc, BaseException)
        )

    def __call__(self, raw: t.Any = _UNSET, *mappers: t.Callable, default=None):
        """
        转换一个值，转换失败时返回默认值，确保不会发生预先定义好的异常。

        :param raw: 被转换的值。
        :param mappers: 用来转换raw的转换器。如果某个转换器不可调用，将不会执行这个转换。
        :param default: 默认值。
        :return: 转换后的结果，或默认值。
        """
        if len(mappers) <= 0:
            return default

        if raw is _UNSET:
            result = mappers[0]()
            converters = mappers[1:]
        else:
            result = raw
            converters = mappers

        try:
            for converter in converters:
                result = converter(result) if callable(converter) else result
            return result
        except self._exceptions:
            return default


safecasts = SafeCaster(TypeError, ValueError, KeyboardInterrupt)


def represent(value) -> str:
    """
    将任意值转换为一个易于阅读的字符串。

    也是 ReprMixin 的默认格式化函数。

    默认使用 repr() 函数进行转换。如果自定义的类需要实现被此函数转换，请重写 .__repr__() 方法。

    :param value: 任意值。
    :return: 字符串。
    """
    if isinstance(value, str):
        return f'"{value}"'
    elif isinstance(value, datetime.timedelta):
        return f'[{value.days}d+{value.seconds}.{value.microseconds:06d}s]'
    elif isinstance(value, datetime.datetime):
        return f'[{value:%Y-%m-%d %H:%M:%S,%f}]'
    elif isinstance(value, datetime.date):
        return f'[{value:%Y-%m-%d}]'
    elif isinstance(value, UUID):
        return value.hex
    else:
        return repr(value)


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


def datasize(literal: str) -> t.Union[int, float]:
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
        raise TypeError(
            '不支持解析一个非字符串类型的值。'  # pragma: no cover
        )

    pattern = re.compile(r'^([0-9]+)\s*([KMGTPEZY]?)(i?[Bb])$')
    result = re.fullmatch(pattern, literal)

    if result is None:
        return 0

    base = int(result.group(1))
    shift = 'BKMGTPEZY'.index(result.group(2))
    power = (1024 if 'i' in result.group(3) else 1000) ** shift
    power = (power / 8) if 'b' in result.group(3) else power

    return base * power


def true(value) -> bool:
    """
    将HTTP请求中 query 部分的参数值转换为 Python 的逻辑值。

    :param value: query 中的参数值。
    :return: True 或 False。
    """
    return value in ('true', 'True', 'TRUE', 1, True)
