# Zeraora Index

> 按用途分类。
>
> - `djangobase` 模块主要存放一些基于[Django](https://pypi.org/project/Django/)的扩展。
> - `charsets` 模块主要存放一些常见常用的字符集。

## 工具类

- [`BearTimer()`](./zeraora/BearTimer.md)，对代码运行进行计时，并打印时间和提示。
- [`ReprMixin()`](./zeraora/ReprMixin.md)，用最小改动来生成通用representation的工具类。

## 优化／增强

- `djangobase.EasyViewSetMixin()`，提供两个方法来简化 `ViewSetMixin.as_view()` 的传参。
- `djangobase.SoftDeleteModelMixin()`，将一个模型实例标记为已删除（软删除）。

## 数据类型

- [`OnionObject()`](./zeraora/OnionObject.md)，将字典构造为对象，使得可以用点分法代替下标访问内容。
- `RadixInteger()`，一个以元组表述各个数位的 N 进制整数。
- 枚举相关
  - [`ChoicesMeta()`](https://docs.djangoproject.com/zh-hans/4.2/ref/models/fields/#enumeration-types)，创建带有标题的枚举的类。摘录自[Django 4.2.x](https://github.com/django/django/blob/stable/4.2.x/django/db/models/enums.py)。
  - [`Choices()`](https://docs.djangoproject.com/zh-hans/4.2/ref/models/fields/#enumeration-types)，带有标题的枚举。摘录自[Django 4.2.x](https://github.com/django/django/blob/stable/4.2.x/django/db/models/enums.py)。
  - [`TextChoices()`](https://docs.djangoproject.com/zh-hans/4.2/ref/models/fields/#enumeration-types)，值是字符串的、带有标题的枚举。摘录自[Django 4.2.x](https://github.com/django/django/blob/stable/4.2.x/django/db/models/enums.py)。
  - [`IntegerChoices()`](https://docs.djangoproject.com/zh-hans/4.2/ref/models/fields/#enumeration-types)，值是整数的、带有标题的枚举。摘录自[Django 4.2.x](https://github.com/django/django/blob/stable/4.2.x/django/db/models/enums.py)。
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

- `Region`，一个枚举。包含中国的大区。
- `Province`，一个枚举。包含中国省级行政区名称、区划代码、字母码、大区、简称、缩写。
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
