---
title: 发行说明
order: 3
excerpt:
---

# 发行说明

## 兼容性与依赖 {#compatibility}

### 0.4.x {#compatibility-0.4.x}

| 依赖性 | 兼容范围    |                                                                                                           |
|:---:|---------|-----------------------------------------------------------------------------------------------------------|
| 必需  | 3.10.0+ | [Python](https://docs.python.org/zh-cn/3/index.html) · 一门编程语言。                                            |
| 必需  | 4.14.0+ | [typing_extensions](https://typing-extensions.readthedocs.io/en/latest/) · 用于兼容标准库 `typing` 模块，提供运行时类型提示。 |
| 非必需 | 2.27.0+ | [Requests](https://requests.readthedocs.io/en/latest/) · 简洁优雅的 HTTP 库。                                    |
| 非必需 | 3.2.0+  | [Django](https://docs.djangoproject.com/zh-hans/5.2/) · Web 服务开发框架。                                       |
| 非必需 | 3.13.0+ | [Django REST Framework](https://www.django-rest-framework.org/) · 基于 Django 的 RESTful Web 服务开发框架。         |

> “非必需”是指仅在用到某些模块的情况下，才需要安装某个依赖；这会在那些模块文档的顶部标明。

### 0.3.x {#compatibility-0.3.x}

| 依赖性 | 兼容范围    |                                                                                                   |
|:---:|---------|---------------------------------------------------------------------------------------------------|
| 必需  | 3.7.0+  | [Python](https://docs.python.org/zh-cn/3/index.html) · 一门编程语言。                                    |
| 非必需 | 2.27.0+ | [Requests](https://requests.readthedocs.io/en/latest/) · 简洁优雅的 HTTP 库。                            |
| 非必需 | 3.2.0+  | [Django](https://docs.djangoproject.com/zh-hans/5.2/) · Web 服务开发框架。                               |
| 非必需 | 3.13.0+ | [Django REST Framework](https://www.django-rest-framework.org/) · 基于 Django 的 RESTful Web 服务开发框架。 |

> “非必需”是指仅在用到某些模块的情况下，才需要安装某个依赖；这会在那些模块文档的顶部标明。

## 开发周期 {#development}

由于开发时间和精力有限，Zeraora 采用短周期敏捷开发与迭代，目前发行的每个 0.x.y 可以对应三个阶段之一，分别是
[`zeraora.VERSION`](/module/zeraora#VERSION) 的 _releaselevel_ 属性可能出现的三个值：

- _alpha_ 版本包含了新功能，尚处于测试阶段，仅供开发人员测试。
- _beta_ 版本的新功能已经过一定的测试与验证，可供用户预览和适配。
- _final_ 版本的功能已经近乎完善，没有新功能添加，可用于正式环境构建与运行。

每一个 0.x 版本都会占用一条独立的 git 分支（名称见下表第一列），生命周期预计为两年，一直到发布起的第三个除夕夜为止，但若是没有
0.(x+1) 的开发计划，那么生命周期将会顺延到下一个除夕夜。

| Zeraora                                               | Python    | 版本现状 Cycle    | 预计生命周期      |
|-------------------------------------------------------|-----------|---------------|-------------|
| 0.4.x（[main](https://github.com/aixcyi/Zeraora)分支）    | 3.10～3.14 | 开发阶段 features | 2028年1月25日止 |
| [0.3.x](https://github.com/aixcyi/Zeraora/tree/0.3.x) | 3.7～3.12  | 维护阶段 bugfix   | 2026年2月16日止 |
| [0.2.x](https://github.com/aixcyi/Zeraora/tree/0.2.x) | 3.7～3.12  | 停止维护 EOL      | 2024年4月12日止 |
| [0.1.x](https://github.com/aixcyi/Zeraora/tree/0.1.x) | 3.7～3.11  | 停止维护 EOL      | 2023年6月9日止  |

## 主要历史变迁

- 0.4.x 精简了大量重复的轮子，重命名了晦涩的模块名，开始部署文档并记录符号变迁。
- 0.3.x 改进了包结构，功能趋于稳定。
- 0.2.x 探索包结构，完善核心，补充非核心特性。
- 0.1.x 试验自动部署，只有核心特性。
