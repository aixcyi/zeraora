"""
对 `Django REST Framework <https://www.django-rest-framework.org/>`_ 的扩展和增强。
"""
from __future__ import annotations

__all__ = [
    'BearerAuthentication',
    'EasyViewSetMixin',
    'SoftDeleteModelMixin',
    'ExistingFilterBackend',
    'ActiveStatusFilterBackend',
]

from typing import Any

from django.core.exceptions import FieldDoesNotExist
from django.utils.decorators import classonlymethod
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.filters import BaseFilterBackend
from rest_framework.response import Response
from rest_framework.viewsets import ViewSetMixin


class BearerAuthentication(TokenAuthentication):
    """
    Simple token based authentication.

    Clients should authenticate by passing the token key in the "Authorization"
    HTTP header, prepended with the string "Bearer ".  For example:

        Authorization: Bearer 401f7ac837da42b97f613d789819ff93537bee6a
    """
    keyword = 'Bearer'
    model = Token


class EasyViewSetMixin(ViewSetMixin):
    """
    提供了两个方法来简化 :func:`as_view() <rest_framework.viewsets.ViewSetMixin.as_view>` 的传参。

    适用于：

    - :class:`ViewSet <rest_framework.viewsets.ViewSet>` 的子类
    - :class:`GenericViewSet <rest_framework.viewsets.GenericViewSet>` 的子类
    - 需要 :class:`ViewSetMixin <rest_framework.viewsets.ViewSetMixin>` 的类
    """

    @classonlymethod
    def to_view(cls, initkwargs: dict[str, Any] = None, **actions: str):
        """
        将视图类存储在一个视图函数上，方便URL反向查找。

        之所以互换 *initkwargs* 和 *actions* 的传参方式，是因为后者往往用得更频繁。

        :param initkwargs: 视图类的初始化参数。
        :param actions: HTTP方法及其在视图类中的方法函数名称。
                        不同方法（的组合）可以让不同的视图函数应对不同的HTTP请求。
                        至少要提供一个key-value。
        :return: 一个新的视图函数。
        :raise TypeError: 来自 :func:`as_view() <rest_framework.viewsets.ViewSetMixin.as_view>` 的异常。
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
        :raise TypeError: 来自 :func:`as_view() <rest_framework.viewsets.ViewSetMixin.as_view>` 的异常。
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

    - 通过 ``self.deletion_field`` 配置存储标记的字段，默认是 ``deleted``。
    - 通过 ``self.deletion_mark`` 配置标记是什么，默认是布尔值 ``True`` 。

    适用于 :class:`rest_framework.generics.GenericAPIView` 的子类
    """
    deletion_field = 'deleted'
    deletion_mark = True

    # noinspection PyUnresolvedReferences
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


class ExistingFilterBackend(BaseFilterBackend):
    """
    筛选掉查询集中标记为已删除的结果。

    - 删除标记默认为 ``True`` ，可以通过在视图类中添加 ``deletion_mark`` 属性来更改。
    - 标记删除的字段默认是 ``deleted`` ，可以通过在视图类中添加 ``deletion_field`` 属性来更改。
      若字段不存在，会抛出 :class:`django.core.exceptions.FieldDoesNotExist` 。

    适用于：

    - :class:`rest_framework.viewsets.GenericViewSet` 子类的 ``filter_backends`` 属性
    - ``rest_framework.settings.DEFAULT_FILTER_BACKENDS``
    - ``django.conf.settings.REST_FRAMEWORK["DEFAULT_FILTER_BACKENDS"]``
    """

    def filter_queryset(self, request, queryset, view):
        field = getattr(view, 'deletion_field', 'deleted')
        mark = getattr(view, 'deletion_mark', True)

        if field not in queryset.model.fields:
            raise FieldDoesNotExist(
                '模型 %s 缺少用于标记删除的字段 %s' % (
                    queryset.model._meta.object_name,
                    field,
                ),
            )

        return queryset.exclude(**{field: mark})


class ActiveStatusFilterBackend(BaseFilterBackend):
    """
    筛选查询集中已启用的结果。

    - 启用标记默认为 ``True`` ，可以通过在视图类中添加 ``active_mark`` 属性来更改。
    - 标记启用的字段默认是 ``activated`` ，可以通过在视图类中添加 ``active_field`` 属性来更改。
      若字段不存在，会抛出 :class:`django.core.exceptions.FieldDoesNotExist` 。

    适用于：
      - :class:`rest_framework.viewsets.GenericViewSet` 子类的 ``filter_backends`` 属性
      - ``rest_framework.settings.DEFAULT_FILTER_BACKENDS``
      - ``django.conf.settings.REST_FRAMEWORK["DEFAULT_FILTER_BACKENDS"]``
    """

    def filter_queryset(self, request, queryset, view):
        field = getattr(view, 'active_field', 'activated')
        mark = getattr(view, 'active_mark', True)

        if field not in queryset.model.fields:
            raise FieldDoesNotExist(
                '模型 %s 缺少用于标记删除的字段 %s' % (
                    queryset.model._meta.object_name,
                    field,
                ),
            )

        return queryset.filter(**{field: mark})
