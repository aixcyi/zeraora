# 全局符号索引

## zeraora

- `__version__`，一个元组。表示Zeraora的版本。
- `version`，一个字符串。表示Zeraora的版本。
- `gvs`，全局变量包。

## zeraora.utils

> 偏工具属性的类与函数。

- [`BearTimer()`](./zeraora/BearTimer.md)，对代码运行进行计时，并打印时间和提示。
- [`ReprMixin()`](./zeraora/ReprMixin.md)，用最小改动来生成通用representation的工具类。
- `@start()`，检查 Python 版本是否高于或等于指定值。
- `@deprecate()`，为一个函数作废弃标记。指示被装饰的函数在当前版本下将于/已于某个版本废弃。
- `load_ads4()`，载入行政区划映射表。

## zeraora.typeclasses

> 数据类型类、枚举类、枚举元类、类型别名等。

- [`OnionObject()`](./zeraora/OnionObject.md)，将字典构造为对象，使得可以用点分法代替下标访问内容。
- `RadixInteger()`，一个以元组表述各个数位的 N 进制整数。
- `ItemsMeta()`，创建带有任意属性的枚举的类。
- `Items()`，每个值都带有任意属性的枚举。

## zeraora.structures

> 数据结构。

- `DivisionCode`，统计用行政区划代码。包含代码整体以及省市县乡村五个部分。
- `Division`，行政区划。包含名称、区划代码、层次层级、使用年份四个部分。

## zeraora.generators

> 用于随机生成和特定顺序生成的生成器。

- `randb62()`，生成 n 个 base62 随机字符。
- `randb64()`，生成 n 个 base64 随机字符。
- `randbytes()`，生成 n 个随机字节。用于在 Python 3.9 以前代替 `random.randbytes(n)` 方法。
- `SnowflakeWorker()`，雪花ID生成的基本实现。
- `SnowflakeMultiWorker()`，雪花ID生成的多例实现。
- `SnowflakeSingleWorker()`，雪花ID生成的单例实现。

## zeraora.converters

> 用于将一种值转换为另一种值的转换器。

- `remove_exponent()`，去除十进制小数（Decimal）的尾导零。摘录自[Python文档](https://docs.python.org/zh-cn/3/library/decimal.html#decimal-faq)。

#### 类型转换

- `casting()`，转换一个值或返回默认值，以确保不会发生异常。
- `true()`，将HTTP请求中 query 部分的参数值转换为 Python 的逻辑值。

#### 字面量

- `datasize()`，将一个字面量转换为字节数目。
- `represent()`，将任意值转换为一个易于阅读的字符串。

#### 时间相关

- `delta2hms()`，将时间增量转换为时分秒格式，其中秒钟以小数形式包含毫秒和微秒。
- `delta2ms()`，将时间增量转换为分秒格式，其中秒钟以小数形式包含毫秒和微秒。
- `delta2s()`，将时间增量转换为秒钟数，以小数形式包含毫秒和微秒。
- `wdate()`，将某一年的某一周的星期几转换为一个具体的日期。
- `get_week_range()`，计算一年中某一周对应的所有日期。
- `get_week_side()`，计算一年中某一周对应的第一天和最后一天。
- `get_week_in_year()`，计算一个具体日期自一年开始的周序号。

## zeraora.dj

> 包含对 Django 的增强。

- `SnakeModel`，一个元类，为模型生成一个下划线小写的（蛇形）数据表名。

#### 字段mixin

- `CreateTimeMixin`，附加一个创建时间字段。
- `DeletionMixin`，附加一个标记删除字段。
- `TimeMixin`，附加一个创建时间和一个修改时间字段。
- `IndexMixin`，附加一个自定义索引字段（ShortIntegerField）以及获取逆序和顺序查询集的两个类方法。
- `ShortIndexMixin`，附加一个自定义索引字段（IntegerField）以及获取逆序和顺序查询集的两个类方法。
- `UrgencyMixin`，附加一个紧急程度字段。
- `ImportanceMixin`，附加一个重要程度字段。
- `BizMixin`，附加一个自动生成业务ID（32位小写HEX字符串）的字段。
- `AddressMixin`，附加了省、市、县、乡镇、街道五个字段，区划代码一个属性，以及两个方法。
- `GlobalAddressMixin`，附加了国家、省、市、县、乡镇、街道、街道2、街道3等字段。

#### 字段

- `BizField`，对外业务ID字段，默认最大长度32字符。
- `MoneyField`，金额字段，默认存储12个数位，包含两位小数。
- `OSSPathField`，对象存储（OSS）中的文件路径。

#### [Lookup](https://docs.djangoproject.com/zh-hans/4.2/ref/models/lookups/#lookup-reference)

- `BitsIn`，过滤一个或多个比特存在于目标字段中的记录。
- `BitsAllIn`，过滤所有比特位都存在于目标字段中的记录。


## zeraora.drf

> 包含对 Django REST Framework 的增强。

- `EasyViewSetMixin`，提供两个方法来简化 `ViewSetMixin.as_view()` 的传参。
- `SoftDeleteModelMixin`，将一个模型实例标记为已删除（软删除）。
- `ExistingFilterBackend`，一个筛选中间件，用于筛选掉查询集中标记为已删除的结果。

## zeraora.constants

> 不变量。

- 枚举
  - `Region`，包含用于划分省级行政区的大区。
  - `Province`，包含34个省级行政区名称、区划代码、字母码、大区、简称、缩写。
  - `DivisionLevel`，行政区划的层次级别。
  - `Degree`，表示程度的五个档位（最高、高、正常、低、最低）。
- 默认配置
  - `LOG_CONF_BEAR`，工具类 `BearTimer` 的默认日志配置。
- 常量
  - `BASE8`
  - `BASE16`
  - `BASE36`
  - `BASE62`
  - `BASE64`
  - `BASE64SAFE`
  - `DIGITS`
  - `DIGITS_SAFE`
  - `HEXDIGITS`
  - `LETTERS`
  - `LETTERS_SAFE`
  - `LOWERS`
  - `LOWERS_SAFE`
  - `OCTDIGITS`
  - `SYMBOL`
  - `SYMBOL_NORMAL`
  - `SYMBOL_SHIFT`
  - `UPPERS`
  - `UPPERS_SAFE`
