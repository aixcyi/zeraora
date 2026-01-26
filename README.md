<div align="center">
    <p><img src="./docs/public/logo.svg" alt="Zeraora Logo" /></p>
    <a href="https://docs.python.org/zh-cn/3/whatsnew/index.html">
        <img alt="[Python Compatibility]"
             src="https://img.shields.io/pypi/pyversions/zeraora?logo=python&logoColor=yellow">
    </a>
    <a href="https://pypi.org/project/Zeraora/">
        <img alt="[PyPI Version]"
             src="https://img.shields.io/pypi/v/zeraora?color=darkgreen">
    </a>
    <a href="">
        <img alt="[Conda Version]"
             src="https://img.shields.io/conda/v/conda-forge/zeraora">
    </a>
    <a href="">
        <img alt="[Package Status]"
             src="https://img.shields.io/pypi/status/Zeraora">
    </a>
    <a href="">
        <img alt="[Downloads per month]"
             src="https://img.shields.io/pypi/dm/zeraora?color=C72777">
    </a>
</div>
<div align="center">
    <i>一堆实用小玩意儿，轻如电，快如猫</i>
    <br>
    <i>Zeraora lightweight collection of utilities that save your dev time.</i>
</div>

一个 Python 工具包，包含一堆杂七杂八的工具，大部分都是从日常业务代码里提取抽象的，有些是为了保障兼容性，希望能帮你少写几行代码。

- [`zeraora.conf`](/module/zeraora.conf)，配置辅助工具。
- [`zeraora.django`](/module/zeraora.django)，对经典 Web 框架 [Django](https://docs.djangoproject.com/zh-hans/5.2/) 的扩展和增强。
- [`zeraora.drf`](/module/zeraora.drf)，对 RESTful API 框架 [Django REST Framework](https://www.django-rest-framework.org/) 的扩展和增强。
- [`zeraora.math`](/module/zeraora.math)，数学计算与常量。
- [`zeraora.requests`](/module/zeraora.requests)，对 [Requests](https://requests.readthedocs.io/en/latest/) 的扩展和增强。
- [`zeraora.string`](/module/zeraora.string)，字符集常量，与字符串生成。
- [`zeraora.time`](/module/zeraora.time)，时间与计时。
- [`zeraora.uuid`](/module/zeraora.uuid)，UUID 生成函数。

优点：除了 [typing_extensions](https://typing-extensions.readthedocs.io/en/latest/)
用来兼容类型提示外，它不强制依赖任何第三方库。  
缺点：优点太少。

## 安装

可以这样，直接安装本体：

```shell
pip install Zeraora
```

也可以这样，网络不好的时候用镜像源：

```shell
pip install Zeraora -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn
```

还可以这样，一条命令同时安装一些可选的依赖：

| `pip install`      | 可选的依赖包                       | 备注                   |
|--------------------|------------------------------|----------------------|
| `Zeraora[client]`  | Requests                     | 面向 HTTP 客户端。         |
| `Zeraora[backend]` | Django                       | 面向后端开发。              |
| `Zeraora[restful]` | Django、Django REST Framework | 面向后端 RESTful API 开发。 |

如果全都要！那就这样：

```shell
pip install "Zeraora[client,restful]"
```

## 兼容性

已经推进到第四个大版本，基本上都稳定了（毕竟东西就那点）；新的东西会细水长流慢慢测、慢慢加。

某个 0.x 内的小版本基本是兼容的，但每个 0.x 的大版本之间改动太大，就不太能兼容了。

| 依赖程度 | 兼容范围    |                                                                                                           |
|:----:|---------|-----------------------------------------------------------------------------------------------------------|
|  必需  | 3.10.0+ | [Python](https://docs.python.org/zh-cn/3/index.html) · 一门编程语言。                                            |
|  必需  | 4.14.0+ | [typing_extensions](https://typing-extensions.readthedocs.io/en/latest/) · 用于兼容标准库 `typing` 模块，提供运行时类型提示。 |
| 非必需  | 2.27.0+ | [Requests](https://requests.readthedocs.io/en/latest/) · 简洁优雅的 HTTP 库。                                    |
| 非必需  | 3.2.0+  | [Django](https://docs.djangoproject.com/zh-hans/5.2/) · Web 服务开发框架。                                       |
| 非必需  | 3.13.0+ | [Django REST Framework](https://www.django-rest-framework.org/) · 基于 Django 的 RESTful Web 服务开发框架。         |

没有办法兼容以前的 Python，3.10 新增的 match-case 实在太好用了！！

## 文档

可前往[文档月饼盒](https://docs.navifox.net/zeraora/)。

## 许可证

[MIT](https://opensource.org/licenses/MIT)。源代码会保持简洁、优雅，方便随时分叉出去。

## 社区

有什么新奇想法，或者实在搞不定的话，就来[罗狐会馆](https://qm.qq.com/q/9RfmeydwNq)坐坐吧，QQ 群坐标 699090940。

作者毛茸茸的，很好挼。

Bug 需要前往 [GitHub](https://github.com/aixcyi/Zeraora/issues) 反馈喔~ 不然记不住容易忘。
