<h1 align="center" style="padding-top: 32px">Zeraora</h1>

<div align="center">
    <a href="https://docs.python.org/zh-cn/3/whatsnew/index.html"><img src="https://img.shields.io/pypi/pyversions/zeraora?logo=python&logoColor=yellow"></a>
    <a href="https://en.wikipedia.org/wiki/MIT_License"><img src="https://img.shields.io/pypi/l/Zeraora?color=purple"></a>
    <a href="https://pypi.org/project/Zeraora/"><img src="https://img.shields.io/pypi/v/zeraora?color=darkgreen"></a>
    <a href=""><img src="https://img.shields.io/pypi/dm/zeraora?color=C72777"></a>
    <a href=""><img src="https://img.shields.io/pypi/status/Zeraora"></a>
    <!--a href=""><img src="https://img.shields.io/conda/v/conda-forge/zeraora"></a-->
</div>
<div align="center">
    <i>实用至上的个人工具库</i>
    <br>
    <i>Personal utility Python package for my projects, with long time support</i>
</div>

## 特性

- 支持with、注解和实例化三种方式调用的计时器 `BearTimer` ；
- 自动为Django模型生成下划线小写（即蛇形）数据表名的 `SnakeModel` ；
- 将字典的任意层级递归转化为对象，以便支持点分法访问数据的 `JSONObject` ；
- 受 Django 的 `Choices` 启发和 Java 原生枚举影响的、可为枚举添加任意属性的 `Items` ；
- 基于 `Items` 的包含34个省级行政区名称、区划代码、字母码、大区、简称、缩写的枚举 `Province` ；
- 允许用 curd 等字符简化 `ViewSet.as_view()` 参数的 `EasyViewSetMixin` ；
- 不强制依赖任何非[标准库](https://docs.python.org/zh-cn/3/library/index.html)。

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

因为没有需求，所以还没有创建 conda 版。

## 版本

|       | 维护时间起止                      | Python                         |
|-------|-----------------------------| ------------------------------ |
| 1.x   | 2024.01.01 ~ 2025.01.01（暂定） | 3.7，3.8，3.9，3.10，3.11，3.12 |
| 0.3.x | 2023.06.09 ~ 2024.06.09     | 3.7，3.8，3.9，3.10            |
| 0.2.x | 2023.04.12 ~ 2024.04.12     | 3.7，3.8，3.9，3.10            |
| 0.1.x | 2023.03.27 ~ 2023.06.09     | 3.7，3.8，3.9，3.10            |

