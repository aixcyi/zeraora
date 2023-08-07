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
    <i>一个纯粹的工具库，为跨平台跨项目复用代码而开发</i>
    <br>
    <i>A utility Python package for our personal and corporate projects, with long time support</i>
</div>




## 特性

- 支持with、注解和实例化三种方式调用的计时器 `BearTimer` ；
- 生成通用representation方便调试时查看对象内部信息的 `ReprMixin` ；
- 自动为Django模型生成下划线小写（即蛇形）数据表名的 `SnakeModel` ；
- 将字典的任意层级递归转化为对象，以便支持点分法访问数据的 `OnionObject` ；
- 受 Django 的 `Choices` 启发和 Java 原生枚举影响的、可为枚举添加任意属性的 `Items` ；
- 基于 `Items` 的包含34个省级行政区名称、区划代码、字母码、大区、简称、缩写的枚举 `Province` ；
- 不强制依赖任何非[标准库](https://docs.python.org/zh-cn/3/library/index.html)；
- 更多符号见[Zeraora全局符号索引](./docs/README.md)。

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

|       | 状态      | 首版时间   | 安全版本自 | 结束维护于 | Python |
| ----- | --------- | ---------- | ---------- | ---------- | ------ |
| 0.3.x | 🆕feature  | 2023.06.09 | -          | ~ 0.5.x    | >=3.7  |
| 0.2.x | ✅security | 2023.04.12 | 0.2.14     | ~ 0.4.x    | >=3.7  |
| 0.1.x | ❌EOL      | 2023.03.27 | -          | 2023.06.09 | >=3.7  |

#### 状态

- feature 处于新增和测试的阶段。更新或回退子版本可能会出现兼容性问题。
- security 处于功能稳定的阶段。在标记为安全的子版本之间切换不会出现兼容性问题；会为问题修复发布新的子版本，但不会迁移新版功能。
- EOL 处于停止维护的阶段。不会处理与之相关的任何问题，也不会发布新的子版本。


## 文档

详见[全局符号索引](./docs/README.md)。

## 开发

这个库只是为了跨平台、跨项目复用代码而已。有些是直接封装实际在用的功能，有些是在库里开发然后通过pip依赖传递给各个项目，有些可能真的只是奇思妙想灵光乍现。如果你有同样的需求，也认可这份努力，那么欢迎加入。

详见[开发指南](./CONTRIBUTING.md)。

## 帮助

可以通过 Issue 反馈，或通过 Pull Request 添加你的工具；如有需要，可以进入QQ群 699090940 获取非即时性的帮助。
