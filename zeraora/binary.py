"""
二进制相关。
"""

__all__ = [
    'randbytes',
]

from random import getrandbits


def randbytes(n: int) -> bytes:
    """
    生成 n 个随机字节。

    此函数用于在 Python 3.9 以前提供标准库中 random.randbytes(n) 的等效能力。
    """
    if n < 1:
        return b''
    return getrandbits(n * 8).to_bytes(n, 'little')
