# Zeraora Index

#### 食用指南

- 列出的符号是在 `from zeraora import (*)` 的情形下的表述，譬如以下示例中的 `BearTimer` 和 `drf.SoftDeleteModelMixin`

但这只是**表述方式**，实际上可以通过任何方式来导入，不必拘泥于此。

```Python
from rest_framework.generics import GenericAPIView
from zeraora import BearTimer, drf


@BearTimer()
class AccountView(drf.SoftDeleteModelMixin,
                  GenericAPIView):
  pass
```

#### 可食用子包

- `dj`，包含对 Django 的增强。
- `drf`，包含对 Django REST Framework 的增强。
- `constants`，包含常量及枚举。

## 工具类

- [`BearTimer()`](./zeraora/BearTimer.md)，对代码运行进行计时，并打印时间和提示。
- [`ReprMixin()`](./zeraora/ReprMixin.md)，用最小改动来生成通用representation的工具类。

## 优化／增强

- ORM模型
  - `dj.SnakeModel`，一个元类，为模型生成一个下划线小写的（蛇形）数据表名。
  - `dj.CreateTimeMixin`，附加一个创建时间字段。
  - `dj.DeletionMixin`，附加一个标记删除字段。
  - `dj.TimeMixin`，附加一个创建时间和一个修改时间字段。
  
- 视图类
  - `drf.EasyViewSetMixin`，提供两个方法来简化 `ViewSetMixin.as_view()` 的传参。
  - `drf.SoftDeleteModelMixin`，将一个模型实例标记为已删除（软删除）。

## 数据类型

- [`OnionObject()`](./zeraora/OnionObject.md)，将字典构造为对象，使得可以用点分法代替下标访问内容。
- `RadixInteger()`，一个以元组表述各个数位的 N 进制整数。
- `ItemsMeta()`，创建带有任意属性的枚举的类。
- `Items()`，每个值都带有任意属性的枚举。

## 转换器

- `remove_exponent()`，去除十进制小数（Decimal）的尾导零。摘录自[Python文档](https://docs.python.org/zh-cn/3/library/decimal.html#decimal-faq)。
- 类型转换
  - `casting()`，转换一个值或返回默认值，以确保不会发生异常。
  - `true()`，将HTTP请求中 query 部分的参数值转换为 Python 的逻辑值。
- 字面量
  - `datasize()`，将一个字面量转换为字节数目。
  - `represent()`，将任意值转换为一个易于阅读的字符串。
- 时间
  - `delta2hms()`，将时间增量转换为时分秒格式，其中秒钟以小数形式包含毫秒和微秒。
  - `delta2ms()`，将时间增量转换为分秒格式，其中秒钟以小数形式包含毫秒和微秒。
  - `delta2s()`，将时间增量转换为秒钟数，以小数形式包含毫秒和微秒。

## 生成器

- `randb62()`，生成 n 个 base62 随机字符。
- `randb64()`，生成 n 个 base64 随机字符。
- `randbytes()`，生成 n 个随机字节。用于在 Python 3.9 以前代替 `random.randbytes(n)` 方法。
- `SnowflakeWorker()`，雪花ID生成的基本实现。
- `SnowflakeMultiWorker()`，雪花ID生成的多例实现。
- `SnowflakeSingleWorker()`，雪花ID生成的单例实现。

## 检查器

- `@start()`，检查 Python 版本是否高于或等于指定值。

## 常量／枚举

- `charsets.Region`，一个枚举。包含用于划分省级行政区的大区。
- `charsets.Province`，一个枚举。包含34个省级行政区名称、区划代码、字母码、大区、简称、缩写。
- `charsets.BASE8`
- `charsets.BASE16`
- `charsets.BASE36`
- `charsets.BASE62`
- `charsets.BASE64`
- `charsets.BASE64SAFE`
- `charsets.DIGITS`
- `charsets.DIGITS_SAFE`
- `charsets.HEXDIGITS`
- `charsets.LETTERS`
- `charsets.LETTERS_SAFE`
- `charsets.LOWERS`
- `charsets.LOWERS_SAFE`
- `charsets.OCTDIGITS`
- `charsets.SYMBOL`
- `charsets.SYMBOL_NORMAL`
- `charsets.SYMBOL_SHIFT`
- `charsets.UPPERS`
- `charsets.UPPERS_SAFE`
- `__version__`，一个元组。表示Zeraora的版本。
- `version`，一个字符串。表示Zeraora的版本。
