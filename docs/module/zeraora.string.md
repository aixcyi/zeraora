---
title: "`string` 字符集与字符串"
outline: deep
excerpt:
---

# <pre>zeraora.string</pre>

此模块定义了一些字符集常量，以及生成字符串的工具类。

## Alphabet

一个静态类，包含不同编码的字符集，每个常量均为 `bytes` 类型。字符种类如下：

| 常量                    |    数字    | 大写<br/>字母 | 小写<br/>字母 | 可见<br/>符号 | 编码名称                                                                                          |
|-----------------------|:--------:|:---------:|:---------:|:---------:|-----------------------------------------------------------------------------------------------|
| `Alphabet.BASE16`     |    全部    | `A` 到 `F` |           |           | RFC 4648 [Base 16](https://datatracker.ietf.org/doc/html/rfc4648#section-7)                   |
| `Alphabet.BASE32`     | `234567` |    全部     |           |           | RFC 4648 [Base 32](https://datatracker.ietf.org/doc/html/rfc4648#section-6)                   |
| `Alphabet.BASE32HEX`  |    全部    | `A` 到 `V` |           |           | RFC 4648 [Base 32 with Extended Hex](https://datatracker.ietf.org/doc/html/rfc4648#section-7) |
| `Alphabet.BASE62`     |    全部    |    全部     |    全部     |           |                                                                                               |
| `Alphabet.BASE64`     |    全部    |    全部     |    全部     |     有     | RFC 4648 [Base 64](https://datatracker.ietf.org/doc/html/rfc4648#section-4)                   |
| `Alphabet.BASE64SAFE` |    全部    |    全部     |    全部     |     有     | RFC 4648 [Base 64 with URL Safe](https://datatracker.ietf.org/doc/html/rfc4648#section-5)     |
| `Alphabet.BASE85`     |    全部    |    全部     |    全部     |     有     | [Base85](https://docs.python.org/zh-cn/3/library/base64.html#base85-encodings)（未被正式规定的事实标准）   |
| `Alphabet.ASCII85`    |    全部    |    全部     |    全部     |     有     | [Ascii85](https://docs.python.org/zh-cn/3/library/base64.html#base85-encodings)（未被正式规定的事实标准）  |
| `Alphabet.Z85`        |    全部    |    全部     |    全部     |     有     | ZeroMQ [Z85](https://rfc.zeromq.org/spec/32/)                                                 |

> [!TIP] 注意
> 上表的种类出现顺序 **不代表** 实际常量值中的字符顺序。

## Notation

一个静态类，包含不同进位制的数码，每个常量均为 `str` 类型。字符种类如下：

| 常量                    |    数字     | 大写<br/>字母 | 小写<br/>字母 | 可见<br/>符号 | 备注             |
|-----------------------|:---------:|:---------:|:---------:|:---------:|----------------|
| `Notation.BASE8`      | `0` 到 `7` |           |           |           | 八进制            |
| `Notation.BASE10`     |    全部     |           |           |           | 十进制            |
| `Notation.BASE16`     |    全部     | `A` 到 `F` |           |           | 十六进制           |
| `Notation.BASE36`     |    全部     |    全部     |           |           | 36 进制          |
| `Notation.BASE62`     |    全部     |    全部     |    全部     |           | 62 进制          |
| `Notation.BASE64`     |    全部     |    全部     |    全部     |   `+/`    | 64 进制          |
| `Notation.BASE64SAFE` |    全部     |    全部     |    全部     |   `-_`    | 64 进制，URL 安全版。 |

## Char

一个静态类，包含不同类型的字符集，每个常量均为 `str` 类型，每个字符集的字符均按 ASCII 顺序排列。

- `Char.DIGIT` 包含全部阿拉伯数字。
- `Char.UPPER` 包含全部大写英文字母。
- `Char.LOWER` 包含全部小写英文字母。
- `Char.LETTER` 包含全部英文字母。
- `Char.SYMBOL` 包含 `\x21` 到 `\x7e` 之间的所有可见符号；即，排除空格、控制符、数字、大小写字母。
- `Char.DIGIT_SAFE` 包含除了 `0` 和 `1` 之外的所有阿拉伯数字。
- `Char.UPPER_SAFE` 包含除了 `I` 和 `O` 之外的所有大写英文字母。
- `Char.LOWER_SAFE` 包含除了 `l` 之外的所有小写英文字母。
- `Char.LETTER_SAFE` 包含除了大写的 `I`、`O` 和小写的 `l` 之外的英文字母。
- `Char.SYMBOL_NORMAL` 包含键盘上不按 Shift 键就能敲出的可见符号。
- `Char.SYMBOL_SHIFT` 包含键盘上需要按住 Shift 键才能敲出的可见符号。

## StringBuilder

```python
class StringBuilder:
    def __init__(self, *blocks, sep='', end='') -> None:
```

字符串构建器。

用于一次性聚合多个短小字符串，来构建一个较长的字符串。参数与
[`self.write()`](#StringBuilder.write) 相同，_blocks_ 支持传入任何能够转换成字符串的值。链式调用示例：

```python :line-numbers
from datetime import date
from zeraora.string import StringBuilder

user = dict(
    name='Tighnari',
    rank=5,
    title='浅蔚轻行',
    birth=date(2022, 12, 29),
)
print(
    StringBuilder()
    .writeline('User Info')
    .writeline('-' * 32)
    .writes(f'{k}: {v!s}\n' for k, v in user.items())
    .writeline('-' * 32)
)
```

C++ 风格的流式输入输出示例：

```python :line-numbers
from sys import stdout
from datetime import date
from zeraora.string import StringBuilder

user = dict(
    name='Tighnari',
    rank=5,
    title='浅蔚轻行',
    birth=date(2022, 12, 29),
)
builder = StringBuilder()
builder << 'User Info\n'
builder << '-' * 32 << '\n'
for k, v in user.items():
    builder << k << ': ' << v << '\n'
builder << '-' * 32 << '\n'
builder >> stdout
```

> [!TIP] 对于 C++ 开发者
> 与 C++ 的 `std::stringstream` 不同，StringBuilder 的 `>>`
> 不用于 **解析** 字符串，而用于 **提取** 构建的字符串。

以上两个示例是等价的，打印结果都是：

```text
User Info
--------------------------------
name: Tighnari
rank: 5
title: 浅蔚轻行
birth: 2022-12-29
--------------------------------
```

### C++ 风格输入 {#StringBuilder-CPP-Input}

```python
builder = StringBuilder()
builder << 'Hello, world.'
```

被插入的内容会调用内置函数 `str()` 进行转换。运算结果（即返回值）是 StringBuilder 对象自身。

### C++ 风格输出 {#StringBuilder-CPP-Output}

```python
from sys import stdout

builder = StringBuilder('Hello, world.')
builder >> stdout
```

可以传入任何支持 `.write(str)` 方法的对象。运算结果（即返回值）是 StringBuilder 对象自身。

### 转换为字符串 {#StringBuilder.str}

```python
class StringBuilder:
    def __str__(self) -> str:
```

等价于 [`self.build()`](#StringBuilder.build)。内置函数 `print()`
与日志系统的 Logger 都支持这个协议，可以将 StringBuilder
对象作为参数直接传入，它们会自动调用 `self.__str__()` 得到构建的字符串。

### write 方法 {#StringBuilder.write}

```python
class StringBuilder:
    def write(self, *blocks, sep='', end='') -> Self:
```

追加字符串到末尾。

- _blocks_ 中的每一个元素都会调用一次内置函数 `str()` 才会插入构建的字符串中。
- _sep_ 是间隔符，用于分隔 _blocks_ 中的每一个元素。
- _end_ 是最后插入的字符串。

### writeline 方法 {#StringBuilder.writeline}

```python
class StringBuilder:
    def writeline(self, *blocks, sep='', end='\n') -> Self:
```

追加**单行**字符串到末尾。

- _blocks_ 中的每一个元素都会调用一次内置函数 `str()` 才会插入构建的字符串中。
- _sep_ 是间隔符，用于分隔 _blocks_ 中的每一个元素。
- _end_ 是最后插入的字符串，默认是 `\n`。

### writelines 方法 {#StringBuilder.writelines}

```python
class StringBuilder:
    def writelines(self, *blocks, sep='\n', end='\n') -> Self:
```

追加**多行**字符串到末尾。

- _blocks_ 中的每一个元素都会调用一次内置函数 `str()` 才会插入构建的字符串中。
- _sep_ 是间隔符，用于分隔 _blocks_ 中的每一个元素，默认是 `\n`。
- _end_ 是最后插入的字符串，默认是 `\n`。

### writes 方法 {#StringBuilder.writes}

```python
class StringBuilder:
    def writes(self, iterable) -> Self:
```

从可迭代对象中提取并追加字符串。

_iterable_ 迭代出的每一个元素都会调用一次内置函数 `str()` 进行转换。

### build 方法 {#StringBuilder.build}

```python
class StringBuilder:
    def build(self) -> str:
```

将所有内容构建为一个字符串。

这个方法会保留内部缓存的内容，如要清掉，需要手动执行
[`self.clear()`](#StringBuilder.clear)。换句话说，构建不是一次性的，构建之后之前的内容仍然会参与构建。

StringBuilder 基本上都是只用一次就丢弃，一般情况下都不需要在意这个。

### clear 方法 {#StringBuilder.clear}

```python
class StringBuilder:
    def clear(self) -> Self:
```

清空构建器中的内容。

StringBuilder 基本上都是只用一次就丢弃，一般情况下都不需要执行这个方法。
