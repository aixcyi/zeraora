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
            <img alt="Conda 适配进度"
                 draggable="false"
                 src="https://img.shields.io/conda/v/conda-forge/zeraora"
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
        <i>一堆实用小玩意儿，快如电，轻如猫</i>
        <br />
        <i>Zeraora lightweight collection of utilities that save your dev time.</i>
    </p>
</div>

## 特性 {#features}

一个 Python 工具包，包含一堆杂七杂八的工具，大部分都是从日常业务代码里提取抽象的，有些是为了保障兼容性，希望能帮你少写几行代码。

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

## 安装 {#install}

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
