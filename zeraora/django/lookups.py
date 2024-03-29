"""
定制的 Django QuerySet `查询器 <https://docs.djangoproject.com/zh-hans/4.2/ref/models/lookups/#lookup-reference>`_ 。

参阅 `如何编写自定义的查询器 <https://docs.djangoproject.com/zh-hans/4.2/howto/custom-lookups/>`_ 。
"""

__all__ = [
    'BitsIn',
    'BitsAllIn',
]

from django.db.models import Lookup


class BitsIn(Lookup):
    """
    过滤一个或多个比特存在于目标字段中的记录。
    """
    lookup_name = 'bits_in'

    def as_sql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        params = lhs_params + rhs_params
        return '%s & %s > 0' % (lhs, rhs), params


class BitsAllIn(Lookup):
    """
    过滤所有比特位都存在于目标字段中的记录。
    """
    lookup_name = 'bits_all_in'

    def as_sql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        params = lhs_params + rhs_params + rhs_params
        return '%s & %s = %s' % (lhs, rhs, rhs), params
