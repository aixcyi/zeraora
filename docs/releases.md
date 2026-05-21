---
title: 发行说明
order: 30
excerpt:
---

# 发行说明

## 兼容性 {#compatibility}

```python
import zeraora

print(zeraora.__version__)  # x.y.z
print(zeraora.VERSION >= (0, 4))
```

Zeraora 的版本号遵守 Semantic Versioning 2.0 规范，大致格式为 `x.y.z`，分别对应主版本号、次版本号和修订号。

- 修订版本 `0.0.z` 之间 API 一般是可以兼容的。
- 次版本号 `0.y.0` 必定包含 API 不兼容的变更，升级之前应当仔细阅读发布注记。
- 主版本号 `x.0.0` 保留给项目里程碑版本，当前保持为 0 用来标记项目仍未成熟，API 可能会随时变更。

每个版本都可以对应三个阶段之一，分别是
[`zeraora.VERSION`](/module/zeraora#VERSION) 的 _releaselevel_ 属性可能出现的三个值：

- _alpha_ 版本包含了新功能，尚处于测试阶段，仅供开发人员测试。
- _beta_ 版本的新功能已经过一定的测试与验证，可供用户预览和适配。
- _candidate_ 版本的功能已经近乎完善，并且有实际线上使用案例，只不过未经完善测试。
- _final_ 版本的功能已经经过测试完善，可用于正式环境构建与运行。

## 依赖 {#dependency}

| 依赖程度 | 兼容范围    |                                                                                                                                   |
|:----:|---------|-----------------------------------------------------------------------------------------------------------------------------------|
|  必需  | 3.10.0+ | [Python](https://docs.python.org/zh-cn/3/index.html) · 一门编程语言。                                                                    |
|  必需  | 4.14.0+ | [typing_extensions](https://typing-extensions.readthedocs.io/en/latest/) · 用于兼容标准库 `typing` 模块，提供运行时类型提示。Zeraora 0.4.0 之前不需要这个依赖。 |
| 非必需  | 2.27.0+ | [Requests](https://requests.readthedocs.io/en/latest/) · 简洁优雅的 HTTP 库。                                                            |
| 非必需  | 3.2.0+  | [Django](https://docs.djangoproject.com/zh-hans/5.2/) · Web 服务开发框架。                                                               |
| 非必需  | 3.13.0+ | [Django REST Framework](https://www.django-rest-framework.org/) · 基于 Django 的 RESTful Web 服务开发框架。                                 |
| 非必需  | 3.14.0+ | [djangorestframework-stubs](https://pypi.org/project/djangorestframework-stubs/) · Django REST Framework 的类型提示。                   |

> 没有办法兼容以前的 Python，3.10 新增的 match-case 实在太好用了！！

## 生命周期 {#lifecycle}

在 Zeraora 0.x 阶段，每一个 0.x 版本都会占用一条独立的
git 分支（名称见下表第一列），生命周期预计为两年，一直到发布起的第三个除夕夜为止，但若是没有
0.(x+1) 的开发计划，那么生命周期将会顺延到下一个除夕夜。

- 开发阶段 _features_ 表示新功能开发中，API 可能会随时变更。
- 维护阶段 _bugfix_ 表示功能完善，主要修复 bug，不添加新功能。
- 停止维护 _EOL_ 表示不再维护。如果没有重大事项，一般不会再更新。

| 分支名称                                                  | Python 兼容范围 | 版本现状            | 生命周期            |
|-------------------------------------------------------|-------------|-----------------|-----------------|
| 0.4.x（[main](https://github.com/aixcyi/Zeraora)）      | 3.10～3.14   | 开发阶段 _features_ | 2028年1月25日止（预计） |
| [0.3.x](https://github.com/aixcyi/Zeraora/tree/0.3.x) | 3.7～3.12    | 停止维护 _EOL_      | 2026年2月16日止     |
| [0.2.x](https://github.com/aixcyi/Zeraora/tree/0.2.x) | 3.7～3.12    | 停止维护 _EOL_      | 2024年4月12日止     |
| [0.1.x](https://github.com/aixcyi/Zeraora/tree/0.1.x) | 3.7～3.11    | 停止维护 _EOL_      | 2023年6月9日止      |
