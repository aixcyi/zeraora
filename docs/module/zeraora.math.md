---
title: "`math` — 数学计算与常量"
excerpt:
---

# <pre>zeraora.math</pre>

此模块提供了二进制小数、十进制小数、进位制相关的函数与常量。

## `bitstream(integer)`

获取一个整数 _integer_ 的所有比特位，以生成器的方式从 **低位** 到 **高位** 返回。

```python
from zeraora.math import bitstream

print(list(bitstream(67)))
# [1, 2, 64]

print(list(bitstream(-43)))
# [-1, -2, -8, -32]

print(list(bitstream(0)))
# []
```

## `digitstream(integer, base)`

获取一个非负整数 _integer_ 在 _base_ 进制下的各位数码，以生成器的方式从 **低位** 到 **高位** 返回。

> [!TIP]
> 1. 每一个数码都以十进制表达，需要另外使用字符集进行转换。
> 2. 生成器无法直接反转顺序，建议调用者处理好生成结果后再取出对象、进行反转。

```python
from zeraora.math import digitstream

digits = digitstream(1008612, 16)
mapper = '0123456789abcdef'.__getitem__
print(''.join(map(mapper, digits))[::-1])
# 'f63e4'
print(hex(1008612))
# '0xf63e4'
```

## `remove_exponent(d)`

去除十进制小数的尾导零。

此函数摘录自
[Decimal 常见问题](https://docs.python.org/zh-cn/3/library/decimal.html#decimal-faq)，仅出于方便使用而摘录。

## `decimalize(d, max_digits=12, decimal_places=2)`

将小数（不含小数点）的总长度控制在 _max_digits_ 位，小数位数控制在 _decimal_places_
位，多余的小数部分将被直接丢弃，不会执行舍入。参数
_d_ 支持传入 `str`、`int`、`float` 或
[`Decimal`](https://docs.python.org/zh-cn/3/library/decimal.html#decimal-objects)
对象。
