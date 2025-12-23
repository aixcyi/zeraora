__all__ = [
    'WrappedListProperty',
    'Configuration',
]

from typing_extensions import Self

from zeraora.string import StringBuilder


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


class Configuration:
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

    def fill(self, save=True) -> Self:
        """
        将配置导出填充到某处。

        *该方法为抽象方法*

        :param save: 填充后是否执行保存。
        :return: 自身。
        """
        raise NotImplementedError

    def show(self) -> Self:
        """
        打印配置信息。\n\n键为字段名，值为字段值。
        """
        print(
            StringBuilder()
            .writeline('=' * 32)
            .writeline(self.__class__.__name__)
            .writeline('-' * 32)
            .writes(f'{k} = {v!r}\n' for k, v in self.dump().items())
            .writeline('=' * 32)
        )
        return self
