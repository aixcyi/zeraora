---
title: UUID
outline: deep
excerpt:
---

# <pre>zeraora.uuid</pre>

此模块提供不可变
[`UUID`](https://docs.python.org/zh-cn/3/library/uuid.html#uuid.UUID)
对象的一些相关函数，用于生成
[RFC 9562](https://datatracker.ietf.org/doc/html/rfc9562.html)（取代了
[RFC 4122](https://datatracker.ietf.org/doc/html/rfc4122.html)）中特定版本的
UUID。另外也可参见[《UUID 结构梳理》](https://blog.navifox.net/refs/uuid)了解 UUID 结构。

> UUID，全局唯一标识符，Universally Unique IDentifier。

## uuid7

```python
def uuid7() -> uuid.UUID:
```

根据 RFC 9562 定义的[第七版](https://datatracker.ietf.org/doc/html/rfc9562.html#section-5.7)
UUID，生成一个带有毫秒级时间戳和一个随机数的 [`UUID`](https://docs.python.org/zh-cn/3/library/uuid.html#uuid.UUID) 对象。

> [!WARNING] 注意
> 此函数使用了标准库 [`random`](https://docs.python.org/zh-cn/3/library/random.html)
> 来产生随机数，因此不应将其用于安全目的。

| 位置                                                          | 字段  | 取值范围                           | 说明                                                  |
|-------------------------------------------------------------|-----|--------------------------------|-----------------------------------------------------|
| <pre>**00112233**-**4455**-7677-8899-aabbccddeeff</pre>     | 时间戳 | <pre>[0, 2<sup>48</sup>)</pre> | 毫秒级 Unix 时间戳。可存储约 8925 年 187 天 5 小时 31 分钟 50.655 秒。 |
| <pre>00112233-4455-7**677**-**8899**-**aabbccddeeff**</pre> | 随机数 | <pre>[0, 2<sup>74</sup>)</pre> |                                                     |
| <pre>00112233-4455-**7**677-8899-aabbccddeeff</pre>         | 版本  | 固定值                            | UUID 的版本。                                           |
| <pre>00112233-4455-7677-**8**899-aabbccddeeff</pre>         | 种类  | 固定值                            | UUID 的种类，仅占用高 2 位。                                  |

> [!NOTE] 备注
> Python 3.14 开始，标准库 [uuid](https://docs.python.org/zh-cn/3/library/uuid.html#uuid.uuid7)
> 已内置同名方法，Zeraora 会用它来代替自己的实现。

### 判定方式 {#uuid7-assertion}

判定是不是第七版 UUID 的方式如下：

```python
import uuid
from zeraora.uuid import uuid7

assert (
    uuid7().variant == uuid.RFC_4122 and
    uuid7().version == 7
)
```

### 提取时间戳 {#uuid7-stamp-extraction}

第七版 UUID 是 RFC 9562 中唯一一种使用 Unix 时间戳的 UUID，通过以下方式可以提取出毫秒级时间戳：

```python
from zeraora.uuid import uuid7

milliseconds: int = uuid7().int >> 80
```

若要一个秒级时间戳，可按如下方式提取：

```python
from zeraora.uuid import uuid7

seconds: float = (uuid7().int >> 80) / 1000
```

## uuid8

```python
def uuid8(
    a: int | None = None,
    b: int | None = None,
    c: int | None = None,
) -> uuid.UUID:
```

根据 RFC 9562 定义的[第八版](https://datatracker.ietf.org/doc/html/rfc9562.html#section-5.8)
UUID，生成一个自定义结构的
[`UUID`](https://docs.python.org/zh-cn/3/library/uuid.html#uuid.UUID) 对象。

三个参数预期为三个 48、12、62
比特的**非负整数**；如果超出长度，则仅保留最低有效位；若为负数，则将会取绝对值；如果没有提供，则分别替换成适当大小的随机数。

> [!WARNING] 注意
> 随机数使用了标准库 [`random`](https://docs.python.org/zh-cn/3/library/random.html)
> 来生成，因此若不提供参数，那么不应将本函数用于安全目的。

| 位置                                                      | 字段 | 取值范围                           | 说明                 |
|---------------------------------------------------------|----|--------------------------------|--------------------|
| <pre>**00112233**-**4455**-8677-8899-aabbccddeeff</pre> |    | <pre>[0, 2<sup>48</sup>)</pre> | 自定义结构 A 部分。        |
| <pre>00112233-4455-**8**677-8899-aabbccddeeff</pre>     | 版本 | 固定值                            | UUID 的版本。          |
| <pre>00112233-4455-8**677**-8899-aabbccddeeff</pre>     |    | <pre>[0, 2<sup>12</sup>)</pre> | 自定义结构 B 部分。        |
| <pre>00112233-4455-8677-**8**899-aabbccddeeff</pre>     | 种类 | 固定值                            | UUID 的种类，仅占用高 2 位。 |
| <pre>00112233-4455-8677-**8899**-**aabbccddeeff**</pre> |    | <pre>[0, 2<sup>62</sup>)</pre> | 自定义结构 C 部分。        |

> [!NOTE] 备注
> Python 3.14 开始，标准库 [uuid](https://docs.python.org/zh-cn/3/library/uuid.html#uuid.uuid8)
> 已内置同名方法，Zeraora 会用它来代替自己的实现。

### 判定方式 {#uuid8-assertion}

判定是不是第八版 UUID 的方式如下：（第一个断言是第二个断言成立的前置条件）

```python
import uuid
from zeraora.uuid import uuid8

assert (
    uuid8().variant == uuid.RFC_4122 and
    uuid8().version == 8
)
```

### 仿第七版 UUID {#uuid7-simulation}

如果既需要一个毫秒级时间戳，又需要自定义剩下的比特位，那么仿照第七版 UUID
来自定义结构是一个不错的选择，它的时间部分刚好用尽了参数 _a_ 的比特位，只需自定义参数
_b_ 和 _c_ 即可。以下是一个简易的封装：

```python
from time import time_ns
from zeraora.uuid import uuid8

def uuid8stamp(b: int = None, c: int = None):
    return uuid8(time_ns() // 1000_000, b, c)
```

### 压缩时间部分的比特位 {#uuid8-stamp-shortening}

当仍然需要记录时间时，比较推荐直接[仿第七版 UUID](#uuid7-simulation) 来自定义结构。

48 比特的毫秒级时间戳可存储近九千年的时间（见[上文](#uuid7)），虽然大部分业务并不需要如此离谱的时间长度，但一个
UUID 除去时间戳及固定部分，仍然有 122 比特可用，对于大部分业务来说已然足够，一般情况下 **没有必要** 压缩。

对于存储占用有更高要求的话可考虑选择总长度 64 比特的雪花ID（Snowflake ID）而不是总长度 128 比特的 UUID。

如果仍然需要压缩时间部分，可以根据实际业务需求，参考[《时间戳对照表》](https://blog.navifox.net/refs/timestamp)
选定时间的精度以及时间部分占用的长度，乃至更改时间戳的起点（epoch）。

## uuid8i

```python
def uuid8i(integer: int | None = None) -> uuid.UUID:
```

根据 RFC 9562 定义的[第八版](https://datatracker.ietf.org/doc/html/rfc9562.html#section-5.8)
UUID，生成一个自定义结构的
[`UUID`](https://docs.python.org/zh-cn/3/library/uuid.html#uuid.UUID) 对象。

> [!TIP] 温馨提示
> 该方法与上文的 `uuid8()` 等效，仅仅只是传参方式不同。

| 位置                                                                  | 字段 | 取值范围                            | 说明                 |
|---------------------------------------------------------------------|----|---------------------------------|--------------------|
| <pre>**00112233**-**4455**-8**677**-**8899**-**aabbccddeeff**</pre> |    | <pre>[0, 2<sup>122</sup>)</pre> | 自定义结构。             |
| <pre>00112233-4455-**8**677-8899-aabbccddeeff</pre>                 | 版本 | 固定值                             | UUID 的版本。          |
| <pre>00112233-4455-8677-**8**899-aabbccddeeff</pre>                 | 种类 | 固定值                             | UUID 的种类，仅占用高 2 位。 |

### 有效位说明 {#uuid8i-available-bits}

参数 _integer_ 可以是一个 128 比特都有效的整数（比如直接生成
128 比特的随机数），传入后会自动将特定的比特位过滤掉（剩余
122 比特可用），使其输出的 UUID 依然可以被判定为第八版 UUID。

```python
import uuid
from random import getrandbits
from zeraora.uuid import uuid8i

integer = getrandbits(128)
assert (
    uuid8i(integer).variant == uuid.RFC_4122 and
    uuid8i(integer).version == 7
)
```
