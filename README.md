<h1 align="center" style="padding-top: 32px">Zeraora</h1>

<div align="center"><i>包含了个人及公司项目中原创且可公开的工具类及快捷函数的工具库<br>A original utility Python package supports for my personal and company's projects</i></div>

## Description

[![Python](https://img.shields.io/badge/Python-3.7%20%2B-blue.svg?logo=python&logoColor=yellow)](https://docs.python.org/zh-cn/3/whatsnew/index.html) [![PyPI](https://img.shields.io/badge/PyPI-unreleased-blue.svg)]((https://pypi.org)) [![License](https://img.shields.io/badge/License-MIT-purple.svg)](https://en.wikipedia.org/wiki/MIT_License)

项目初衷是解决在不同项目、不同环境之间快速使用自己编写的工具类及快捷函数的痛点。

## Compatibility

[Python 3.7](https://docs.python.org/zh-cn/3/whatsnew/3.7.html#summary-release-highlights) 开始 `dict` 正式按照插入顺序存储，考虑到 `dict` 是 Python 的基石，跨越这个版本保证的兼容性的代码可能会存在不易察觉的错误，因此将该版本定为兼容下限。这也是我接触过的项目中的最低运行版本，故而不太希望维护对更低版本的兼容。

作为一个纯工具库，Zeraora不会声明依赖任何包，避免污染项目环境，更重要的一点是不是所有功能都依赖第三方包。因此如果遇到 `ModuleNotFoundError` 或 `ImportError` ，请阅读docstring或浏览**源代码**以确定需要安装哪些包。

不建议在生产环境上使用此包，哪怕它本身已经应用到作者经历过的其它生产环境；如若实在需要，**强烈建议**您阅读一遍用到的功能的源代码，并在 `requirements.txt` 中指定**具体的**版本号，以尽最大可能避免出现兼容性问题。

## Usage

可以使用 pip 直接安装：

```shell
pip install zeraora
```

未来计划打包到 Anaconda Cloud，以便使用 conda 安装：

```shell
conda install zeraora
```

## Change

此处仅列出不兼容旧版的修改，其余变动见git历史。

暂无。

## APIs

> 一个成熟的IDE应该学会自己生成文档~

