"""
对 `requests <https://pypi.org/project/requests/>`_ 的扩展和增强。
"""

__all__ = [
    'HTTPTokenAuth',
    'HTTPBearerAuth',
]

from requests.auth import AuthBase


class HTTPTokenAuth(AuthBase):
    """
    为 ``requests.post()`` 等方法提供 *auth* 参数。它让请求带上了以下格式的头： ::

        Authorization: Token 我的令牌
    """
    key = 'Token'

    def __init__(self, token: str):
        self.token = token

    def __call__(self, r):
        r.headers['Authorization'] = f'{self.key} {self.token}'
        return r

    def __eq__(self, other):
        return all([
            self.key == getattr(other, 'key', None),
            self.token == getattr(other, 'token', None),
        ])

    def __ne__(self, other):
        return not self == other


class HTTPBearerAuth(HTTPTokenAuth):
    """
    为 ``requests.post()`` 等方法提供 *auth* 参数。它让请求带上了以下格式的头： ::

        Authorization: Bearer 我的令牌
    """

    def __call__(self, r):
        r.headers['Authorization'] = f'Bearer {self.token}'
        return r
