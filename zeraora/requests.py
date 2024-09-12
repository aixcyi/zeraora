"""
对 `requests <https://pypi.org/project/requests/>`_ 的扩展和增强。
"""

__all__ = [
    'HTTPBearerAuth',
]

from requests.auth import AuthBase


class HTTPBearerAuth(AuthBase):
    """
    为 ``requests.post()`` 等方法的 *auth* 参数提供对象。
    """

    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers['Authorization'] = f'Bearer {self.token}'
        return r

    def __eq__(self, other):
        return self.token == getattr(other, 'token', None)

    def __ne__(self, other):
        return self.token != getattr(other, 'token', None)
