__all__ = [
    'logc',
    'WrappedListProperty',
    'WrappedSetProperty',
    'Configuration',
]

import json
from abc import ABC, abstractmethod
from itertools import chain
from typing import Any, Callable, Generic, Iterable, TypeVar

from typing_extensions import Self, deprecated

from zeraora.string import StringBuilder

M = TypeVar('M')


@deprecated('未来可能会调整替换规则。', category=FutureWarning)
def logc(*pairs: tuple[str, Any], **kwargs: Any) -> dict[str, Any]:
    """
    专为 `配置字典架构 <https://docs.python.org/zh-cn/3/library/logging.config.html#configuration-dictionary-schema>`_
    编写的 :class:`dict` 变种函数。

    - 接受逐个键值对入参。
    - 去除“键”尾随的所有 ``_`` 字符。
    - 键等于 ``"_"`` 时替换为 ``"."``。
    - 键等于 ``"__"`` 时替换为 ``"()"``。
    - 键等于 ``"klass"`` 时替换为 ``"class"``。

    >>> logc(
    >>>     __='my.package.customFormatterFactory',
    >>>     klass='logging.StreamHandler',
    >>>     level='DEBUG',
    >>>     filters=[],
    >>>     formatter='bear',
    >>>     _={
    >>>         'foo': 'baz'
    >>>     },
    >>> )
    {
        '()': 'my.package.customFormatterFactory',
        'class': 'logging.StreamHandler',
        'level': 'DEBUG',
        'filters': [],
        'formatter': 'bear',
        '.': {
            'foo': 'baz'
        },
    }
    """

    def constructor():
        for key, val in chain(pairs, kwargs.items()):
            match key:
                case 'klass':
                    yield 'class', val
                case '__':
                    yield '()', val
                case '_':
                    yield '.', val
                case _:
                    yield key.rstrip('_'), val

    return dict(constructor())


class WrappedListProperty(Generic[M]):

    def __init__(self, primitive: type, wrapper: type[M]):
        """
        包装列表属性。

        在内部维护一个成员都是基本类型的列表（用于导出JSON），单独访问属性时会得到一个成员都是包装类型的列表。

        :param primitive: 基本类型。实际存储和批量提取的类型。
        :param wrapper: 包装类型。访问单个属性得到的类型。
        """
        self.serialize = primitive
        self.deserialize = wrapper

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner) -> list[M]:
        return list(map(self.deserialize, instance.__dict__[self.name]))

    def __set__(self, instance, value: Iterable[M]):
        instance.__dict__[self.name] = list(map(self.serialize, value))


class WrappedSetProperty(Generic[M]):

    def __init__(self, primitive: type, wrapper: M):
        """
        包装集合属性。

        在内部维护一个成员都是基本类型的列表（用于导出JSON），单独访问属性时会得到一个成员都是包装类型的集合。

        :param primitive: 基本类型。实际存储和批量提取的类型。
        :param wrapper: 包装类型。访问单个属性得到的类型。
        """
        self.serialize = primitive
        self.deserialize = wrapper

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner) -> set[M]:
        return set(map(self.deserialize, instance.__dict__[self.name]))

    def __set__(self, instance, value: Iterable[M]):
        instance.__dict__[self.name] = list(map(self.serialize, value))


class Configuration(ABC):
    """
    配置映射编辑器。
    """
    VERSION = 1

    def __init__(self, configs: dict, /):
        self._version_ = self.VERSION
        self._loaded_ = dict()
        self.load(configs)

    def __str__(self):
        fields = self.diff()
        return (
            StringBuilder()
            .writeline('=' * 32)
            .writeline(self.__class__.__name__)
            .writeline('-' * 32)
            .writes(
                f'* {k} = {v!r}\n' if k in fields else
                f'  {k} = {v!r}\n' for k, v in self.dump().items()
            )
            .writeline('=' * 32)
            .build()
        )

    def load(self, configs: dict, /) -> Self:
        """
        载入并覆盖当前配置。
        """
        self._version_ = configs.get('$version', self.VERSION)
        self._loaded_ = configs
        self.__dict__.update(
            (k, v)
            for k, v in configs.items()
            if type(k) is str and k.isidentifier() and not k.startswith('_')
        )
        return self

    def dump(self, *, pure=False) -> dict:
        """
        导出配置。

        :param pure: 是否仅导出普通配置，不额外添加 ``$version`` 字段。
        :return: 以字典类型存放的数据。
        """
        return ({} if pure else {
            '$version': self.VERSION,
        }) | {
            k: self.__dict__[k]
            for k in sorted(self.__dict__.keys())
            if not k.startswith('_')
        }

    def diff(self) -> set[str]:
        """
        对比当前配置与载入的配置，返回修改过的属性名称。
        """
        loaded = self._loaded_
        edited = self.dump()
        return set(loaded.keys()) ^ set(edited.keys()) | {
            k
            for k in set(loaded.keys()) & set(edited.keys())
            if loaded[k] != edited[k]
        }

    @abstractmethod
    def fill(self, save=True, *args, **kwargs) -> Self:
        """
        将配置导出填充到某处。

        :param save: 填充后是否执行保存。
        :return: 自身。
        """
        raise NotImplementedError

    def json(
            self, *, pure=False, skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True,
            cls: type[json.JSONEncoder] | None = None, indent: int | str | None = None,
            separators: tuple[str, str] | None = None, default: Callable | None = None, sort_keys=False, **kw
    ) -> str:
        """
        导出配置为 JSON 字符串。

        :param pure: 是否仅导出普通配置，不额外添加 ``$version`` 字段。
        :param skipkeys: 见 ``json.dumps()``。
        :param ensure_ascii: 见 ``json.dumps()``。
        :param check_circular: 见 ``json.dumps()``。
        :param allow_nan: 见 ``json.dumps()``。
        :param cls: 见 ``json.dumps()``。
        :param indent: 见 ``json.dumps()``。
        :param separators: 见 ``json.dumps()``。
        :param default: 见 ``json.dumps()``。
        :param sort_keys: 见 ``json.dumps()``。
        :param kw: 见 ``json.dumps()``。
        :return: 一个 JSON 字符串。
        """
        return json.dumps(
            self.dump(pure=pure),
            skipkeys=skipkeys,
            ensure_ascii=ensure_ascii,
            check_circular=check_circular,
            allow_nan=allow_nan,
            cls=cls,
            indent=indent,
            separators=separators,
            default=default,
            sort_keys=sort_keys,
            **kw,
        )
