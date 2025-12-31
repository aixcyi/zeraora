__all__ = [
    'BitListField',
    'BearerAuthentication',
    'IsAdminUserOrReadOnly',
]

from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.fields import IntegerField, ListField
from rest_framework.permissions import BasePermission, SAFE_METHODS

from zeraora.math import bitstream


class BitListField(ListField):
    """
    比特数组字段。

    将一个整数序列化为一个比特数组，将一个比特数组反序列化为一个整数。

    - 7 <-> [1, 2, 4]
    - 0 <-> []
    - -7 <-> [-1, -2, -4]
    - 后端的整数 <-> 前端的整数数组
    """
    default_error_messages = {
        **ListField.default_error_messages,
        'not_an_int': '原始值必须是一个整数',
    }

    def __init__(self, **kwargs):
        kwargs.update(child=IntegerField())
        super().__init__(**kwargs)

    def to_representation(self, data: int) -> list[int]:
        if not isinstance(data, int):
            self.fail('not_an_int')
        return list(bitstream(data))

    def to_internal_value(self, data) -> int:
        bits: list[int] = super().to_internal_value(data)
        return sum(bits)


class BearerAuthentication(TokenAuthentication):
    """
    简单的基于令牌的身份验证。

    客户端应设置如下格式的名为 Authorization 的 HTTP 标头： ::

        Authorization: Bearer 401f7ac837da42b97f613d789819ff93537bee6a
    """
    keyword = 'Bearer'
    model = Token


class IsAdminUserOrReadOnly(BasePermission):
    """
    要么请求来自一个已认证的管理员，要么它是一个只读请求。
    """

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_authenticated and
            request.user.is_staff
        )
