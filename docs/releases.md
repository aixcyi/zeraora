---
title: 发行说明
order: 3
excerpt:
---

# 发行说明

## 兼容性与依赖 {#compatibility}

### 0.4.x {#compatibility-0.4.x}

| 要求 | 兼容范围    |                                                                                                           |
|----|---------|-----------------------------------------------------------------------------------------------------------|
| 刚需 | 3.10.0+ | [Python](https://docs.python.org/zh-cn/3/index.html) · 一门编程语言。                                            |
| 刚需 | 4.14.0+ | [typing_extensions](https://typing-extensions.readthedocs.io/en/latest/) · 用于兼容标准库 `typing` 模块，提供运行时类型提示。 |
| 可选 | 2.27.0+ | [Requests](https://requests.readthedocs.io/en/latest/) · 简洁优雅的 HTTP 库。                                    |
| 可选 | 3.2.0+  | [Django](https://docs.djangoproject.com/zh-hans/5.2/) · Web 服务开发框架。                                       |
| 可选 | 3.13.0+ | [Django REST Framework](https://www.django-rest-framework.org/) · 基于 Django 的 RESTful Web 服务开发框架。         |

### 0.3.x {#compatibility-0.3.x}

| 要求 | 兼容范围    |                                                                                                   |
|----|---------|---------------------------------------------------------------------------------------------------|
| 刚需 | 3.7.0+  | [Python](https://docs.python.org/zh-cn/3/index.html) · 一门编程语言。                                    |
| 可选 | 2.27.0+ | [Requests](https://requests.readthedocs.io/en/latest/) · 简洁优雅的 HTTP 库。                            |
| 可选 | 3.2.0+  | [Django](https://docs.djangoproject.com/zh-hans/5.2/) · Web 服务开发框架。                               |
| 可选 | 3.13.0+ | [Django REST Framework](https://www.django-rest-framework.org/) · 基于 Django 的 RESTful Web 服务开发框架。 |

## 开发周期 {#development}

从 0.4 版本开始，开发周期分为三个阶段，每个 0.x.y 版本一般情况下仅占用一个阶段，对应
[`zeraora.VERSION`](/module/zeraora#VERSION) 的 _releaselevel_ 属性可能出现的三个值：

- _alpha_ 阶段，仅供开发人员测试，结构功能可能会有较大变动，不建议将项目发布到正式环境中。
- _beta_ 阶段，供用户预览和适配，结构功能比较稳定，可能仍有新功能添加，项目发布前应审慎考虑。
- _final_ 阶段，正式发布并转入维护状态，直至 0.x 版本生命周期结束，结构及功能不再变动，仅接受问题修复。

开发阶段仅占用仓库 main 分支；转入维护阶段后，代码仓库中会创建相应版本的独立分支，若此时尚未计划开发 0.(x+1) 版本，那么将优先更新 main 分支。

| Zeraora                                               | Python    | 版本 Cycle     | 预计生命周期      |
|-------------------------------------------------------|-----------|--------------|-------------|
| 0.4.x（[main](https://github.com/aixcyi/Zeraora)分支）    | 3.10～3.14 | 开发中 features | 2030年2月2日止  |
| [0.3.x](https://github.com/aixcyi/Zeraora/tree/0.3.x) | 3.7～3.12  | 维护中 bugfix   | 2028年1月25日止 |
| [0.2.x](https://github.com/aixcyi/Zeraora/tree/0.2.x) | 3.7～3.12  | 已停止维护 EOL    | 2024年4月12日止 |
| [0.1.x](https://github.com/aixcyi/Zeraora/tree/0.1.x) | 3.7～3.11  | 已停止维护 EOL    | 2023年6月9日止  |

## 主要历史变迁

- 0.4.x 精简了大量重复的轮子，重命名了晦涩的模块名，开始部署文档站点。
- 0.3.x 改进了包结构，功能趋于稳定。
- 0.2.x 探索包结构，完善核心，补充非核心特性。
- 0.1.x 试验自动部署，只有核心特性。
