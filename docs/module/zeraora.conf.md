---
title: "`conf` 配置辅助工具"
outline: deep
excerpt:
---

# <pre>zeraora.conf</pre>

此模块提供了一些方便开发、运维、运营编辑与使用“配置”的快捷方法和工具。

## Configuration

配置映射编辑器。

像 JavaScript 那样把字典当作一个对象使用，主要用于对“配置数据”的映射、编辑、补全。

- 不依赖文件，纯内存下读写。
- 自动填充缺漏字段。
- IDE 下可提供类型提示、字段补全。
- 可定义包装对象数组以快速存储和无损访问。
- 支持版本管理。
- 支持对比原始配置。
- 支持直接打印。

这不是一个面向文件的、允许用户编辑的配置的“加载器”，而是一个让开发者在代码中更方便、更准确地使用、修改配置的“编辑器”，所有字段名（包括动态插入的）都应该在程序运行前就定好，因此不会提供额外的钩子用来统一字段命名风格、识别/兼容非法字段名。

如果你的需求是“加载配置文件”或者刚需与文件交互，[Pydantic](https://pypi.org/project/pydantic/)、[python-box](https://pypi.org/project/python-box/)
和 [Prodict](https://pypi.org/project/prodict/) 可能是更好的选择。

### 基础用法 {#Configuration-Basic-Usage}

1. 创建一个新的类并继承 `Configuration`。
2. 实现所有抽象方法。
3. 重新定义 `VERSION` 常量（哪怕值与父类一致）。
4. 自定义初始化过程 `__init__()`：
   1. 定义字段、提供默认值，（可选）标注字段的类型。
   2. 调用 `super().__init__()`。
   3. 执行你需要的其它操作。

> [!IMPORTANT] 重要提醒
> - 不要打乱初始化过程的顺序，不然实际的数据会被默认值覆盖掉。
> - 字段必须定义为对象变量，如果定义为类变量，那么不经改动的情况下，无法被其它对象方法感知到。

```python :line-numbers
from decimal import Decimal
from zeraora.conf import Configuration

class StoreConfiguration(Configuration):
    """
    各个门店单独的配置。
    """
    VERSION = 1

    def __init__(self, configs: dict | None = None):
        self.enableStorehouse = False
        """
        启用库存管理服务？
        """
        self.stockSalableFloor = 1
        """
        最低可售库存量。
        """
        self.sellingPlatforms = ['applet', 'cashier', 'kiosk']
        """
        允许在哪些销售平台展示。
        """
        super().__init__(configs or dict())  # 读取配置，覆盖默认值

    def fill(self, save=True, *args, **kwargs):
        return self
```

### 定制初始化过程 {#Configuration-Customize-Initialization}

如果配置位于一个复合对象（例如 Django ORM 的 `Model` 对象）内，可以重写
`__init__()` 的参数来接收这个对象，然后在 `fill()` 中将当前配置写回去。

```python :line-numbers
from decimal import Decimal
from django.db import models  # [!code ++]
from zeraora.conf import Configuration

class Store(models.Model):  # [!code ++:6]
    """
    门店信息。
    """
    name = models.CharField(max_length=100)
    configuration = models.JSONField(default=dict)

class StoreConfiguration(Configuration):
    """
    各个门店单独的配置。
    """
    VERSION = 1

    def __init__(self, configs: dict | None = None):  # [!code --]
    def __init__(self, store: Store):  # [!code ++]
        self.enableStorehouse = False
        """
        启用库存管理服务？
        """
        self.stockSalableFloor = 1
        """
        最低可售库存量。
        """
        self.sellingPlatforms = ['applet', 'cashier', 'kiosk']
        """
        允许在哪些销售平台展示。
        """
        super().__init__(configs or dict())  # [!code --]
        super().__init__(store.configuration)  # [!code ++]
        self._store_ = store  # [!code ++]

    def fill(self, save=True, *args, **kwargs):  # [!code --:2]
        return self
    def fill(self, save=True, *args, **kwargs):  # [!code ++:6]
        store = self._store_
        store.configuration = self.dump()
        if save:
            store.save()
        return self
```

### 包装数组 {#Configuration-Define-Array-Fields}

以下面的代码为例，为 `concessions` 声明一个 [`WrappedListProperty`](#WrappedListProperty)
可以自动包装数组内的元素，这样访问 `StoreConfiguration().concessions`
时就可以得到一个 `List[Decimal]` 类型的列表，而在内部依然会存储为一个 `List[str]`
以便快速导出。

```python :line-numbers
from decimal import Decimal
from zeraora.conf import Configuration, WrappedListProperty  # [!code focus]

class StoreConfiguration(Configuration):
    """
    各个门店单独的配置。
    """
    VERSION = 1

    concessions = WrappedListProperty(str, Decimal)  # [!code focus]

    def __init__(self, configs: dict | None = None):
        self.concessions: list[Decimal] = [Decimal('1')]  # [!code focus:4]
        """
        销售折扣白名单。留空则允许收银员输入任意折扣。
        """
        super().__init__(configs or dict())

    def fill(self, save=True, *args, **kwargs):
        return self
```

### 包装集合 {#Configuration-Define-Set-Fields}

如果想让数组字段自动去除重复元素，可以为 `concessions` 声明一个
[`WrappedSetProperty`](#WrappedSetProperty)，这样访问 `StoreConfiguration().concessions`
时就可以得到一个 `Set[Decimal]` 类型的集合，而在内部依然会存储为一个 `List[str]`
以便快速导出。

```python :line-numbers
from decimal import Decimal
from zeraora.conf import Configuration, WrappedSetProperty  # [!code focus]


class StoreConfiguration(Configuration):
    """
    各个门店单独的配置。
    """
    VERSION = 1

    concessions = WrappedSetProperty(str, Decimal)  # [!code focus]

    def __init__(self, configs: dict | None = None):
        self.concessions: set[Decimal] = {Decimal('1')}  # [!code focus:4]
        """
        销售折扣白名单。留空则允许收银员输入任意折扣。
        """
        super().__init__(configs or dict())  # 读取配置，覆盖默认值

    def fill(self, save=True, *args, **kwargs):
        # 因为不需要保存，所以这里没有具体实现
        return self
```

### `$version` 与版本管理 {#Configuration-Versioning-Control}

`super().__init__(configs)` 与 `self.load(configs)` 时会自动读取版本号：

```python
self._version_ = configs.get('$version', self.VERSION)
```

而在导出的配置中（包括 `self.dump()` 和 `self.json()`）都会额外包含一个 `$version` 字段，值固定为 `cls.VERSION`
而不是载入的 `self._version_`，这是因为导出的配置已经补全缺失的值，理应使用更新的版本号。

`$version` 指的是一个用于版本管理的字段，可以重写 `cls.VERSIONING_CONTROL_FIELD` 来控制这个字段名。

> [!NOTE] 备注
> 文档（全文）及示例代码都会用 `$version` 代指版本管理字段。

### 导出配置与转换 {#Configuration-Dump-Data}

调用 [`self.dump()`](#Configuration.dump) 就能拿到 `dict`
类型的、包含所有字段的配置，而调用 [`self.json()`](#Configuration.json)
则以一个 JSON 字符串返回。导出结果会额外包含一些特殊字段（如果载入的数据没有的话），比如
`$version`，若不需要，请指定参数 `pure=True` 。

`self.json()` 也支持 [`json.dump()`](https://docs.python.org/zh-cn/3/library/json.html#json.dumps)
的所有可选参数，而后者默认将非 ASCII 字符串转换为 ASCII，要是不想这样，请指定参数
`ensure_ascii=False`。补充一句，以下是导出最短 JSON 字符串的写法：

```python
self.json(separators=(',', ':'))
```

### 比对／打印 {#Configuration-Diff-And-Print}

在调用了 `super().__init__(configs)` 或 `self.load(configs)` 之后，这份 `configs`
会作为[原始配置](#Configuration.loaded)保存在内部，对
`self` 的修改不会影响到 `configs`。

调用 [`self.diff()`](#Configuration.diff)
可以一个字符串集合，这个集合包含了当前配置与原始数据有差异的字段名。

想更直观地浏览变更，可以直接打印 `Configuration` 实例，只要是支持通过 `str()` 转换的方式都可以：

```python
from decimal import Decimal
from typing_extensions import Self
from zeraora.conf import Configuration
import logging

class StoreConfiguration(Configuration):
    """
    各个门店单独的配置。
    """
    VERSION = 1

    def __init__(self, configs: dict | None = None):
        self.enableStorehouse = False
        self.stockSalableFloor = 1
        self.concessions = [Decimal('1')]
        super().__init__(configs or dict())

    def fill(self, save=True, *args, **kwargs) -> Self:
        return self

config = StoreConfiguration()
config.concessions = [Decimal('0.5'), Decimal('1'), Decimal('0.9')]
config.stockSalableFloor = 100
logger = logging.getLogger(__file__)  # [!code focus:4]
logger.debug(config)  # [!code focus:4]
print(config)  # [!code focus:4]
```

打印格式如下，`*` 开头表示已被修改的字段：

```text
================================
StoreConfiguration
--------------------------------
* $version = 1
* concessions = ['0.5', '1', '0.9']
  enableStorehouse = False
* stockSalableFloor = 100
================================
```

### 初始化 {#Configuration.init}

```python
class Configuration:
    def __init__(self, configs: dict) -> None:
```
默认只接收一个 `dict`，但比较推荐重写来接收你想要的参数（比如 Django ORM 模型实例什么的）。

不论如何，应当且仅在这个方法内定义字段及其默认值，并且在所有字段定义之后再调用
`super().__init__(configs)`，不然载入的数据会覆盖掉默认值。 

当你调用 `super().__init__(configs)` 时，最终执行的是
`self.load(configs)`，所以如果想要定制底层载入逻辑，重写
[`self.load()`](#Configuration.load) 即可。

### load 方法 {#Configuration.load}

```python
class Configuration:
    def load(self, configs: dict) -> Self:
```
覆盖更新当下所有配置，并将 `configs` 覆盖存储为[原始配置](#Configuration.loaded)用于比对。

- 以 `_` 开头的字段会被过滤掉。
- 字段名不是[标识符](https://docs.python.org/zh-cn/3/reference/lexical_analysis.html#identifiers)的也会被过滤掉。
- `$version` 字段（如果有则）会被存储到 [`self._version_`](#Configuration.version) 中。
- 没有值的字段会用默认值填充。

### dump 方法 {#Configuration.dump}

```python
class Configuration:
    def dump(self, pure=False) -> dict:
```

导出当前配置为一个 `dict`。

- 最顶级的一层字段会按照 ASCII 进行排序。
- `pure=False` 时还会导出一个 `$version` 字段。

### json 方法 {#Configuration.json}

```python
class Configuration:
    def json(self, pure=False, **kw) -> str:
```

导出当前配置成一个 JSON 字符串。

- 最顶级的一层字段会按照 ASCII 进行排序。
- `pure=False` 时还会导出一个 `$version` 字段。
- 其余可选参数 _kw_ 与 [`json.dump()`](https://docs.python.org/zh-cn/3/library/json.html#json.dumps) 的一致。

### diff 方法 {#Configuration.diff}

```python
class Configuration:
    def diff(self) -> set[str]:
```

对比当前配置与[原始配置](#Configuration.loaded)。

- 如果一个字段未在类中定义未属性，或者一个字段并未出现在配置中，但定义了对应的属性，也会一并返回。
- 如果没有修改过 `$version` 则不会返回这个字段。

### fill 方法 {#Configuration.fill}

```python
class Configuration:
    def fill(self, save=True, *args, **kwargs) -> Self:
```

_**该方法为抽象方法**_，大致用于实现下面这些逻辑：

- 填充当前配置数据到 ORM 模型。
- 保存当前配置数据到数据库。
- 另存当前配置数据到文件内。

如果以上逻辑一个都不需要，直接返回 `self` 就好了。

### VERSION {#Configuration.VERSION}

```python
class Configuration:
    VERSION: int
```

一个常量，表示当前配置的架构版本。

Zeraora 默认使用 _int_ 存储版本号，因为 _int_
类型方便比较、存储、识读，并且简易配置数据的版本号一般不需要划分得很细。如果需要像 `3.14.1`
这样允许多段的版本号，可以考虑编码成 `3014001` 或者 `0x030e01` 这样的整数。

实在想改成 _str_ 或其它单体类型也没问题，重新声明
[`cls.VERSION`](#Configuration.VERSION)
和 [`self._version_`](#Configuration.version)
的类型即可，只不过在判断时需要格外注意类似 `"3.14" < "3.9"` 的问题。

需要注意的是，这个常量在设计之初就没有考虑过 `tuple` 这类复合类型；如果实在需要，请考虑使用
`@property` 增设一个属性来动态转换。

> [!TIP] 强烈建议
> 实现 `Configuration` 时，建议覆盖这个常量，哪怕你需要的值跟 `Configuration` 的一样。

### \_loaded_ 字段 {#Configuration.loaded}

一个非公开字段，用于存储配置的“原始配置”。

所谓的原始配置，就是最初载入的配置，不会随着 `Configuration` 实例的修改而修改，用于与修改后的配置进行比对。

它在 `super().load(configs)` 和 `super().__init__()`
时会被重新赋值，且不会自动执行 **浅拷贝** 或 **深拷贝**，所以赋值之后 `configs['foo'] = "bar"`
会导致原始配置被修改。

不过一般不需要为此做任何处理，之所以这么设计，是因为映射器的目的本就是避免直接修改
`dict`，再加上深拷贝会对性能有些许影响、浅拷贝又不能保证隔绝这种牵连，所以将操作交给调用方。

### \_version_ 字段 {#Configuration.version}

一个非公开字段，用于表示[原始配置](#Configuration.loaded)的版本。

它是 `super().load(configs)` 时自动从 `configs` 提取的 `$version`
字段的值，如果没有这个字段，则使用 [`cls.VERSION`](#Configuration.VERSION) 填充。

## WrappedListProperty

```python
WrappedListProperty(primitive, wrapper)
```

包装列表属性。

直接访问属性会得到一个全新的 `List[wrapper]` 类型的列表，而在内部维护着一个同步变更的 `List[primitive]` 类型的列表。

这个属性设计之初就是配合 [`Configuration`](#Configuration) 使用的，以下面为例，内部是一个
`List[str]` 类型的列表，直接访问 `conf.concessions` 会得到一个 `List[Decimal]` 类型的列表。

注意，必须在 `class` 下定义成“类变量”，而不能在 `def` 内定义成“对象变量”，因为 `WrappedListProperty`
是一个描述器类。详见[《描述器指南》](https://docs.python.org/zh-cn/3/howto/descriptor.html)。

```python :line-numbers
from decimal import Decimal
from zeraora.conf import Configuration, WrappedListProperty  # [!code focus]

class StoreConfiguration(Configuration):
    """
    各个门店单独的配置。
    """
    VERSION = 1

    concessions = WrappedListProperty(str, Decimal)  # [!code focus]

    def __init__(self, configs: dict | None = None):
        self.concessions: list[Decimal] = [Decimal('1')]  # [!code focus:4]
        """
        销售折扣白名单。留空则允许收银员输入任意折扣。
        """
        super().__init__(configs or dict())

    def fill(self, save=True, *args, **kwargs):
        return self

conf = StoreConfiguration()  # [!code focus:5]
conf.concessions  # [Decimal('0.9')]
conf.concessions = [Decimal('0.9'), Decimal('0.85')]  # [!code highlight]
conf.concessions  # [Decimal('0.9'), Decimal('0.85')]
conf.dump()
```

```json
{
    "$version": 1, 
    "concessions": [
        "0.9", 
        "0.85"
    ]
}
```

另外，访问 `StoreConfiguration().concessions` 拿到的列表是 **动态生成** 的，所以想要修改它，只能 **覆盖** 字段值：

```python
conf = StoreConfiguration()
conf.concessions  # 返回 [Decimal('1')]
conf.concessions = [Decimal('1'), Decimal('0.9'), Decimal('0.85')]
conf.concessions  # 返回 [Decimal('1'), Decimal('0.9'), Decimal('0.85')]
```

对它的任何操作都会被直接丢弃：

```python
conf = StoreConfiguration()
conf.concessions  # 返回 [Decimal('1')]
conf.concessions.append(Decimal('0.85'))
conf.concessions  # 返回 [Decimal('1')]
```

::: details 获取内部列表
可以通过 `conf.__dict__['concessions']` 拿到 `List[primitive]`
类型的内部列表，不过一般情况下你不太会需要这个。
:::

_primitive_ 和 _wrapper_ 两种类型一定要可以相互转换，比如 str 和 Decimal 可以做到 `str(Decimal())` 和
`Decimal(str())`；如果不能，推荐改成一个函数，比如 str 和 datetime 可以这样写：

```python
from datetime import datetime
from zeraora.conf import Configuration, WrappedListProperty

def ymdhms(v: str):
    return datetime.strptime(v, '%Y-%m-%d %H:%M:%S')

class StoreConfiguration(Configuration):
    shelf_at = WrappedListProperty(str, ymdhms)
```

_primitive_ 一般来说都是用可导出 JSON 或其它文本格式的类型，这样可以让“配置类”的存储格式更加广泛；_wrapper_
应该优先考虑类型，如果实在不能互相转换，应当定义成函数，而不是使用 _lambda_，这样会加重代码阅读者的心智负担！

## WrappedSetProperty

```python
WrappedSetProperty(primitive, wrapper)
```

包装集合属性。

除了直接访问属性会得到 `set[wrapper]` 类型的集合，其它细节与 [`WrappedListProperty`](#WrappedListProperty) 别无二致。

## logc

```python
def logc(*pairs: dict[str, Any], **kwargs) -> dict:
```

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

> [!TIP] 意义何在？
> - 以“函数参数”的方式传递 **不能够自定义** 的字段；
> - 以“字典字面值”的方式传递 **可以自定义** 的字段。
> 
> 这可能是一个不错的编码风格。这个函数便是解决“函数参数”命名问题的。
