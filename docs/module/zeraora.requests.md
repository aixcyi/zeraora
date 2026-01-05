---
title: "`requests` 框架扩展"
excerpt:
---

# <pre>zeraora.requests</pre>

此模块提供了对 [Requests](https://requests.readthedocs.io/en/latest/)
这个第三方库的一些扩展和增强。

> [!WARNING] 依赖性警告
> 使用此模块前，请务必确保您安装了 Requests 这个第三方库！

## `HTTPTokenAuth(token)`

让请求带上以下格式的 HTTP 标头来传递我的令牌 _token_ 以实现身份认证：

```http request
GET /api
Authorization: Token 我的令牌
```

而 Requests 自带的 `HTTPBasicAuth` 提供的 HTTP 标头格式如下：

```http request
GET /api
Authorization: Basic 我的用户名 我的密码
```

这个类主要为 `requests.get()`、`requests.post()` 等方法提供 _auth_ 参数，用法如下：

```python
import requests
from zeraora.requests import HTTPTokenAuth

requests.post(
    url='https://zeraora.tighnari.net/docs-testing/',
    auth=HTTPTokenAuth('c2b7bafcd3f000000000000000000000'),
)
```

## `HTTPBearerAuth(token)`

让请求带上以下格式的 HTTP 标头来传递我的令牌 _token_ 以实现身份认证：

```http request
GET /api
Authorization: Bearer 我的令牌
```

用法参见 [`HTTPTokenAuth`](#HTTPTokenAuth)
