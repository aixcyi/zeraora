"""
对 `Django <https://docs.djangoproject.com/zh-hans/4.2/>`_ 的扩展和增强。
"""
from __future__ import annotations

__all__ = [
    'SnakeModel',
]

from django.apps import apps
from django.db import models

from zeraora.string import case_camel_to_snake


class SnakeModel(models.base.ModelBase):
    """
    为模型生成一个下划线分隔的小写的数据表名（即蛇形命名法）。

    - 通过 ``Meta`` 手动指定的表名不会被覆盖。
    - 只会给非抽象模型（``Meta.abstract == False``）生成表名。

    ----

    用法如下： ::

        # ./apps/mall/models.py

        from django.db import models
        from zeraora.django import SnakeModel

        class GoodsSKUInfo(models.Model, metaclass=SnakeModel):
            name = models.CharField(max_length=64)
            price = models.IntegerField()
            stock = models.IntegerField()

            class Meta:
                abstract = False
                # db_table = ""

    以上模型没有设置 ``Meta.db_table``，
    那么 Django 默认生成的是 ``mall_goodsskuinfo``，
    而使用 SnakeModel 之后会默认生成 ``mall_goods_sku_info`` 。
    """

    def __new__(cls, name, bases, attrs, **kwargs):
        module = attrs.get('__module__', None)
        app_config = apps.get_containing_app_config(module)
        if app_config is None:
            return super().__new__(cls, name, bases, attrs, **kwargs)

        app_name = app_config.label
        model_name = case_camel_to_snake(app_name)
        table_name = f'{app_name}_{model_name}'

        if 'Meta' not in attrs:
            attrs['Meta'] = type('Meta', (), dict(db_table=table_name))

        abstract = getattr(attrs["Meta"], 'abstract', False)
        if not hasattr(attrs["Meta"], 'db_table') and not abstract:
            setattr(attrs['Meta'], 'db_table', table_name)

        return super().__new__(cls, name, bases, attrs, **kwargs)
