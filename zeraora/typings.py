__all__ = [
    'JSONObject',
    'JsonObject',
]


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
