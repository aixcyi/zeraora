---
prev: false
next: false
editLink: false
lastUpdated: false
titleTemplate: false
title: Zeraora
aside: false
sidebar: false
outline: false
excerpt:
---

<div>
    <p style="display: flex; justify-content: center">
        <img alt="Zeraora logo" draggable="false" src="/logo.svg" style="user-select: none" />
    </p>
    <p style="display: flex; flex-wrap: wrap; gap: .5rem; justify-content: center">
        <a draggable="false" href="https://docs.python.org/zh-cn/3/whatsnew/index.html">
            <img alt="Python 兼容性"
                 draggable="false"
                 src="https://img.shields.io/pypi/pyversions/zeraora?logo=python&logoColor=yellow"
                 style="user-select: none" />
        </a>
        <a draggable="false" href="https://pypi.org/project/Zeraora/">
            <img alt="PyPI 版本号"
                 draggable="false"
                 src="https://img.shields.io/pypi/v/zeraora?color=darkgreen"
                 style="user-select: none" />
        </a>
        <a draggable="false" href="">
            <img alt="PyPI 包状态"
                 draggable="false"
                 src="https://img.shields.io/pypi/status/Zeraora"
                 style="user-select: none" />
        </a>
        <a draggable="false" href="">
            <img alt="每月下载量"
                 draggable="false"
                 src="https://img.shields.io/pypi/dm/zeraora?color=C72777"
                 style="user-select: none" />
        </a>
    </p>
    <p style="text-align: center">
        <i>电猫工具包，快如电，轻如喵</i>
        <br />
        <i>Zeraora lightweight collection of utilities that save your dev time.</i>
    </p>
</div>

## 简介 {#intro}

一个 Python 工具包，包含一堆杂七杂八的工具，大部分都是从个人与公司项目提取、封装、抽象的，希望能帮你少写几行代码。

- [<pre>zeraora.conf</pre>](/module/zeraora.conf)，配置辅助工具。
- [<pre>zeraora.django</pre>](/module/zeraora.django)，对经典 Web 框架 [Django](https://docs.djangoproject.com/zh-hans/5.2/) 的扩展和增强。
- [<pre>zeraora.drf</pre>](/module/zeraora.drf)，对 RESTful API 框架 [Django REST Framework](https://www.django-rest-framework.org/) 的扩展和增强。
- [<pre>zeraora.math</pre>](/module/zeraora.math)，数学计算与常量。
- [<pre>zeraora.requests</pre>](/module/zeraora.requests)，对 [Requests](https://requests.readthedocs.io/en/latest/) 的扩展和增强。
- [<pre>zeraora.string</pre>](/module/zeraora.string)，字符集常量，与字符串生成。
- [<pre>zeraora.time</pre>](/module/zeraora.time)，时间与计时。
- [<pre>zeraora.uuid</pre>](/module/zeraora.uuid)，UUID 生成函数。

优点：除了 [typing_extensions](https://typing-extensions.readthedocs.io/en/latest/)
用来兼容类型提示外，它**不强制依赖**任何第三方库。  
缺点：优点太少。

## 速览 {#features}

### SnakeModel

Django 默认会为以下模型生成一个名为 `wms_goodsskuinfo` 的表

```python
# ./apps/wms/models.py
from django.db import models

class GoodsSKUInfo(models.Model):
    pass
```

而借助
[SnakeModel](https://docs.navifox.net/zeraora/module/zeraora.django.html#SnakeModel)
可以自动生成为 `wms_goods_sku_info`，你只需要

```python
# ./apps/wms/models.py
from django.db import models
from zeraora.django import SnakeModel

class GoodsSKUInfo(models.Model, metaclass=SnakeModel):
    pass
```

### Configuration

在找一个具有类型提示的、能被 IDE 自动补全字段的、不依赖文件的、超轻量的 ORM？来试试
[Configuration](https://docs.navifox.net/zeraora/module/zeraora.conf.html#Configuration) 吧。

```python
# ./apps/wms/models.py
from django.db import models
from zeraora.conf import Configuration


class Store(models.Model):
    ...
    configuration = models.JSONField(default=dict)


class StoreConfiguration(Configuration):
    VERSION = 1

    def __init__(self, __store: Store):
        self.enableStorehouse = False
        """启用仓库管理服务？"""
        self.minSaleableStock = 1
        """最低可售库存量。"""
        super().__init__(store.configuration or dict())
        self._store_ = __store

    def fill(self, save=True, *args, **kwargs):
        __store = self._store_
        __store.configuration = self.dump()
        if save:
            __store.save()
        return self


store = Store.objects.get(id=1)
store.configuration = {
    "enableStorehouse": True,
}
configs = StoreConfiguration(store)
print(configs.enableStorehouse)  # True
print(configs.minSaleableStock)  # 1
```

### BearStopwatch

想要一个代码计时器？这里有与 Python 日志系统相适配的
[BearStopwatch](https://docs.navifox.net/zeraora/module/zeraora.time.html#BearStopwatch) 。

```python
from zeraora.time import BearStopwatch

with BearStopwatch.configit() as fox:
    # 业务逻辑
    pass
```

要是是 Django 项目，可以直接在 `settings.py` 中配置：

```python
# ./my_project/settings.py
from zeraora.time import BearStopwatch

LOGGING = {
    'version': 1,
    'formatters': {...},
    'filters': {...},
    'handlers': {
        'Console': {  # 确保有一个控制台输出
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
        # ...
    },
    'loggers': {
        BearStopwatch.LOGGER: {  # 添加相应的日志记录器
            'level': BearStopwatch.LEVEL,
            'handlers': ['Console'],
        },
    },
}
```

想要直接通过命令行打印？有的兄弟，有的！
[FoxStopwatch](https://docs.navifox.net/zeraora/module/zeraora.time.html#FoxStopwatch)
用法更简单：

```python
from zeraora.time import FoxStopwatch

with FoxStopwatch() as fox:
    # 业务逻辑
    pass
```

## 安装 {#install}

> uv 用户将 `pip install` 替换成 `uv pip install` 即可。

可以这样，直接安装本体：

```shell
pip install Zeraora
```

也可以这样，网络不好的时候用[镜像源](https://refs.navifox.net/mirror)：

```shell
pip install Zeraora -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn
```

还可以这样，只用一条命令就能一并安装一些可选的依赖：

| <pre>pip install</pre>      | 可选的依赖包                       | 备注                   |
|-----------------------------|------------------------------|----------------------|
| <pre>Zeraora[client]</pre>  | Requests                     | 面向 HTTP 客户端。         |
| <pre>Zeraora[backend]</pre> | Django                       | 面向后端开发。              |
| <pre>Zeraora[restful]</pre> | Django、Django REST Framework | 面向后端 RESTful API 开发。 |

如果全都要！那就这样：

```shell
pip install "Zeraora[client,restful]"
```

## 兼容性 {#compatibility}

| 依赖程度 | 兼容范围    |                                                                                                                                   |
|:----:|---------|-----------------------------------------------------------------------------------------------------------------------------------|
|  必需  | 3.10.0+ | [Python](https://docs.python.org/zh-cn/3/index.html) · 一门编程语言。                                                                    |
|  必需  | 4.14.0+ | [typing_extensions](https://typing-extensions.readthedocs.io/en/latest/) · 用于兼容标准库 `typing` 模块，提供运行时类型提示。Zeraora 0.4.0 之前不需要这个依赖。 |
| 非必需  | 2.27.0+ | [Requests](https://requests.readthedocs.io/en/latest/) · 简洁优雅的 HTTP 库。                                                            |
| 非必需  | 3.2.0+  | [Django](https://docs.djangoproject.com/zh-hans/5.2/) · Web 服务开发框架。                                                               |
| 非必需  | 3.13.0+ | [Django REST Framework](https://www.django-rest-framework.org/) · 基于 Django 的 RESTful Web 服务开发框架。                                 |
| 非必需  | 3.14.0+ | [djangorestframework-stubs](https://pypi.org/project/djangorestframework-stubs/) · Django REST Framework 的类型提示。                   |

## 许可证 {#license}

[MIT](https://opensource.org/licenses/MIT)。源代码会保持简洁、优雅，方便随时分叉出去。

## 社区 {#community}

前往 [GitHub](https://github.com/aixcyi/Zeraora/issues)
反馈 Bug，为项目添砖 Java；实在拿不准的话，就来[罗狐会馆](https://qm.qq.com/q/70TQXUMtQk)坐坐吧。

<div style="display: flex; flex-direction: column; justify-content: center; align-items: center">
    <img
        alt="QRCode"
        src="/qrcode.png"
        style="width: 240px; margin-top: 64px; padding: 24px; background-color: #24273a; border-radius: 32px"
    />
</div>
