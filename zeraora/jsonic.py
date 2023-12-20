"""
JavaScript Object Node 相关。
"""
from __future__ import annotations

__all__ = [
    'JSONObject',
]


class JSONObject(object):
    __depth: int
    __verify: bool

    def __new__(cls, _data: dict = None, _depth: int = -1, _verify_keys=False, **kvs):
        """
        一个仿照 JavaScript 对象设计的 Python 类。

        使用本类转换字典得到的实例 **可以也只能** 使用点分法代替下标访问字典的值。

        >>> resp = JSONObject({
        >>>     "code": 1,
        >>>     "message": "ok",
        >>>     "data": [
        >>>         {"openid": "d7d3d2ed", "username": "leo"},
        >>>     ],
        >>> })
        >>> resp.code  # => 1
        >>> resp.message  # => 'ok'
        >>> resp.data[0].username  # => "leo"

        可以通过 ``obj = obj | {}`` 或其语法糖 ``|=`` 来将字典直接更新到 ``JSONObject`` 对象：

        >>> a, b = 355, 113
        >>> obj = JSONObject({'a': a, 'b': b})
        >>> obj |= {'y': a / b}
        >>> obj.a  # => 355
        >>> obj.b  # => 113
        >>> obj.y  # => 3.1415929203539825

        可以通过 ``~obj`` 将 ``JSONObject`` 对象递归还原为字典：

        >>> a, b = 355, 113
        >>> obj = JSONObject({'a': a, 'b': b, 'y': a / b})
        >>> raw = ~obj
        >>> print(raw)  # => {'a': 355, 'b': 113, 'y': 3.1415929203539825}

        ----

        对于字典的键，本类仅转化符合 Python 变量命名规则且不以下划线（``"_"``）开头的，当遇到时，默认会直接跳过、不作处理。

        >>> data = JSONObject({
        >>>     "_secret": "BV1bW411n7fY",
        >>> })
        >>> hasattr(resp, '_secret')  # => False

        如果希望检测出这样的键名，可以通过指定构造器参数 ``_verify_keys=False`` 并捕获异常来实现。

        异常实例的 ``args`` 属性将会是一个四元素的元组，分别表示键的类型、值，当前转化的层级，以及提示文本。

        >>> try:
        >>>     data = JSONObject(_verify_keys=False, _data={
        >>>         "_secret": "BV1bW411n7fY",
        >>>     })
        >>> except KeyError as e:
        >>>     print(e.args[0])  # => <class 'str'>
        >>>     print(e.args[1])  # '_secret'
        >>>     print(e.args[2])  # -1
        >>>     print(e.args[3])  # '<提示文本>'

        注意：使用 ``hasattr()`` 函数时需要警惕被检测的键名是否以双下划线（``"__"``）开头，
        因为类的实现方法以及存储变量均以双下划线开头，这样做有可能导致误判。

        ----

        对于字典的值，本类仅转化 ``dict`` 、 ``list`` 、 ``tuple`` 及其子类的实例，其余类型会保留原值。

        >>> from datetime import date
        >>>
        >>> resp = JSONObject({
        >>>     "gender": {True, False, None},
        >>>     "join": (date(2012, 1, 1), date(2012, 1, 31)),
        >>>     "data": [
        >>>         {"openid": "d7d3d2ed", "gender": True, "username": "leo"},
        >>>         {"openid": "7b7c7fee", "gender": False, "username": "meow"},
        >>>     ],
        >>> })
        >>> type(resp.gender)  # => <class 'set'>
        >>> type(resp.join[0])  # => <class 'datetime.date'>
        >>> type(resp.data[0])  # => <class 'JSONObject'>
        >>> type(resp.join)  # => <class 'tuple'>
        >>> type(resp.data)  # => <class 'list'>

        注意，本类会保留字典值的类型为 ``list`` 、 ``tuple`` 及其子类的类型，
        如需转化后的实例的 “数组” 可变，请提前将数据中 ``tuple`` 类型的值（递归）转换为 ``list`` 类型的。

        ----

        对于 IDE 或类型检查工具给出的属性错误，可以通过添加属性类型标注的方式避免，并为可能不存在的键赋予默认值。

        >>> from typing import Any
        >>>
        >>> class TokenResponse(JSONObject):
        >>>     code: int
        >>>     message: str
        >>>     data: Any = None
        >>>
        >>> resp = TokenResponse({"code": 1, "message": "ok"})
        >>> resp.code  # => 1
        >>> resp.message  # => 'ok'
        >>> resp.data  # => None

        :param _data: ``dict`` 或其子类的实例。
        :param _depth: 递归转化的层数。负数表示无限递归转化，若提供 ``0`` 则以 ``dict`` 类型返回合并 ``kwargs`` 后的 ``data`` 。
        :param _verify_keys: 遇到不符合 Python 命名规则的键名时是否抛出异常。 ``False`` 表示忽略该键。
        :return: OnionObject 的对象。
        :raise TypeError: ``dictionary`` 不是 ``dict`` 或其子类的实例。
        :raise KeyError: 键名不符合 Python 命名规则且 ``_verify_key=True`` 。
        """
        if _data is None:
            _data = {}
        if not isinstance(_data, dict):
            raise TypeError(
                'JSONObject.__new__() 的 dictionary 参数必须是一个 dict 或其子类的实例。'
            )
        _data.update(kvs)

        # 必须在 0 时返回原值，否则在有限层递归时，从Object跨越到Array后会导致无限递归
        if _depth == 0:
            return _data

        self = object.__new__(cls)
        self.__verify = _verify_keys
        self.__depth = _depth
        self.__ior__(_data)
        return self

    def __repr__(self) -> str:
        attrs = ', '.join(
            f'{attr}={type(value).__name__}(...)'  # 避免重复递归
            if isinstance(value, JSONObject) else
            f'{attr}={value!r}'
            for attr, value in self.__dict__.items()
            if not attr.startswith('_')
        )
        return f'JSONObject({attrs})'

    def __or__(self, _data: dict) -> JSONObject:
        for k, v in _data.items():
            k = str(k)
            if not k.isidentifier() or k.startswith('_'):
                if not self.__verify:
                    continue
                else:
                    raise KeyError(
                        type(k), k, self.__depth,
                        f'键名不符合 Python 命名规则或以下划线开头：{k!s}'
                    )
            if isinstance(v, dict):
                self.__setattr__(k, self.__class__(
                    v, _depth=self.__depth - 1, _verify_keys=self.__verify
                ))
            elif isinstance(v, (list, tuple)):
                self.__setattr__(k, self.__translate_items(v[:]))
            else:
                self.__setattr__(k, v)
        return self

    __ior__ = __or__

    def __invert__(self) -> dict:
        return dict(self.__convert_to_dict())

    def __translate_items(self, items: list | tuple) -> list | tuple:
        """
        转化列表或元组的成员，并保留 ``items`` 本身的类型。
        """
        cls = type(self)

        def translate():
            for item in items:
                if isinstance(item, dict):
                    yield cls(
                        item,
                        _depth=(self.__depth - 1) if self.__depth else -1,
                        _verify_keys=self.__verify
                    )
                elif isinstance(item, (list, tuple)):
                    yield self.__translate_items(item)
                else:
                    yield item

        return type(items)(translate())

    def __convert_to_dict(self):
        prefix = f'_{type(self).__name__}__'
        for k, v in self.__dict__.items():
            if k.startswith('__') or k.startswith(prefix):
                continue
            if isinstance(v, (list, tuple)):
                yield k, type(v)(
                    ~i if isinstance(i, JSONObject) else i
                    for i in v
                )
            elif isinstance(v, JSONObject):
                yield k, ~v
            else:
                yield k, v
