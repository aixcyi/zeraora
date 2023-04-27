# Zeraora

## Index

**B**

- `charsets.BASE8`
- `charsets.BASE16`
- `charsets.BASE36`
- `charsets.BASE62`
- `charsets.BASE64`
- `charsets.BASE64SAFE`
- [`BearTimer()`](./zeraora/BearTimer.md)，对代码运行进行计时，并打印时间和提示。

**C**

- `casting()`，转换一个值或返回默认值，以确保不会发生异常。
- [`Choices()`](https://docs.djangoproject.com/zh-hans/4.2/ref/models/fields/#enumeration-types)，用于创建带有标签文本的枚举的类。
- [`ChoicesMeta()`](https://docs.djangoproject.com/zh-hans/4.2/ref/models/fields/#enumeration-types)，用于创建带有标签文本的枚举的元类。

**D**

- `datasize()`，将一个字面量转换为字节数目。
- `delta2hms()`，将时间增量转换为时分秒格式，其中秒钟以小数形式包含毫秒和微秒。
- `delta2ms()`，将时间增量转换为分秒格式，其中秒钟以小数形式包含毫秒和微秒。
- `delta2s()`，将时间增量转换为秒钟数，以小数形式包含毫秒和微秒。
- `charsets.DIGITS`
- `charsets.DIGITS_SAFE`

**E**

- `djangobase.EasyViewSetMixin()`，提供两个方法来简化 `ViewSetMixin.as_view()` 的传参。

**H**

- `charsets.HEXDIGITS`

**I**

- [`IntegerChoices()`](https://docs.djangoproject.com/zh-hans/4.2/ref/models/fields/#enumeration-types)，用于创建值是整数的带有标签文本的枚举的类。

**L**

- `charsets.LETTERS`
- `charsets.LETTERS_SAFE`
- `charsets.LOWERS`
- `charsets.LOWERS_SAFE`

**O**

- `charsets.OCTDIGITS`
- [`OnionObject()`](./zeraora/OnionObject.md)，将字典构造为对象，使得可以用点分法代替下标访问内容。

**P**

- `Province`，中国省级行政区。（常量枚举）

**R**

- `randb62()`，生成 n 个 base62 随机字符。
- `randb64()`，生成 n 个 base64 随机字符。
- `randbytes()`，生成 n 个随机字节。此函数用于在 Python 3.9 以前代替 random.randbytes(n) 方法。
- `REGIONS`，中国省份和大区之间的映射。
- `remove_exponent()`，去除十进制小数（Decimal）的尾导零。摘录自[Python文档](https://docs.python.org/zh-cn/3/library/decimal.html#decimal-faq)。
- `represent()`，将任意值转换为一个易于阅读的字符串。
- [`ReprMixin()`](./zeraora/ReprMixin.md)，用最小改动来生成通用representation的工具类。

**S**

- `SnowflakeMultiWorker()`，雪花ID生成的多例实现。
- `SnowflakeSingleWorker()`，雪花ID生成的单例实现。
- `SnowflakeWorker()`，雪花ID生成的基本实现。
- `djangobase.SoftDeleteModelMixin()`，将一个模型实例标记为已删除（软删除）。
- `@start()`，检查 Python 版本是否高于或等于指定值。
- `charset.SYMBOL`
- `charset.SYMBOL_NORMAL`
- `charset.SYMBOL_SHIFT`

**T**

- [`TextChoices()`](https://docs.djangoproject.com/zh-hans/4.2/ref/models/fields/#enumeration-types)，用于创建值是字符串的带有标签文本的枚举的类。

**U**

- `charset.UPPERS`
- `charset.UPPERS_SAFE`

**V**

- `version`，一个字符串，表示Zeraora的版本。

(*)

- `__author__`
- `__version__`，一个元组，表示Zeraora的版本。

