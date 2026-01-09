---
title: "`conf` 配置辅助工具"
outline: deep
excerpt:
---

# <pre>zeraora.conf</pre>

此模块提供了一些方便开发人员编辑与使用“配置”的快捷方法和工具。

## `logc(*pairs, **kwargs)`

专为 Python
日志系统[配置字典架构](https://docs.python.org/zh-cn/3/library/logging.config.html#configuration-dictionary-schema)编写而生的
[`dict`](https://docs.python.org/zh-cn/3/library/functions.html#func-dict)
变种函数。它有以下功能：

- 接受逐个键值对入参。
- 去除“键”尾随的所有 `_` 字符。
- 将名为 `_` 的“键”替换成 `.`。
- 将名为 `__` 的“键”替换成 `()`。
- 将名为 `klass` 的“键”替换成 `class`。

```python
from zeraora.conf import logc

assert logc(
    __='my.package.customFormatterFactory',
    klass='logging.StreamHandler',
    level='DEBUG',
    filters=[],
    formatter='bear',
    _=dict(
        foo='baz',
    ),
) == {
    '()': 'my.package.customFormatterFactory',
    'class': 'logging.StreamHandler',
    'level': 'DEBUG',
    'filters': [],
    'formatter': 'bear',
    '.': {
        'foo': 'baz',
    },
}
```

## `WrappedListProperty(primitive, wrapper)`

包装列表属性。

一个数据描述器。在内部维护一个成员都是基本类型 _primitive_ 的列表（用于导出JSON），单独访问属性时会得到一个成员都是包装类型
_wrapper_ 的列表。

> [!TIP] 属性的内部值
> 属性的内部值寄存于所在对象的 `__dict__` 属性中，专门用于配合
> [`Configuration`](#Configuration) 使用，不太建议手动单独提取。

```python :line-numbers
from decimal import Decimal
from zeraora.conf import Configuration, WrappedListProperty


class StoreConfiguration(Configuration):
    # 定义属性
    concessions = WrappedListProperty(str, Decimal)  # [!code highlight]

    def __init__(self, __configs=None):
        # 定义默认值、类型提示
        self.concessions: list[Decimal] = [Decimal('0.9')]
        # 读取配置，覆盖默认值
        super().__init__(__configs or dict())

    def fill(self, save=True, *args, **kwargs):
        return self


# 使用时，直接覆盖属性
configs = StoreConfiguration()
configs.concessions  # [Decimal('0.9')]
configs.concessions = [Decimal('0.9'), Decimal('0.85')]  # [!code highlight]
configs.concessions  # [Decimal('0.9'), Decimal('0.85')]
configs.dump()  # {'$version': 1, 'concessions': ['0.9', '0.85']}

# 请不要在原地修改
configs.concessions  # [Decimal('0.9')]
configs.concessions.append(Decimal('0.85'))  # [!code error]
configs.concessions  # [Decimal('0.9')]
```

## `WrappedSetProperty(primitive, wrapper)`

包装集合属性。

一个数据描述器。在内部维护一个成员都是基本类型 _primitive_ 的 **列表**（方便用于导出JSON），单独访问属性时会得到一个成员都是包装类型
_wrapper_ 的集合。

> [!TIP] 属性的内部值
> 属性的内部值寄存于所在对象的 `__dict__` 属性中，专门用于配合
> [`Configuration`](#Configuration) 使用，不太建议手动单独提取。

```python :line-numbers
from decimal import Decimal
from zeraora.conf import Configuration, WrappedSetProperty


class StoreConfiguration(Configuration):
    # 定义属性
    concessions = WrappedSetProperty(str, Decimal)  # [!code highlight]

    def __init__(self, __configs=None):
        # 定义默认值、类型提示
        self.concessions: set[Decimal] = {Decimal('0.9')}
        # 读取配置，覆盖默认值
        super().__init__(__configs or dict())

    def fill(self, save=True, *args, **kwargs):
        return self


# 使用时，直接覆盖属性
configs = StoreConfiguration()
configs.concessions  # {Decimal('0.9')}
configs.concessions = {Decimal('0.9'), Decimal('0.85')}  # [!code highlight]
configs.concessions  # {Decimal('0.9'), Decimal('0.85')}
configs.dump()  # {'$version': 1, 'concessions': ['0.9', '0.85']}

# 请不要在原地修改
configs.concessions  # {Decimal('0.9')}
configs.concessions.add(Decimal('0.85'))  # [!code error]
configs.concessions  # {Decimal('0.9')}
```

## `Configuration`

配置映射编辑器。

一个抽象类。实现对字典／对象／JSON 这类配置的映射，用于实现缺省值的自动填充，以及具有代码提示的一次性编辑。

> [!TIP] 小提示
> 修改对象的属性值 **不会同步** 变更原始配置，除非手动调用 `self.load()` 方法。

```python :line-numbers
from decimal import Decimal
from zeraora.conf import Configuration, WrappedSetProperty


class StoreConfiguration(Configuration):
    # 建议每个实现都重新声明一遍，方便排查问题时一眼知晓当前配置的最新版本。
    VERSION = 1

    # 定义可自动转换的列表属性
    concessions = WrappedSetProperty(str, Decimal)

    def __init__(self, __store):
        # 定义默认值、类型提示
        self.enableStorehouse = False
        """启用仓库管理服务？"""
        self.minSaleableStock = 1
        """最低可售库存量。"""
        self.concessions: set[Decimal] = {Decimal('1')}
        """销售折扣（百分比）白名单。"""
        # 读取配置，覆盖默认值
        super().__init__(store.configuration or dict())
        # 声明“配置”之外的属性需要以下划线开头命名，避免被 dump() 导出。
        self._store_ = __store

    def fill(self, save=True, *args, **kwargs):
        # TODO: 填充到 ORM 模型，保存到数据库，亦或是导出到文件中。
        return self


store = ...
store.data = {
    "enableStorehouse": True,
    "concessions": ["1", "0.9", "0.85"]
}
configs = StoreConfiguration(store)
configs.enableStorehouse  # True
configs.minSaleableStock  # 1
configs.concessions  # {Decimal('1'), Decimal('0.9'), Decimal('0.85')}
configs.concessions = {Decimal('1'), '0.9', 0.5}
configs.concessions  # {Decimal('1'), Decimal('0.9'), Decimal('0.5')}
configs.dump()
```

```json
{
    "enableStorehouse": true,
    "minSaleableStock": 1,
    "concessions": ["1", "0.9", "0.5"]
}
```

> [!WARNING] 默认值
> 1. 应当声明在 `super().__init__()` 之前，避免被载入的配置覆盖。
> 2. 必须定义为对象变量，若定义为类变量，则在不经改动的情况下，无法被 `self.dump()` 及 `self.fill()` 检测到。

> [!WARNING] “描述器”的定义
> 按照[《描述器指南》](https://docs.python.org/zh-cn/3/howto/descriptor.html)，如若使用
> `WrappedListProperty`、`WrappedSetProperty` 等描述器，定义的属性必须是类变量；如果定义为对象变量，描述器将会失效。

### `load(configs)` {#Configuration.load}

载入一个 `dict` 类型的数据并覆盖当前配置。

- 返回 `Configuration` 对象自身；一般情况下不需要调用。
- 以 `_` 开头的字段不会被载入。
- 配置中的 `$version` 字段（若有则）会被存储到 `self._version_` 属性中，如有必要，可另写一个属性方便访问。

### `dump()` {#Configuration.dump}

导出当前配置，以 `dict` 类型返回。

- 未被载入的字段会填充为默认值。
- 最顶级的一层字段会按照 ASCII 进行排序。
- 固定导出一个名为 `$version` 的字段，其值固定为 `cls.VERSION`
  而不是载入的 `self._version_`，这是因为导出的配置已经补全缺失的值，理应使用更新的版本号。

### `diff()` {#Configuration.diff}

对比当前配置与载入的配置。

- 返回修改过值的字段的名称；如果一个字段未在类中定义未属性，或者一个字段并未出现在配置中，但定义了对应的属性，也会一并返回。
- 如果没有修改过 `$version` 则不会返回这个字段。

### `fill(save=True, *args, **kwargs)` {#Configuration.fill}

将配置导出填充到某处。

_**该方法为抽象方法**_。用于方便统一在业务代码中调用“保存”的逻辑，不管是填充到
ORM 模型、保存到数据库，还是另存到文中内。方法应当返回 `Configuration` 对象自身。

### `show(printer=print)` {#Configuration.show}

打印配置信息。

一个方便随时调试的简陋方法，`*` 开头表示已被修改的字段，打印格式如下：

```text
================================
StoreConfiguration
--------------------------------
* enableStorehouse = True
* minSaleableStock = 100
  concessions = ["1"]
================================
```

默认使用 `print()` 打印，如若提供其它方法或函数，它的第一个参数必须能接受字符串，其余参数必须允许省略，例如：

```python
import logging

logger = logging.getLogger('navifox.store')

if __name__ == '__main__':
    store = ...
    configs = StoreConfiguration(store)
    configs.show(logger.debug)
```
