<h1 align="center" style="padding-top: 32px">Zeraora</h1>

<div align="center"><i>长期维护的个人开源工具库<br>An original utility Python package with LTS supports for my personal and company projects</i></div>

## Description

[![Python](https://img.shields.io/badge/Python-3.7%20%2B-blue.svg?logo=python&logoColor=yellow)](https://docs.python.org/zh-cn/3/whatsnew/index.html) [![License](https://img.shields.io/badge/License-MIT-purple.svg)](https://en.wikipedia.org/wiki/MIT_License) ![PyPI](https://img.shields.io/pypi/v/zeraora) ![conda](https://img.shields.io/conda/v/conda-forge/zeraora)

解决在不同项目、不同环境之间快速使用自己编写的工具类及快捷函数的痛点。

## Usage

可以使用 pip 直接安装：

```shell
pip install zeraora
```

未来将发布到 Anaconda Cloud，以便使用 conda 安装：

```shell
conda install zeraora
```

不能保证所有工具类和快捷函数自始至终都放在同一个子包，因此应该像这样直接导入：

```python
from zeraora import BearTimer

with BearTimer() as bear:
    summary = 0
    for i in range(1000000):
        bear.step(f'loop to {i} now.')
        summary += i
```

亦或者像这样导入：

```python
import zeraora

with BearTimer.BearTimer() as bear:
    summary = 0
    for i in range(1000000):
        bear.step(f'loop to {i} now.')
        summary += i
```

但对于 `charsets` 可以放心从子包导入：

```python
from random import choices
from zeraora.charsets import BASE64

def make_pwd(length: int) -> str:
    return ''.join(choices(BASE64, k=length))

if __name__ == '__main__':
    [
        print(make_pwd(16)) for _ in range(20)
    ]
```

## Compatibility

[Python 3.7](https://docs.python.org/zh-cn/3/whatsnew/3.7.html#summary-release-highlights) 开始 `dict` 正式按照插入顺序存储，考虑到 `dict` 是 Python 的基石，跨越这个版本保证的兼容性的代码可能会存在不易察觉的错误，因此将该版本定为兼容下限。这也是我接触过的项目中的最低运行版本，故而不太希望维护对更低版本的兼容。

## Change

此处仅列出不兼容旧版的修改，其余变动见git历史。

暂无。

## APIs

> 一个成熟的IDE应该学会自己生成文档~

