<h1 align="center" style="padding-top: 32px">Zeraora</h1>

<div align="center">
    <a href="https://docs.python.org/zh-cn/3/whatsnew/index.html"><img src="https://img.shields.io/badge/Python-3.7%20%2B-blue.svg?logo=python&logoColor=yellow"></a>
    <a href="https://en.wikipedia.org/wiki/MIT_License"><img src="https://img.shields.io/badge/License-MIT-purple.svg"></a>
    <a href="https://pypi.org/project/Zeraora/"><img src="https://img.shields.io/pypi/v/zeraora?color=darkgreen&label=PyPI"></a>
    <a href=""><img src="https://img.shields.io/conda/v/conda-forge/zeraora"></a>
</div>
<div align="center">
    <i>长期维护的个人开源工具库</i>
    <br>
    <i>An utility Python package supports for my personal and company projects</i>
</div>

## 特性

- 支持with、注解和实例化三种方式调用的计时器 [`BearTimer`](https://github.com/aixcyi/zeraora/blob/master/docs/zeraora/BearTimer.md) ；
- 生成通用representation方便调试时查看对象内部信息的 [`ReprMixin`](https://github.com/aixcyi/zeraora/blob/master/docs/zeraora/ReprMixin.md) ；
- 将字典的任意层级递归转化为对象，以便支持点分法访问数据的 [`OnionObject`](https://github.com/aixcyi/zeraora/blob/master/docs/zeraora/OnionObject.md) ；
- 受 Django 的 `Choices` 启发的、可为枚举添加任意属性的 `Items` ；
- 用以简化 `.as_view()` 传参的 `EasyViewSetMixin` ；
- 仿照 `DestroyModelMixin` 实现的 `SoftDeleteModelMixin` ；
- 安全转换快捷函数 `safecast()` 和链式调用安全转换的 `SafeCast` ；
- 不强制依赖任何非[标准库](https://docs.python.org/zh-cn/3/library/index.html)；
- 更多……

## 安装

使用 pip 直接安装：

```shell
pip install zeraora
```

临时通过本地代理使用 pip 安装：

```shell
pip install zeraora --proxy=127.0.0.1:6666
```

使用 pip 时临时指定安装源来安装：

```shell
pip install zeraora -i http://pypi.mirrors.ustc.edu.cn/simple/
```

## 文档

见[全局符号索引](https://github.com/aixcyi/zeraora/blob/master/docs/README.md)或源码中的[类型标注](https://docs.python.org/zh-cn/3/glossary.html#term-type-hint)和[reStructuredText](https://zh.wikipedia.org/wiki/ReStructuredText)格式的[文档字符串](https://docs.python.org/zh-cn/3/glossary.html#term-docstring)。

## 版本

|      | 状态[^1] | 支持时间 | 兼容   | 依赖              |
| ---- | -------- | -------- | ------ | ----------------- |
| v0.3 | 🆕feature | 长期     | -      | Python 3.7 或更新 |
| v0.2 | ✅bugfix  | 长期     | v0.1.x | Python 3.7 或更新 |
| v0.1 | ❌EOL     | 不再支持 | -      | Python 3.7 或更新 |

[^1]: 概念参见[Python版本状态](https://devguide.python.org/versions/#status-key)。

## 内部架构

对于不依赖任何第三方库的符号，按照功能划分内部包，但会统一公开在 `zeraora` 这个顶层包中。  
对于依赖第三方库的符号，会以依赖库为包名划分一级公开包，然后按照功能划分二级内部包，最后统一公开在上一级包中。  
统一存放是为了规避内部包结构改动带来的影响。

对外公开的包结构如下：

- `zeraora`
  - `constants`
  - `dj`
  - `drf`

实际文件结构大致如下：

- `zeraora`
  - `constants`
    - `charsets`
    - `division`
  - `dj`
    - `models`
    - ……
  - `drf`
    - `viewsets`
    - ……
- `converters`
- `generators`
- `utils`
- ……
