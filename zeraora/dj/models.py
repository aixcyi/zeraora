"""
对 Django ORM模型 的增强。
"""
from __future__ import annotations

__all__ = [
    'SnakeModel',
]

import re

from django.apps import apps
from django.db import models


def convert_camel_name(name):
    # "CombineOrderSKUModel"
    # -> "Combine OrderSKU Model"
    # -> "Combine Order SKU Model"
    # -> "combine_order_sku_model"
    mid = re.sub('(.)([A-Z][a-z]+)', r'\1 \2', name)
    words = re.sub('([a-z0-9])([A-Z])', r'\1 \2', mid)
    return '_'.join(word.lower() for word in words.split())


class SnakeModel(models.base.ModelBase):
    """
    自动生成一个下划线小写的（蛇形）数据表名。

    >>> class GoodsSKUInfo(models.Model,
    >>>                    metaclass=SnakeModel):
    >>>     # 字段声明...
    >>>
    >>>     class Meta:
    >>>         # SnakeModel的生成格式
    >>>         db_table = "{app}_goods_sku_info"
    >>>
    >>>         # Django的生成格式
    >>>         # db_table = "{app}_goodsskuinfo"

    - 不会覆盖已经指定了的表名。
    - 可以用于抽象模型中，但只会为继承了抽象模型的非抽象模型生成表名。

    适用于：``django.db.models.Model`` 的子类
    """

    def __new__(cls, name, bases, attrs, **kwargs):
        module = attrs.get('__module__', None)
        app_config = apps.get_containing_app_config(module)
        if app_config is None:
            return super().__new__(cls, name, bases, attrs, **kwargs)

        app_name = app_config.label
        model_name = convert_camel_name(app_name)
        table_name = f'{app_name}_{model_name}'

        if 'Meta' not in attrs:
            attrs['Meta'] = type('Meta', (), dict(db_table=table_name))

        abstract = getattr(attrs["Meta"], 'abstract', False)
        if not hasattr(attrs["Meta"], 'db_table') and not abstract:
            setattr(attrs['Meta'], 'db_table', table_name)

        return super().__new__(cls, name, bases, attrs, **kwargs)
