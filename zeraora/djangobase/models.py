"""
对 Django ORM模型 的增强。
"""
import re

try:
    from django.apps import apps
    from django.db import models
except ImportError:
    print('需要安装Django框架：pip install django')
    raise


class SnakeModel(models.base.ModelBase):
    """
    自动生成一个下划线小写的（蛇形）数据表名。

    >>> class Meta:
    >>>
    >>>     # SnakeModel 生成的格式
    >>>     db_table = "{app_name}_{snake_model_name}"
    >>>
    >>>     # Django 生成的格式
    >>>     # db_table = "{app_name}_{lowermodelname}"

    - 不会覆盖已经指定了的表名。
    - 可以用于抽象模型中，但只会为继承了抽象模型的非抽象模型生成表名。
    """

    def __new__(cls, name, bases, attrs, **kwargs):
        module = attrs.get('__module__', None)
        app_config = apps.get_containing_app_config(module)
        if app_config is None:
            return super().__new__(cls, name, bases, attrs, **kwargs)

        app_name = app_config.label

        model_name = re.sub(r'[A-Z]', (lambda s: f'_{s.group(0).lower()}'), name, re.I)
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
    附加一个用于记录创建时间的字段 ``created_at`` 。

    - ``created_at`` 记录的是第一次创建对象时的日期和时间。
    """
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        abstract = True


class TimeMixin(models.Model):
    """
    附加一个记录创建时间的字段 ``created_at`` 和一个记录修改时间的字段 ``updated_at`` 。

    - ``created_at`` 记录的是第一次创建对象时的日期和时间。
    - ``updated_at`` 记录的是每次保存对象时的日期和时间。仅当调用 ``Model.save()`` 时被更新。
    """
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('修改时间', auto_now=True)

    class Meta:
        abstract = True


class DeletionMixin(models.Model):
    """
    附加一个用于标记删除的字段 ``deleted`` ，默认为 ``False`` ，当为 ``True`` 时表示已被标记删除。
    """
    deleted = models.BooleanField(default=False, blank=True)

    class Meta:
        abstract = True
