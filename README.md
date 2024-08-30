<div align="center">
    <p><img src="./logo.svg"/></p>
    <a href="https://docs.python.org/zh-cn/3/whatsnew/index.html"><img src="https://img.shields.io/pypi/pyversions/zeraora?logo=python&logoColor=yellow"></a>
    <a href="https://en.wikipedia.org/wiki/MIT_License"><img src="https://img.shields.io/pypi/l/Zeraora?color=purple"></a>
    <a href="https://pypi.org/project/Zeraora/"><img src="https://img.shields.io/pypi/v/zeraora?color=darkgreen"></a>
    <a href=""><img src="https://img.shields.io/pypi/dm/zeraora?color=C72777"></a>
    <a href=""><img src="https://img.shields.io/pypi/status/Zeraora"></a>
    <!--a href=""><img src="https://img.shields.io/conda/v/conda-forge/zeraora"></a-->
</div>
<div align="center">
    <i>长期维护的个人实用工具包</i>
    <br>
    <i>A personal practical utility Python package, with long time support.</i>
</div>

## 特性／Feature

- 支持 `with` 、注解和实例化三种方式调用的计时器 `BearTimer` ；
- 自动为 Django 模型生成下划线小写（即蛇形）数据表名的 `SnakeModel` ；
- 受 Django 的 `Choices` 启发和 Java 原生枚举影响的、可为枚举添加任意属性的 `Items` ；
- 允许用 `curd` 等字符简化 `ViewSet.as_view()` 参数的 `EasyViewSetMixin` ；
- 不强制依赖任何非[标准库](https://docs.python.org/zh-cn/3/library/index.html)；
- 更多……

## 安装／Installation

使用 pip 直接安装：

```shell
pip install zeraora
```

因为没有需求，所以还没有创建 conda 版。

## 兼容性／Compatibility

|       | Python                     |
|-------|----------------------------|
| 0.4.x | 3.7，3.8，3.9，3.10，3.11，3.12 |
| 0.3.x | 3.7，3.8，3.9，3.10           |
| 0.2.x | 3.7，3.8，3.9，3.10           |
| 0.1.x | 3.7，3.8，3.9，3.10           |

