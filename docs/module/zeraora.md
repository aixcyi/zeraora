---
title: "`__init__`"
excerpt:
---

# <pre>zeraora</pre>

## `__version__`

一个表示 Zeraora 版本号的字符串，格式符合[Python 版本风格](https://packaging.python.org/en/latest/specifications/version-specifiers/)。

## `VERSION`

一个表示 Zeraora 版本号的具名元组，与标准库 sys 的
[`version_info`](https://docs.python.org/zh-cn/3/library/sys.html#sys.version_info)
一样包含 _major_、_minor_、_micro_、_serial_
四个非负整数字段和 _releaselevel_ 一个字符串字段。

| 下标 |   [0]   |   [1]   |   [2]   |             [3]              |   [4]    |
|:--:|:-------:|:-------:|:-------:|:----------------------------:|:--------:|
| 字段 | _major_ | _minor_ | _micro_ |           _level_            | _serial_ |
| 类型 |  `int`  |  `int`  |  `int`  |            `str`             |  `int`   |
| 别名 |         |         |         |        _releaselevel_        |          |
| 取值 | [0,256) | [0,256) | [0,256) | `alpha`<br>`beta`<br>`final` |  [0,16)  |

因为是一个元组，所以你完全可以像 `(0,3) <= zeraora.VERSION < (0,4)`
这样判断和比较版本号。

> [!NOTE] 替代品
> 如果你也需要一个类似的结构来表示自己的版本号，可以考虑第三方库
> [packaging](https://pypi.org/project/packaging/) 的
> [`Version`](https://packaging.pypa.io/en/stable/version.html#packaging.version.Version)
> 类。

另外，`zeraora.VERSION` 还有一个属性 `.is_final` 用于判断是不是最终版本，不过
packaging 包的 `Version` 类中没有叫这个的属性。

> [!WARNING] 在 0.4 版本发生改变
> 以前是一个仅保证有 _major_ 和 _minor_ 两个元素的 `tuple`，现在是一个具名元组。
