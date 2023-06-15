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
    <i>实际应用积累的长期维护的实用开源工具库</i>
    <br>
    <i>A utility Python package for our personal and corporate projects, with long time support</i>
</div>


## 特性

- 支持with、注解和实例化三种方式调用的计时器 `BearTimer` ；
- 生成通用representation方便调试时查看对象内部信息的 `ReprMixin` ；
- 将字典的任意层级递归转化为对象，以便支持点分法访问数据的 `OnionObject` ；
- 受 Django 的 `Choices` 和 Java 原生枚举语法启发的、可为枚举添加任意属性的 `Items` ；
- 用以简化 `.as_view()` 传参的 `EasyViewSetMixin` ；
- 仿照 `DestroyModelMixin` 实现的 `SoftDeleteModelMixin` ；
- 自动为Django模型生成下划线小写（即蛇形）数据表名的 `SnakeModel` ；
- 包含34个省级行政区名称、区划代码、字母码、大区、简称、缩写的枚举 `Province` ；
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

见[全局符号索引](./docs/README.md)。

## 版本

|       | 状态[^1] | 维护时间 | 依赖[^2]          | 备注                                                         |
| ----- | -------- | -------- | ----------------- | ------------------------------------------------------------ |
| 0.3.x | 🆕feature | 长期     | Python 3.7 或更新 | **分支**：main<br/>趋于稳定，但改了包结构，没办法向下兼容。  |
| 0.2.x | ✅bugfix  | 长期     | Python 3.7 或更新 | **分支**：0.2.x<br/>探索包结构，完善核心特性，补充非核心特性。 |
| 0.1.x | ❌EOL     | 不再维护 | Python 3.7 或更新 | **分支**：release/*<br/>试验自动部署，只有核心特性。         |

[^1]: 概念参见[Python版本状态](https://devguide.python.org/versions/#status-key)。
[^2]: 仅在最低依赖版本中进行(过)单元测试。

## 分支

主分支将从名为 `master` 的分支切换为 `main` 并且于2023年6月12日删除前者（自动同步不好做所以躺平了），原因是 `main` 听起来确实比前者要舒服一点点，若要深究的话参见[这里](https://stackoverflow.com/a/65021103)。两条分支是完全一致的，换句话说，后续的更新**就是**在 `master` 基础上进行的。

## 帮助

这个包偏向于抽象及封装一些实际在用的实用功能，目前整体趋于稳定，如需部署生产环境，请优先考虑 0.3.x 或后续更新的版本。

欢迎通过 Issue 或 Pull Request 来提出功能创意、命名建议，亦或反馈问题、修复漏洞、编写测试等等等等；如有需要，可以进入QQ群 699090940 获取帮助。
