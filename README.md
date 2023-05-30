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

## 特点

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

见[全局符号索引](https://github.com/aixcyi/zeraora/blob/master/docs/README.md)（Markdown格式）或源码中的[类型标注](https://docs.python.org/zh-cn/3/glossary.html#term-type-hint)和[文档字符串](https://docs.python.org/zh-cn/3/glossary.html#term-docstring)（[reStructuredText](https://zh.wikipedia.org/wiki/ReStructuredText)格式）。

## 版本

|        | 状态[^1] | 安全版本[^2] | 最新版本 | 最后支持 | 兼容[^3]    |
| ------ | -------- | ------------ | -------- | -------- | ----------- |
| v0.3.x | 🆕feature | 未发布       | 未发布   | -        | Python 3.7+ |
| v0.2.x | ✅bugfix  | v0.2.12      | v0.2.12  | 长期     | Python 3.7+ |
| v0.1.x | ❌EOL     | v0.1.1       | v0.1.1   | 不再支持 | Python 3.7+ |

[^1]: 概念参见[Python版本状态](https://devguide.python.org/versions/)。
[^2]: 指这个版本开始从prerelease转为bugfix，不再包含不兼容改动。
[^3]: 指Python版本需要大于或等于某个版本。

## 兼容性

高情商：[Python 3.7](https://docs.python.org/zh-cn/3/whatsnew/3.7.html#summary-release-highlights) 是本项目开始时的最后一个安全版本，因而将该版本定为兼容下限。  
低情商：这是我接触过的最低运行版本。

~~项目会尽力保证向后兼容性，但还是~~建议在requirements中写明特定的版本号，避免因为版本更新或回退而出现棘手的错误。

