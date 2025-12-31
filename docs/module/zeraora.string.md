---
title: "`string` — 字符集与字符串"
outline: deep
excerpt:
---

# <pre>zeraora.string</pre>

此模块定义了一些字符集常量，以及生成字符串的工具类。

## `Alphabet`

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

> [!IMPORTANT] 注意
> 上表的种类出现顺序 **不代表** 实际常量值中的字符顺序。

## `Notation`

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

## `Char`

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

## `StringBuilder(*blocks, sep='', end='')`

字符串构建器。  
用于一次性聚合多个短小字符串，来构建一个较长的字符串。支持链式调用与 C++ 风格的流式输入输出。

### `write(*blocks, sep='', end='')` {#StringBuilder.write}

追加字符串到末尾。

### `writeline(*blocks, sep='', end='\n')` {#StringBuilder.writeline}

追加**单行**字符串到末尾。

### `writelines(*blocks, sep='\n', end='\n')` {#StringBuilder.writelines}

追加**多行**字符串到末尾。

参数 _blocks_ 是要追加的字符串，参数 _sep_ 是分隔每个 _blocks_ 的分隔符，参数 _end_ 是最后追加的字符串。所有参数都将会转换为
`str` 类型。

```python
from zeraora.string import StringBuilder

print(
    StringBuilder('User Info', end='\n')
    .writeline('=' * 32)
    .write('Tighnari', end=' ')
    .writeline('-' * 23)
    .writelines(
        'rank: 5',
        'title: 浅蔚轻行',
        'birth: 12月29日',
    )
    .writeline('=' * 32)
)
```

```text
User Info
================================
Tighnari -----------------------
rank: 5
title: 浅蔚轻行
birth: 12月29日
================================
```

### `writes(iterable)` {#StringBuilder.writes}

从可迭代对象中提取并追加字符串。

参数 _iterable_ 迭代出的所有元素都将会转换到 `str` 类型。

```python
from datetime import date
from zeraora.string import StringBuilder

user = dict(
    name='Tighnari',
    rank=5,
    title='浅蔚轻行',
    birth=date(2022, 12, 29),
)
print(
    StringBuilder('User Info', end='\n')
    .writeline('-' * 32)
    .writes(f'{k}: {v!s}\n' for k, v in user.items())
    .writeline('-' * 32)
)
```

```text
User Info
--------------------------------
name: Tighnari
rank: 5
title: 浅蔚轻行
birth: 2022-12-29
--------------------------------
```

### `__str__()` {#StringBuilder.str}

构建最终的字符串。

内置的 `print()` 与日志系统的 `Logger()` 都会默认执行 `str(StringBuilder())`。稍微注意一下，这种方式并不会清空内部的缓存。

### `build()` {#StringBuilder.build}

构建最终的字符串，并清空构建器内部的缓存。

此方法用于解决需要复用空的构建器对象的情况。下面展示了不清除缓存与清除缓存两种方式并用的后果：

```python
from zeraora.string import StringBuilder

builder = StringBuilder()
print(builder.writeline('[INFO] Hello, I am Tighnari.'), end='')
print(builder.writeline('[WARN] 重复打印了').build(), end='')
print(builder.writeline('[INFO] 你好，我叫提纳里！').build(), end='')
```

```text
[INFO] Hello, I am Tighnari.
[INFO] Hello, I am Tighnari.
[WARN] 重复打印了
[INFO] 你好，我叫提纳里！
```

### 流式输入

模仿 C++ 风格使用 Python 的 `<<` 运算符可以实现流式输入。

```python
from zeraora.string import StringBuilder

endl = '\n'
builder = StringBuilder()
builder << '你好，我叫提纳里！' << endl
builder << 'Hello, I am Klee.'
print(builder)
```

```text
你好，我叫提纳里！
Hello, I am Klee.
```

### 流式输出

模仿 C++ 风格使用 Python 的 `>>` 运算符可以实现流式输出，输出到的所有对象都必须已经实现 `write()` 方法。

```python
from sys import stdout
from zeraora.string import StringBuilder

endl = '\n'
builder = StringBuilder()
builder << '你好，我叫提纳里！' << endl
builder >> stdout
```

```text
你好，我叫提纳里！
```

<style scoped>
th, td {
    text-wrap: nowrap;
}
</style>
