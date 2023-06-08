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

    - ``created_at`` ，只读，记录模型创建时刻（日期+时间）。

    适用于：``django.db.models.Model`` 的子类
    """
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        abstract = True


class TimeMixin(models.Model):
    """
    为模型附加以下字段：

    - ``created_at`` ，只读，记录模型创建时刻（日期+时间）。
    - ``updated_at`` ，记录模型修改时刻（日期+时间），仅当 ``Model.save()`` 被调用时被自动设置。

    适用于：``django.db.models.Model`` 的子类
    """
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('修改时间', auto_now=True)

    class Meta:
        abstract = True


class DeletionMixin(models.Model):
    """
    为模型附加以下字段：

    - ``deleted`` ，用于标记删除状态。默认为 ``False`` ，当被设置为 ``True`` 时表示被标记为已删除。

    适用于：``django.db.models.Model`` 的子类
    """
    deleted = models.BooleanField(default=False, blank=True)

    class Meta:
        abstract = True
