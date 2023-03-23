import os
from random import getrandbits

from zeraora.charsets import BASE62, BASE64


def randbytes(n: int) -> bytes:
    """
    生成 n 个随机字节。

    此函数是对 Python 3.9 以前的 random.randbytes(n) 的替代。
    """
    assert n >= 0
    return getrandbits(n * 8).to_bytes(n, 'little')


def randb62(n: int) -> str:
    """
    生成 n 个 base62 随机字符。
    """
    return ''.join(BASE62[i % 62] for i in os.urandom(n))


def randb64(n: int) -> str:
    """
    生成 n 个 base64 随机字符。
    """
    return ''.join(BASE64[i >> 2] for i in os.urandom(n))
