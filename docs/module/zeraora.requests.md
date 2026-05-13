---
title: "`requests` 框架扩展"
excerpt:
---

# <pre>zeraora.requests</pre>

此模块提供了对 [Requests](https://requests.readthedocs.io/en/latest/)
这个第三方库的一些扩展和增强。

> [!WARNING] 依赖性警告
> 使用此模块前，请务必确保您安装了 Requests 这个第三方库！

## HTTPTokenAuth

让请求带上以下格式的 Authorization 标头来传递 _我的令牌_ 以实现身份认证：

```http request
GET /api/oms/orders
Authorization: Token 我的令牌
```

而 Requests 自带的
[HTTPBasicAuth](https://requests.readthedocs.io/en/latest/api/#requests.auth.HTTPBasicAuth)
提供的 Authorization 标头格式如下：

```http request
GET /api/oms/orders
Authorization: Basic 我的用户名 我的密码
```

这个类主要为 Requests 的
[`get()`](https://requests.readthedocs.io/en/latest/api/#requests.get)
和
[`post()`](https://requests.readthedocs.io/en/latest/api/#requests.post)
等方法提供 _auth_ 参数，用法如下：

```python
import requests
from zeraora.requests import HTTPTokenAuth

# 传递一个 token，值是 "c2b7bafcd3f000000000000000000000"
requests.post(
    url='https://docs.navifox.net/zeraora/docs-testing/',
    auth=HTTPTokenAuth('c2b7bafcd3f000000000000000000000'),
)
```

## HTTPBearerAuth

与 [HTTPTokenAuth](#HTTPTokenAuth)
一样，只不过会将 Authorization 标头中的 `Token` 换成 `Bearer`：

```http request
GET /api/oms/orders
Authorization: Bearer 我的令牌
```
