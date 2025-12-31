---
prev: false
next: false
titleTemplate: ":title"
title: Zeraora
aside: false
sidebar: false
outline: false
excerpt:
---

<div align="center">
    <p><img src="/logo.svg"/></p>
    <p style="display: flex; flex-wrap: wrap; gap: .5rem; justify-content: center">
        <a href="https://docs.python.org/zh-cn/3/whatsnew/index.html"><img src="https://img.shields.io/pypi/pyversions/zeraora?logo=python&logoColor=yellow"></a>
        <a href="https://pypi.org/project/Zeraora/"><img src="https://img.shields.io/pypi/v/zeraora?color=darkgreen"></a>
        <a href=""><img src="https://img.shields.io/conda/v/conda-forge/zeraora"></a>
        <a href=""><img src="https://img.shields.io/pypi/status/Zeraora"></a>
        <a href=""><img src="https://img.shields.io/pypi/dm/zeraora?color=C72777"></a>
    </p>
    <p>
        <i>长期维护的实用基础设施工具包</i>
        <br>
        <i>Personal infrastructure toolkit with long-term maintenance.</i>
    </p>
</div>

## 特性 {#features}

一个 Python 工具包，包含从实务实践中抽象提取的工具。

除了 [typing_extensions](https://typing-extensions.readthedocs.io/en/latest/)
用于兼容类型提示外，工具包不强制依赖任何第三方库；内含的实用工具大致拆分成以下几个包，文档中部分工具也备注了一些实践指南：

- [<pre>zeraora.conf</pre>](/module/zeraora.conf)，配置辅助工具。
- [<pre>zeraora.django</pre>](/module/zeraora.django)，对经典 Web 框架 [Django](https://docs.djangoproject.com/zh-hans/5.2/) 的扩展和增强。
- [<pre>zeraora.drf</pre>](/module/zeraora.drf)，对 RESTful API 框架 [Django REST Framework](https://www.django-rest-framework.org/) 的扩展和增强。
- [<pre>zeraora.enum</pre>](/module/zeraora.enum)，实用枚举。
- [<pre>zeraora.math</pre>](/module/zeraora.math)，数学计算与常量。
- [<pre>zeraora.requests</pre>](/module/zeraora.requests)，对 [Requests](https://requests.readthedocs.io/en/latest/) 的扩展和增强。
- [<pre>zeraora.string</pre>](/module/zeraora.string)，字符集常量，与字符串生成。
- [<pre>zeraora.time</pre>](/module/zeraora.time)，时间与计时。
- [<pre>zeraora.uuid</pre>](/module/zeraora.uuid)，UUID 生成函数。

## 安装 {#install}

```shell
pip install Zeraora
```

若安装时网络不佳，可以考虑使用镜像源：

```shell
pip install Zeraora -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn
```

安装时也可以一同安装可选的依赖包：

| <pre>pip install</pre>      | 可选的依赖包                       | 备注                   |
|-----------------------------|------------------------------|----------------------|
| <pre>Zeraora[client]</pre>  | Requests                     | 面向 HTTP 客户端。         |
| <pre>Zeraora[backend]</pre> | Django                       | 面向后端开发。              |
| <pre>Zeraora[restful]</pre> | Django、Django REST Framework | 面向后端 RESTful API 开发。 |

还可以一次性安装多个依赖：

```shell
pip install "Zeraora[client,restful]"
```

## 兼容性 {#compatibility}

Zeraora 目前仍在积极开发中，无法保证每个 0.x 之间能够互相迁移；但一旦正式发布第一个
0.x，那么接下来每一个 0.x.y 都会维持比较高的兼容性，以确保可以随时回退，不会因迁移而产生太多更改。

| 要求 | 兼容范围    |                                                                                                           |
|----|---------|-----------------------------------------------------------------------------------------------------------|
| 刚需 | 3.10.0+ | [Python](https://docs.python.org/zh-cn/3/index.html) · 一门编程语言。                                            |
| 刚需 | 4.14.0+ | [typing_extensions](https://typing-extensions.readthedocs.io/en/latest/) · 用于兼容标准库 `typing` 模块，提供运行时类型提示。 |
| 可选 | 2.27.0+ | [Requests](https://requests.readthedocs.io/en/latest/) · 简洁优雅的 HTTP 库。                                    |
| 可选 | 3.2.0+  | [Django](https://docs.djangoproject.com/zh-hans/5.2/) · Web 服务开发框架。                                       |
| 可选 | 3.13.0+ | [Django REST Framework](https://www.django-rest-framework.org/) · 基于 Django 的 RESTful Web 服务开发框架。         |

## 社区 {#community}

可前往 GitHub [issues](https://github.com/aixcyi/Zeraora/issues)
获取帮助或进行反馈；也可前往[罗狐会馆](https://qm.qq.com/q/9RfmeydwNq)参与讨论、获取非实时帮助。



<style scoped>
li pre {
    display: inline;
    margin: 0;
}
</style>
