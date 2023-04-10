"""
装饰器。用于检查代码、环境等。
"""

import sys
from functools import wraps


def start(*version: int, note=None):
    """
    检查 Python 版本是否高于或等于指定值，
    如果低于指定的版本就会抛出 RuntimeError。
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if sys.version_info < version:
                raise RuntimeError(
                    f'Require Python version {version:s} to run. '
                    f'运行此函数/类需要Python版本在 {version:s} 及以上。'
                    + ('' if note is None else note)
                )
            return func(*args, **kwargs)

        return wrapper

    return decorator
