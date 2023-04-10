"""
类型相关。
"""

import datetime
from typing import Callable
from uuid import UUID


class JSONObject(object):
    def __init__(self, dictionary: dict = None, **kvs):
        """
        将嵌套字典转化为嵌套对象（递归转化）。

        :param dictionary: 包含数据的字典。请确保所有键都符合标识符命名要求，且均为字符串。
        :param kvs: 任意键值对。
        :return: JSONObject。
        :raise TypeError: 属性名称必须是字符串。
        """
        for k, v in {**(dictionary if dictionary else {}), **kvs}.items():
            k = str(k)
            if not k.isidentifier():
                continue
            if v.__class__ is list:
                self.__setattr__(k, self._translate_list(v[:]))
            elif v.__class__ is dict:
                self.__setattr__(k, self.__class__(v))
            else:
                self.__setattr__(k, v)

    def __or__(self, dictionary: dict):
        for k, v in dictionary.items():
            k = str(k)
            if not k.isidentifier():
                continue
            if v.__class__ is list:
                self.__setattr__(k, self._translate_list(v[:]))
            elif v.__class__ is dict:
                self.__setattr__(k, self.__class__(v))
            else:
                self.__setattr__(k, v)
        return self

    def __repr__(self):
        attrs = ', '.join(
            f'{attr}={value!r}'
            for attr, value in self.__dict__.items()
            if not attr.startswith('_')
        )
        return f'JSONObject({attrs})'

    __str__ = __repr__

    @classmethod
    def _translate_list(cls, items: list) -> list:
        for i in range(len(items)):
            item = items[i]
            if item.__class__ is list:
                items[i] = cls._translate_list(item)
            elif item.__class__ is dict:
                items[i] = cls(item)
        return items


class JsonObject(object):
    def __init__(self, dictionary: dict = None, **kvs):
        """
        将字典转化为对象（非递归）。

        :param dictionary: 包含数据的字典。请确保所有键都符合标识符命名要求，且均为字符串。
        :param kvs: 任意键值对。
        :return: JSONObject。
        :raise TypeError: 属性名称必须是字符串。
        """
        for k, v in {**(dictionary if dictionary else {}), **kvs}.items():
            k = str(k)
            if k.isidentifier():
                self.__setattr__(k, v)

    def __or__(self, dictionary: dict):
        for k, v in dictionary.items():
            k = str(k)
            if k.isidentifier():
                self.__setattr__(k, v)
        return self

    def __repr__(self):
        attrs = ', '.join(
            f'{attr}={value!r}'
            for attr, value in self.__dict__.items()
            if not attr.startswith('_')
        )
        return f'JsonObject({attrs})'

    __str__ = __repr__


def casting(
        mapper: Callable,
        raw,
        *errs: Exception,
        default=None,
):
    """
    使用mapper将raw转换为所需的值，当出现异常时返回default。

    默认捕获以下异常，可以通过errs参数追加更多异常：
        - ValueError
        - KeyboardInterrupt

    :param mapper: 类型转换器。如果转换器不可调用，将直接返回默认值。
    :param raw: 被转换的值。
    :param errs: 需要捕获的其它异常。应当提供可被 except 语句接受的值，否则会出现异常。
    :param default: 默认值。即使不提供也会默认返回 None 而不会抛出异常。
    :return: 转换后的值。如若捕获到特定异常将返回默认值。
    """
    if not callable(mapper):
        return default
    try:
        return mapper(raw)
    except (ValueError, KeyboardInterrupt) + errs:
        return default


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
    elif isinstance(value, datetime.date):
        return f'[{value:%Y-%m-%d}]'
    elif isinstance(value, datetime.datetime):
        return f'[{value:%Y-%m-%d %H:%M:%S,%f}]'
    elif isinstance(value, datetime.timedelta):
        return f'[{value.days}d,{value.seconds}s,{value.microseconds}μs]'
    elif isinstance(value, UUID):
        return value.hex
    else:
        return repr(value)


class ReprMixin(object):
    class AttributeMeta:
        pass

    class TagMeta:
        pass

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
        return ', '.join(obtain())

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
                    pass

        attributes = self.TagMeta.__dict__
        annotations = attributes.get('__annotations__', {})
        return ' '.join(obtain())

    def _obtain_pk(self) -> str:
        if hasattr(self, 'pk'):
            return represent(self.pk)
        if hasattr(self, 'id'):
            return represent(self.id)
        return ''

    def _obtain_kls(self) -> str:
        return self.__class__.__name__
