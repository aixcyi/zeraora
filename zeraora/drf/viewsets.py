"""
对 Django REST Framework 视图集（viewset）的增强。
"""
from __future__ import annotations

__all__ = [
    'EasyViewSetMixin',
    'SoftDeleteModelMixin',
]

from typing import Any

try:
    from django.utils.decorators import classonlymethod
    from rest_framework import status
    from rest_framework.response import Response
    from rest_framework.viewsets import ViewSetMixin
except ImportError as e:
    raise ImportError('需要安装Django以及DRF框架：\npip install django djangorestframework') from e


class EasyViewSetMixin(ViewSetMixin):
    """
    提供了两个方法来简化 ``.as_view()`` 的传参。

    适用于：
      - ``rest_framework.viewsets.ViewSet`` 的子类
      - ``rest_framework.viewsets.GenericViewSet`` 的子类
      - 需要 ``rest_framework.viewsets.ViewSetMixin`` 的类
    """

    @classonlymethod
    def to_view(cls, initkwargs: dict[str, Any] = None, **actions: str):
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

    - 通过 ``self.deletion_field`` 配置存储标记的字段，默认是 ``deleted``。
    - 通过 ``self.deletion_mark`` 配置标记是什么，默认是布尔值 ``True`` 。

    适用于：``rest_framework.generics.GenericAPIView`` 的子类
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
