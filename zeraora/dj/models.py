"""
对 Django ORM模型 的增强。
"""
from __future__ import annotations

import re
import uuid

from .. import gvs
from ..constants import Degree, Province
from ..structures import DivisionCode
from ..utils import warn_empty_ads

try:
    from django.apps import apps
    from django.db import models
except ImportError as e:
    raise ImportError('需要安装Django框架：\npip install django') from e


class SnakeModel(models.base.ModelBase):
    """
    自动生成一个下划线小写的（蛇形）数据表名。

    >>> class YourModel(models.Model,
    >>>                 metaclass=SnakeModel):
    >>>     # 字段声明...
    >>>
    >>>     class Meta:
    >>>         # SnakeModel的生成格式
    >>>         db_table = "{app}_{snake_model_name}"
    >>>
    >>>         # Django的生成格式
    >>>         # db_table = "{app}_{lowermodelname}"

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

        model_name = re.sub(r'[A-Z]', (lambda s: f'_{s.group(0).lower()}'), name)
        model_name = model_name[1:] if model_name.startswith('_') else model_name

        table_name = f'{app_name}_{model_name}'

        if 'Meta' not in attrs:
            attrs['Meta'] = type('Meta', (), dict(db_table=table_name))

        abstract = getattr(attrs["Meta"], 'abstract', False)
        if not hasattr(attrs["Meta"], 'db_table') and not abstract:
            setattr(attrs['Meta'], 'db_table', table_name)

        return super().__new__(cls, name, bases, attrs, **kwargs)


class CreateTimeMixin(models.Model):
    """
    为模型附加以下字段：

    - ``created_at`` ，只读。记录模型创建时刻（日期+时间）。

    适用于：``django.db.models.Model`` 的子类
    """
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        abstract = True


class TimeMixin(models.Model):
    """
    为模型附加以下字段：

    - ``created_at`` ，只读。记录模型创建时刻（日期+时间）。
    - ``updated_at`` ，可空。记录模型修改时刻（日期+时间），仅当 ``Model.save()`` 被调用时被自动设置。

    适用于：``django.db.models.Model`` 的子类
    """
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('修改时间', auto_now=True)

    class Meta:
        abstract = True


class ActiveStatusMixin(models.Model):
    """
    为模型附加以下字段和方法：

    - ``activated`` ，可空。用于标记禁用状态。默认为 ``True`` ，当被设置为 ``False`` 时表示被标记为已禁用。
    - ``get_active_set()`` ，获取已启用的行，返回一个查询集。

    适用于：``django.db.models.Model`` 的子类
    """
    activated = models.BooleanField(default=True, blank=True)

    @classmethod
    def get_active_set(cls, *args, **kwargs) -> models.QuerySet:
        return cls.objects.all().filter(*args, **kwargs, activated=True)

    class Meta:
        abstract = True


class DeletionMixin(models.Model):
    """
    为模型附加以下字段和方法：

    - ``deleted`` ，可空。用于标记删除状态。默认为 ``False`` ，当被设置为 ``True`` 时表示被标记为已删除。
    - ``get_existing_set()`` ，获取未被删除的行，返回一个查询集。

    适用于：``django.db.models.Model`` 的子类
    """
    deleted = models.BooleanField(default=False, blank=True)

    @classmethod
    def get_existing_set(cls, *args, **kwargs) -> models.QuerySet:
        return cls.objects.all().filter(*args, **kwargs, deleted=False)

    class Meta:
        abstract = True


class IndexMixin(models.Model):
    """
    为模型附加以下字段和方法：

    - ``index`` ，可空。用于存放自定义索引（32位有符号整数）。默认值 ``0`` 。
    - ``get_ordered_set()`` ，获取一个按 ``index`` 字段从大到小排序的查询集。
    - ``get_reversed_set()`` ，获取一个按 ``index`` 字段从小到大排序的查询集。

    适用于：``django.db.models.Model`` 的子类
    """
    index = models.IntegerField(default=0, blank=True)

    @classmethod
    def get_ordered_set(cls, *args, **kwargs) -> models.QuerySet:
        """
        返回一个按 ``index`` 字段 **从大到小** 排序的查询集。

        :param args: 传递给 Model.objects.filter() 的 *args 参数。
        :param kwargs: 传递给 Model.objects.filter() 的 **kwargs 参数。
        :return: 对应模型的查询集。
        """
        return cls.objects.all().filter(*args, **kwargs).order_by('-index')

    @classmethod
    def get_reversed_set(cls, *args, **kwargs) -> models.QuerySet:
        """
        返回一个按 ``index`` 字段 **从小到大** 排序的查询集。

        :param args: 传递给 Model.objects.filter() 的 *args 参数。
        :param kwargs: 传递给 Model.objects.filter() 的 **kwargs 参数。
        :return: 对应模型的查询集。
        """
        return cls.objects.all().filter(*args, **kwargs).order_by('index')

    class Meta:
        abstract = True


class ShortIndexMixin(IndexMixin):
    """
    为模型附加以下字段和方法：

    - ``index`` ，可空。用于存放自定义索引（16位有符号整数）。默认值 ``0`` 。
    - ``get_ordered_set()`` ，获取一个按 ``index`` 字段从大到小排序的查询集。
    - ``get_reversed_set()`` ，获取一个按 ``index`` 字段从小到大排序的查询集。

    适用于：``django.db.models.Model`` 的子类
    """
    index = models.SmallIntegerField(default=0, blank=True)

    class Meta:
        abstract = True


class UrgencyMixin(models.Model):
    """
    为模型附加以下字段：

    - ``urgency`` ，可空。用于记录紧急程度。
      取值范围限定在 ``zeraora.constants.Degree.choices`` ，
      默认值为 ``zeraora.constants.Degree.NORMAL`` 。

    适用于：``django.db.models.Model`` 的子类
    """
    urgency = models.SmallIntegerField(default=Degree.NORMAL, choices=Degree.choices, blank=True)

    class Meta:
        abstract = True


class ImportanceMixin(models.Model):
    """
    为模型附加以下字段：

    - ``importance`` ，可空。用于记录重要程度。
      取值范围限定在 ``zeraora.constants.Degree.choices`` ，
      默认值为 ``zeraora.constants.Degree.NORMAL`` 。

    适用于：``django.db.models.Model`` 的子类
    """
    importance = models.SmallIntegerField(default=Degree.NORMAL, choices=Degree.choices, blank=True)

    class Meta:
        abstract = True


def biz_id() -> str:
    """
    使用 ``uuid4()`` 生成一个biz_id，即32位小写HEX字符串，正则表达式为 ``^[0-9a-z]{32}$`` 。
    """
    return uuid.uuid4().hex


class BizMixin(models.Model):
    """
    为模型附加以下字段和方法：

    - ``biz`` ，索引，唯一。用于提供业务ID（32位小写HEX字符串），默认值通过使用 ``uuid4()`` 来生成。

    适用于：``django.db.models.Model`` 的子类
    """
    biz = models.CharField(max_length=32, default=biz_id, unique=True, db_index=True, blank=True)

    class Meta:
        abstract = True


class AddressMixin(models.Model):
    """
    为模型附加以下字段、属性、方法：

    - ``province`` 。省份代码，两位整数字符。
    - ``prefecture`` 。市区代码，两位整数字符。
    - ``county`` 。县区代码，两位整数字符。
    - ``street`` 。街道地址。最多存放150个字符。
    - ``ad_code`` 。行政区划代码，返回一个 ``DivisionCode`` 元组。
    - ``check_area_exist()`` 。检查省市县代码是否正确。
    - ``show_address()`` 。返回一个用于显示的地址。

    使用此类的相关方法或属性前，请在合适的时候调用 ``zeraora.utils.load_ads4()`` 来加载必要数据。

    ----

    适用于：``django.db.models.Model`` 的子类
    """
    province = models.CharField('省份', max_length=2, choices=Province.choices, blank=True)
    prefecture = models.CharField('市区', max_length=2, default='00', blank=True)
    county = models.CharField('县区', max_length=2, default='00', blank=True)
    township = models.CharField('乡镇', max_length=3, default='000', blank=True)
    street = models.CharField('街道', max_length=150, default=None, null=True, blank=True)

    @property
    def ad_code(self) -> DivisionCode:
        """
        行政区划代码。

        返回一个 ``DivisionCode`` 元组。
        写入时提供一个 ``DivisionCode`` 元组，或者一个至少有六位数字的字符串。
        """
        return DivisionCode(self.province, self.prefecture, self.county, self.township)

    @ad_code.setter
    def ad_code(self, _code: str | DivisionCode):
        adc = _code if isinstance(_code, DivisionCode) else DivisionCode.fromcode(_code)
        self.province = adc.province
        self.prefecture = adc.prefecture
        self.county = adc.county
        self.township = adc.township

    def check_area_exist(self) -> bool:
        """
        检查省、市、县、乡镇四个层级的代码是否存在。
        """
        warn_empty_ads()
        return self.ad_code in gvs.ad_map

    def show_address(self, sep: str = ' ') -> str:
        """
        拼接一个用于显示的完整地址，包含省、市、县、街道。

        :param sep: 省、市、县、街道之间的间隔符，默认为一个空格。
        :return: 一个完整地址。
        """
        province = DivisionCode(self.province)
        prefecture = DivisionCode(self.province, self.prefecture)
        county = DivisionCode(self.province, self.prefecture, self.county)

        warn_empty_ads()
        try:
            province = gvs.ad_map[province]
            prefecture = gvs.ad_map[prefecture]
            county = gvs.ad_map[county]
        except IndexError:
            pass

        return sep.join([province, prefecture, county, self.street])

    class Meta:
        abstract = True


class GlobalAddressMixin(models.Model):
    """
    为模型附加以下字段、属性、方法：

    - ``nation`` 。国家。
    - ``province`` ，可空，默认为空。省。
    - ``prefecture`` ，可空，默认为空。市。
    - ``county`` ，可空，默认为空。县。
    - ``street`` ，可空，默认为空。街道。。最多存放200个字符。
    - ``street2`` ，可空，默认为空。街道2。。最多存放200个字符。
    - ``street3`` ，可空，默认为空。街道3。。最多存放200个字符。

    适用于：``django.db.models.Model`` 的子类
    """
    nation = models.CharField('国家', max_length=50)
    province = models.CharField('省', max_length=100, default=None, null=True, blank=True)
    prefecture = models.CharField('市', max_length=100, default=None, null=True, blank=True)
    county = models.CharField('县', max_length=100, default=None, null=True, blank=True)
    street = models.CharField('街道', max_length=200, default=None, null=True, blank=True)
    street2 = models.CharField('街道2', max_length=200, default=None, null=True, blank=True)
    street3 = models.CharField('街道3', max_length=200, default=None, null=True, blank=True)

    class Meta:
        abstract = True
