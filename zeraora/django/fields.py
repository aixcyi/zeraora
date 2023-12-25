"""
定制的 Django ORM `模型字段 <https://docs.djangoproject.com/zh-hans/4.2/ref/models/fields/>`_ 。

参阅 `编写自定义模型字段 <https://docs.djangoproject.com/zh-hans/4.2/howto/custom-model-fields/>`_ 。
"""

__all__ = [
    'BizField',
    'MoneyField',
    'OSSPathField',
]

from decimal import Decimal

from django.db import models
from django.utils.translation import gettext_lazy


class BizField(models.CharField):
    """
    对外业务ID字段。默认最大长度 32 字符。
    """
    description = "对外业务ID，最多容纳 %(max_length)s 个字符。"

    def __init__(self, verbose_name=None, **kwargs):
        kwargs.setdefault('max_length', 32)
        super().__init__(verbose_name, **kwargs)


class MoneyField(models.DecimalField):
    """
    金额。默认 12 位数，小数部分占用 2 位。
    """
    description = gettext_lazy("金额。")

    ZERO = Decimal('0.00')

    def __init__(self, verbose_name=None, default: Decimal = ZERO, **kwargs):
        kwargs.setdefault('max_digits', 12)
        kwargs.setdefault('decimal_places', 2)
        super().__init__(verbose_name, default=default, **kwargs)


class OSSPathField(models.CharField):
    """
    对象储存（OSS）中的文件路径。
    """
    description = gettext_lazy("对象储存（OSS）中的文件路径。")

    def __init__(self, verbose_name=None, **kwargs):
        kwargs.setdefault('max_length', 100)
        kwargs.setdefault('null', True)
        kwargs.setdefault('default', None)
        kwargs.setdefault('blank', True)
        super().__init__(verbose_name, **kwargs)
