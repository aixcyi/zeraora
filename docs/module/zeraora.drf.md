---
title: "`drf` — REST Framework 扩展"
excerpt:
---

# <pre>zeraora.drf</pre>

此模块提供了对 [Django REST Framework](https://www.django-rest-framework.org/)
这个框架的一些扩展和增强。

> [!WARNING] 依赖性警告
> 使用此模块前，请务必确保您安装了 Django REST Framework 这个框架！

## `BitListField`

一个序列化器字段，允许在“整数”和“比特数组”之间转换。

| 序列化前／后端 |        序列化后／前端 |
|--------:|---------------:|
|       7 |    `[1, 2, 4]` |
|       0 |           `[]` |
|      -7 | `[-1, -2, -4]` |

```python :line-numbers
from rest_framework import serializers
from zeraora.drf import BitListField
from apps.oms.models import Ticket

class TicketDetailSerializer(serializers.ModelSerializer):
    """
    门票信息（序列化器）。
    """
    days = BitListField(help_text='第n比特代表周n')  # [!code focus]

    class Meta:
        model = Ticket
        fields = '__all__'
```

## `BearerAuthentication`

一个基于 Token 的认证器。

使用框架的 [`TokenAuthentication`](https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication)
需要提供以下格式的 HTTP 头，否则无法提取认证信息：

```http request
GET /api
Authorization: Token xxxxxx
```

而如果需要对接 apifox 等自动化软件，则可以使用 `BearerAuthentication` 来要求更加通用的格式：

```http request
GET /api
Authorization: Bearer xxxxxx
```

在函数视图中，用法如下：

```python :line-numbers
from zeraora.drf import BearerAuthentication
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)

@api_view(['GET'])
@authentication_classes([BearerAuthentication])  # [!code focus]
@permission_classes([IsAdminUser])
def get_server_state(request, *args, **kwargs):
    ...
```

在类视图中，用法如下：

```python :line-numbers
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from zeraora.drf import BearerAuthentication

class OrderView(APIView):
    authentication_classes = [BearerAuthentication]  # [!code focus]
    permission_classes = [IsAdminUser]
    ...
```

## `IsAdminUserOrReadOnly`

一个权限校验器。要么请求来自一个已认证的管理员，要么它是一个只读请求。

在函数视图中，用法如下：

```python :line-numbers
from zeraora.drf import IsAdminUserOrReadOnly
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUserOrReadOnly])  # [!code focus]
def manage_buckets(request, *args, **kwargs):
    ...
```

在类视图中，用法如下：

```python :line-numbers
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from zeraora.drf import IsAdminUserOrReadOnly

class BucketView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUserOrReadOnly]  # [!code focus]
    ...
```
