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
- 安全转换的 `casting()` 和链式调用安全转换的 `Cast` ；
- 用以简化 `.as_view()` 传参的 `EasyViewSetMixin` ；
- 仿照 `DestroyModelMixin` 实现的 `SoftDeleteModelMixin` ；
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

部分文档以Markdown格式存放在docs目录下，查看该目录下的 [README.md](https://github.com/aixcyi/zeraora/blob/master/docs/README.md) 可以浏览全局公开符号的索引。

源代码多数附带[类型标注](https://docs.python.org/zh-cn/3/glossary.html#term-type-hint)和[文档字符串](https://docs.python.org/zh-cn/3/glossary.html#term-docstring)（[reStructuredText](https://zh.wikipedia.org/wiki/ReStructuredText)格式），文档未尽事宜请移步源代码浏览。

## 兼容性

[Python 3.7](https://docs.python.org/zh-cn/3/whatsnew/3.7.html#summary-release-highlights) 开始 `dict` 正式按照插入顺序存储，考虑到 `dict` 是 Python 的基石，为了避免出现难以察觉的错误，因而将该版本定为兼容下限。这也是我接触过的项目中的最低运行版本，故而不太希望维护对更低版本的兼容。

项目会尽力保证向后兼容性，但还是建议在requirements中写明特定的版本号，避免因为版本更新或回退而出现棘手的错误。

## 更新

> 仅列出不兼容旧版的修改，其余变动见git历史。

### 0.2.7（2023-5-09）

- 快捷函数 `casting` 更名为 `safecast` ，调用参数一致。
- 更改了内部结构，导致使用了 `ReprMixin` 的 Django 模型的迁移文件（migration）中 `CreateModel` 的 `base` 参数传入了错误值。点击[这里](https://github.com/aixcyi/zeraora/blob/master/docs/zeraora/ReprMixin.md)查看解决方案。

### 0.2.5（2023-5-02）

- `OnionObject.__repr__()` 不再进行嵌套递归，因为在调试模式中可以展开嵌套，在此递归并无意义。现在OnionObject对象内的OnionObject对象在 `repr()` 后会显示为 `OnionObject(...)` 。
- 去除 `OnionObject.__str__()` 方法，可以用 `import json` 后 `json.dumps(OnionObject())` 实现原来的效果。
- 更改 `BearTimer` 的默认打印格式。
- 将 `BearTimer.output()` 拆分为负责准备打印的 `record()` 和实现打印的 `handle()` 。

### 0.2.0（2023-4-12）

- 将递归转化的 `JSONObject` 与仅表层转化的 `JsonObject` 合并为 `OnionObject` ，并删去前述两个类。

