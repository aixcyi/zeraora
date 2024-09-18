<div align="center">
    <p><img src="./logo.svg"/></p>
    <a href="https://docs.python.org/zh-cn/3/whatsnew/index.html"><img src="https://img.shields.io/pypi/pyversions/zeraora?logo=python&logoColor=yellow"></a>
    <a href="https://pypi.org/project/Zeraora/"><img src="https://img.shields.io/pypi/v/zeraora?color=darkgreen"></a>
    <a href=""><img src="https://img.shields.io/conda/v/conda-forge/zeraora"></a>
    <a href=""><img src="https://img.shields.io/pypi/status/Zeraora"></a>
    <a href=""><img src="https://img.shields.io/pypi/dm/zeraora?color=C72777"></a>
</div>
<div align="center">
    <i>长期维护的个人实用工具包</i>
    <br>
    <i>A personal practical utility Python package, with long time support.</i>
</div>

## 特性／Features

- 支持 `with`、注解和实例化三种方式调用的计时器 `BearTimer` ；
- 自动为 Django 模型生成下划线小写（即蛇形）数据表名的 `SnakeModel` ；
- 受 Django 的 `Choices` 启发和 Java 原生枚举影响的、可为枚举添加任意属性的 `Items` ；
- 允许用 `curd` 等字符简化 `ViewSet.as_view()` 参数的 `EasyViewSetMixin` ；
- 继承标准库 `datetime` 的增强型日期时间对象 `Datetime` ；
- 不强制依赖任何非[标准库](https://docs.python.org/zh-cn/3/library/index.html)；
- 更多……

## 安装／Install

使用 pip 直接安装：

```shell
pip install zeraora
```

安装最新的版本（预发布）

```shell
pip install zeraora --pre
```

或者移步 PyPI 在
[Release history](https://pypi.org/project/Zeraora/#history)
选定版本后 Download files 手动下载 .whl 文件并安装

```shell
pip install ./Zeraora-0.4.0.0a-none-any.whl
```

因为暂时没有需求，所以还没创建 conda 版。

## 兼容／Compatibility

> - 每个 0.x 之间并不兼容，请务必选择最新的发布版。
> - 依赖包版本仅考虑单独依赖时的情况。

- Zeraora 0.4.x
  - [Python](https://www.python.org/) 3.7｜3.8｜3.9｜3.10｜3.11｜3.12
  - [Django](https://www.djangoproject.com/) 2.x｜3.x｜4.x｜5.0
  - [Django REST Framework](https://www.django-rest-framework.org/) 2.3.0+
  - [requests](https://requests.readthedocs.io/) 0.8.3+

| Zeraora | Python                     |
|---------|----------------------------|
| 0.4.x   | 3.7，3.8，3.9，3.10，3.11，3.12 |
| 0.3.x   | 3.7，3.8，3.9，3.10           |
| 0.2.x   | 3.7，3.8，3.9，3.10           |
| 0.1.x   | 3.7，3.8，3.9，3.10           |

## 文档／Document

参见 [Wiki](https://github.com/aixcyi/zeraora/wiki)

## 链接／Links

- GitHub [Discussions](https://github.com/aixcyi/zeraora/discussions)
- QQ群 [418751161](https://qm.qq.com/q/ou4RdUFMTm)
- GitHub [Issues](https://github.com/aixcyi/zeraora/issues)
- 码云 [Issues](https://gitee.com/aixcyi/zeraora/issues)
