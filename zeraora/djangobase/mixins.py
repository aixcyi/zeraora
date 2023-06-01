import re
from typing import Any, Dict

try:
    from django.utils.decorators import classonlymethod
    from django.apps import apps
    from django.db import models
    from rest_framework import status
    from rest_framework.response import Response
    from rest_framework.viewsets import ViewSetMixin
except ImportError:
    print('需要安装Django以及DRF框架：pip install django djangorestframework')
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


class EasyViewSetMixin(ViewSetMixin):
    """
    提供了两个方法来简化 ``.as_view()`` 的传参。
    """

    @classonlymethod
    def to_view(cls, initkwargs: Dict[str, Any] = None, **actions: str):
        """
        将视图类存储在一个视图函数上，方便URL反向查找。

        之所以调转 ``initkwargs`` 和 ``actions`` 的传参方式，是因为后者往往用得更频繁。

        :param initkwargs: 视图类的初始化参数。
        :param actions: HTTP方法及其在视图类中的方法函数名称。
                        不同方法（的组合）可以让不同的视图函数应对不同的HTTP请求。
                        至少要提供一个key-value。
        :return: 一个新的视图函数。
        :raise TypeError: 来自 .as_view() 的异常。
        """
        if initkwargs is None:
            initkwargs = {}
        return cls.as_view(actions, **initkwargs)

    @classonlymethod
    def av(cls, actions: str, **initkwargs):
        """
        将视图类存储在一个视图函数上，方便URL反向查找。

        使用区分大小写的字母代表指定视图类方法及其对应的HTTP方法。

        ``actions`` 的缩写如下：
          - ``o``，对应 OPTIONS 请求及 ``.options()`` 方法。
          - ``l``，对应 GET 请求及 ``.list()`` 方法。
          - ``r``，对应 GET 请求及 ``.retrieve()`` 方法。
          - ``c``，对应 POST 请求及 ``.create()`` 方法。
          - ``u``，对应 PUT 请求及 ``.update()`` 方法。
          - ``U``，对应 PUT 请求及 ``.partial_update()`` 方法。
          - ``p``，对应 PATCH 请求及 ``.partial_update()`` 方法。
          - ``d``，对应 DELETE 请求及 ``.destroy()`` 方法。
          - ``D``，对应 DELETE 请求及 ``.soft_delete()`` 方法。

        :param actions: 缩写。相同HTTP请求的缩写不能组合，否则只择其一。
        :param initkwargs: 视图类的初始化参数。
        :return: 一个新的视图函数。
        :raise KeyError: 缩写未被定义。
        :raise TypeError: 来自 .as_view() 的异常。
        """
        # 缩写 p 是请求方法的性质向功能的妥协。
        # PATCH 请求是对资源进行部分修改，PUT 请求是对资源进行整体覆盖，与 partial 相悖；
        # 但是 PUT 请求是幂等的，而 PATCH 不是，也就是说多次
        # PATCH 相同内容产生的效果可以不一样，这与 update 相悖。
        mapper = {
            'o': ('options', 'options'),
            'l': ('get', 'list'),
            'r': ('get', 'retrieve'),
            'c': ('post', 'create'),
            'u': ('put', 'update'),
            'U': ('put', 'partial_update'),
            'p': ('patch', 'partial_update'),
            'd': ('delete', 'destroy'),
            'D': ('delete', 'soft_delete'),
        }
        return cls.as_view(dict(mapper[a] for a in actions), **initkwargs)


class SoftDeleteModelMixin:
    """
    将一个模型实例标记为已删除。（软删除）
    """
    deletion_field = 'deleted'
    deletion_mark = True

    def soft_delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_soft_delete(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_soft_delete(self, instance):
        if not hasattr(instance, self.deletion_field):
            raise TypeError(
                '模型 %s 没有用于标记删除的字段 %s 。' % (
                    type(instance).__name__,
                    self.deletion_field,
                )
            )

        setattr(instance, self.deletion_field, self.deletion_mark)

        instance.save()
