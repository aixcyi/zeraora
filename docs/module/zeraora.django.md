---
title: "`django` 框架扩展"
excerpt:
---

# <pre>zeraora.django</pre>

此模块提供了对 [Django](https://docs.djangoproject.com/zh-hans/5.2/)
这个框架的一些扩展和增强。

> [!WARNING] 依赖性警告
> 使用此模块前，请务必确保您安装了 Django 这个框架！

## SnakeModel

一个元类，用于为模型生成一个下划线分隔的小写的数据表名（即蛇形命名法）。

```python :line-numbers
# ./apps/wms/models.py
from django.db import models
from zeraora.django import SnakeModel

class GoodsSKUInfo(models.Model, metaclass=SnakeModel):  # [!code highlight]
    name = models.CharField(max_length=64)
    price = models.IntegerField()
    stock = models.IntegerField()
```

默认情况下，Django 会为 GoodsSKUInfo 模型生成一个名为 `wms_goodsskuinfo`
的表，而使用 SnakeModel 元类后，会生成一个名为 `wms_goods_sku_info` 的表。

## PrefilterManager

一个[管理器](https://docs.djangoproject.com/zh-hans/5.2/topics/db/managers/)类，允许预设任意过滤条件。

> [!TIP] 实践指南
> 用一个管理器之前，建议先定义 `objects` 属性，避免 Django
> 将不符合预期的管理器认作[默认管理器](https://docs.djangoproject.com/zh-hans/5.2/topics/db/managers/#default-managers)。

```python :line-numbers
# ./apps/oms/models.py
from django.db import models
from zeraora.django import PrefilterManager

class OrderState(models.IntegerChoices):
    ORDERING = 0, '点单中'
    SUBMITTED = 10, '已下单'
    PAYING = 20, '支付中'
    PAYED = 50, '已支付'

class Order(models.Model):
    no = models.CharField(max_length=11, unique=True, db_index=True)
    state = models.IntegerField()
    deleted = models.BooleanField(default=False)

    objects = models.Manager()
    availables = PrefilterManager(  # [!code focus]
        ~models.Q(state=OrderState.ORDERING),  # [!code focus]
        deleted=False,  # [!code focus]
    )  # [!code focus]

# 下面两个查询集是等价的
Order.availables.all()
Order.objects.filter(~models.Q(state=OrderState.ORDERING), deleted=False)
```
