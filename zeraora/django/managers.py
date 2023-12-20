"""
定制的 Django Manager 。

这是什么？
https://docs.djangoproject.com/zh-hans/4.2/topics/db/managers/

如何自定义？
https://docs.djangoproject.com/zh-hans/4.2/topics/db/managers/#custom-managers
"""

__all__ = [
    'ExistingManager',
]

from django.db.models import Manager


class ExistingManager(Manager):
    """
    管理未删除的行（即过滤掉 deleted=True 的行）。
    """

    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)
