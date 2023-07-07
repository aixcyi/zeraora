"""
对 Django REST Framework 过滤器中间件的增强。

这是什么？
https://www.django-rest-framework.org/api-guide/filtering/

如何自定义？
https://www.django-rest-framework.org/api-guide/filtering/#custom-generic-filtering
"""
try:
    from django.core.exceptions import FieldDoesNotExist
    from rest_framework.filters import BaseFilterBackend
except ImportError as e:
    raise ImportError('需要安装Django以及DRF框架：\npip install django djangorestframework') from e


class ExistingFilterBackend(BaseFilterBackend):
    """
    筛选掉查询集中标记为已删除的结果。

    - 删除标记默认为 ``True`` ，可以通过在视图类中添加 ``deletion_mark`` 属性来更改。
    - 标记删除的字段默认是 ``deleted`` ，可以通过在视图类中添加 ``deletion_field`` 属性来更改。
      若字段不存在，会抛出 ``django.core.exceptions.FieldDoesNotExist`` 。

    适用于：
      - ``rest_framework.viewsets.GenericViewSet`` 子类的 ``filter_backends`` 属性
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
      若字段不存在，会抛出 ``django.core.exceptions.FieldDoesNotExist`` 。

    适用于：
      - ``rest_framework.viewsets.GenericViewSet`` 子类的 ``filter_backends`` 属性
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
