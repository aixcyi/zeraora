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
    <i>实际应用积累的长期维护的个人开源工具库</i>
    <br>
    <i>A utility Python package for my personal and corporate projects, with long time support</i>
</div>

## 特性

- 支持with、注解和实例化三种方式调用的计时器 `BearTimer` ；
- 生成通用representation方便调试时查看对象内部信息的 `ReprMixin` ；
- 将字典的任意层级递归转化为对象，以便支持点分法访问数据的 `OnionObject` ；
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

见[全局符号索引](./docs/README.md)。

## 版本

|      | 状态[^1] | 支持时间 | 依赖              | 备注                                       |
| ---- | -------- | -------- | ----------------- | ------------------------------------------ |
| v0.3 | 🆕feature | 长期     | Python 3.7 或更新 | 趋于稳定，但改了包结构，不向下兼容。       |
| v0.2 | ✅bugfix  | 长期     | Python 3.7 或更新 | 探索包结构，完善核心特性，补充非核心特性。 |
| v0.1 | ❌EOL     | 不再支持 | Python 3.7 或更新 | 试验自动部署，只有核心特性。               |

[^1]: 概念参见[Python版本状态](https://devguide.python.org/versions/#status-key)。

## 分支

主分支将从名为 `master` 的分支切换为 `main` 并且前者将于2023年6月12日删除（自动同步不好做所以躺平了），原因是后者听起来确实比前者要舒服一点点，若要深究的话参见[这里](https://stackoverflow.com/a/65021103)。

## 帮助

目前已经趋于稳定，部署生产环境时请优先考虑0.3.x，或更新到0.2.x最新子版本。如有需要，请优先通过 Issue 或 Pull Request 、其次通过QQ群 699090940 来反馈问题、提出创意或协助修复漏洞。
