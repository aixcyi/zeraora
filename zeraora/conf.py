__all__ = [
    'logc',
    'WrappedListProperty',
    'Configuration',
]

from abc import ABC, abstractmethod
from itertools import chain
from typing import Any, Callable

from typing_extensions import Self

from zeraora.string import StringBuilder


def logc(*pairs: tuple[str, Any] | list[str, Any], **kwargs: Any) -> dict[str, Any]:
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


class WrappedListProperty:

    def __init__(self, primitive: type, wrapper: type):
        """
        包装列表属性。

        :param primitive: 基本类型。实际存储和批量提取的类型。
        :param wrapper: 包装类型。访问单个属性得到的类型。
        """
        self.serialize = primitive
        self.deserialize = wrapper

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        return list(map(self.deserialize, instance.__dict__[self.name]))

    def __set__(self, instance, value):
        instance.__dict__[self.name] = list(map(self.serialize, value))


class Configuration(ABC):
    """
    配置映射编辑器。
    """
    VERSION = 1

    def __init__(self, configs: dict):
        self._version_ = self.VERSION
        self._loaded_ = dict()
        self.load(configs)

    def load(self, configs: dict) -> Self:
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

    def dump(self) -> dict:
        """
        导出配置。
        """
        return {
            '$version': self.VERSION,
        } | {
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

    def show(self, printer: Callable[[str], Any] = print) -> Self:
        """
        打印配置信息。

        键为字段名，值为字段值；前缀 * 表示字段值已被修改，无前缀则表示未被修改。

        :param printer: 一个用于打印的函数或方法。其第一个参数必须字符串，其余参数必须允许省略。
        :return: 自身。
        """
        fields = self.diff()
        printer(
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
        return self
