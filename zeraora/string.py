"""
字符、字符串相关工具与常量。
"""
__all__ = [
    'Notations',
    'Chars',
    'SafeChars',
    'randb64',
    'randb64o',
    'randb62',
    'randb62o',
    'randb16',
    'randb16o',
]

import os
from base64 import b64encode, urlsafe_b64encode
from itertools import chain
from math import ceil
from random import getrandbits


class Notations:
    """
    进位制数码。
    """
    BASE8 = '01234567'
    BASE10 = '0123456789'
    BASE16 = ''.join(chain(BASE10, map(chr, range(ord('A'), ord('F') + 1))))
    BASE36 = ''.join(chain(BASE10, map(chr, range(ord('A'), ord('Z') + 1))))
    BASE62 = ''.join(chain(BASE36, map(chr, range(ord('a'), ord('z') + 1))))
    BASE64 = BASE62 + '+/'
    BASE64SAFE = BASE62 + '-_'


class Chars:
    """
    不同类型的字符。
    """
    DIGIT = Notations.BASE10
    UPPER = ''.join(map(chr, range(ord('A'), ord('Z') + 1)))
    LOWER = ''.join(map(chr, range(ord('a'), ord('z') + 1)))
    LETTER = UPPER + LOWER
    SYMBOL = ''.join(chain(
        map(chr, range(0x21, 0x2F + 1)),
        map(chr, range(0x3A, 0x40 + 1)),
        map(chr, range(0x5B, 0x60 + 1)),
        map(chr, range(0x7B, 0x7E + 1)),
    ))


class SafeChars:
    DIGIT = Chars.DIGIT.replace('0', '').replace('1', '')
    UPPER = Chars.UPPER.replace('I', '').replace('O', '')
    LOWER = Chars.LOWER.replace('l', '')
    LETTER = UPPER + LOWER
    SYMBOL_NORMAL = r"`-=[]\;',./"
    SYMBOL_SHIFT = r'~!@#$%^&*()_+{}|:"<>?'


def randb64(n: int, safe=False) -> str:
    """
    快速生成 n 个 Base64 随机字符。

    - 参数 ``safe`` 决定是否生成 URL-Safe Base64 字符串。
    - 使用标准库 random 生成，受 random.seed() 影响。
    - 在大量调用时，此函数可能会比 randb64o() 耗费略多的时间。
    """
    if n < 1:
        return ''
    if not safe:
        return b64encode(getrandbits(n * 6).to_bytes(ceil(n * 6 / 8), 'little')).decode('ASCII')[:n]
    else:
        return urlsafe_b64encode(getrandbits(n * 6).to_bytes(ceil(n * 6 / 8), 'little')).decode('ASCII')[:n]


def randb64o(n: int, safe=False) -> str:
    """
    生成 n 个 Base64 随机字符。

    - 参数 ``safe`` 决定是否生成 URL-Safe Base64 字符串。
    - 使用标准库的 os.urandom(n) 函数生成，不会受 random.seed() 影响。
    - 在大量调用时，此函数可能会比 randb64() 花费略少的时间。
    """
    if n < 1:
        return ''
    if not safe:
        return b64encode(os.urandom(ceil(n * 6 / 8))).decode('ASCII')[:n]
    else:
        return urlsafe_b64encode(os.urandom(ceil(n * 6 / 8))).decode('ASCII')[:n]


def randb62(n: int) -> str:
    """
    生成 n 个 Base62 随机字符。

    - 使用标准库 random 生成，受 random.seed() 影响。
    - 在大量调用时，此函数可能会比 randb62o() 耗费略多的时间。
    """
    if n < 1:
        return ''
    return ''.join(Notations.BASE62[i % 62] for i in getrandbits(n * 8).to_bytes(n, 'little'))


def randb62o(n: int) -> str:
    """
    生成 n 个 Base62 随机字符。

    - 使用标准库的 os.urandom(n) 函数生成，不会受 random.seed() 影响。
    - 在大量调用时，此函数可能会比 randb62() 花费略少的时间。
    """
    if n < 1:
        return ''
    return ''.join(Notations.BASE62[i % 62] for i in os.urandom(n))


def randb16(n: int) -> str:
    """
    生成 n 个 Base16（即 Hex）随机字符。

    - 使用标准库 random 生成，受 random.seed() 影响。
    - 在大量调用时，此函数可能会比 randb16o() 耗费略多的时间。

    >>> randb16(8)
    'd7d3d2ed'

    >>> randb16(8).upper()
    'D7D3D2ED'
    """
    if n < 1:
        return ''
    return getrandbits(n * 4).to_bytes(ceil(n / 2), 'little').hex()[:n]


def randb16o(n: int) -> str:
    """
    生成 n 个 Base16（即 Hex）随机字符。

    - 使用标准库的 os.urandom(n) 函数生成，不会受 random.seed() 影响。
    - 在大量调用时，此函数可能会比 randb16() 花费略少的时间。

    >>> randb16o(8)
    'd7d3d2ed'

    >>> randb16o(8).upper()
    'D7D3D2ED'
    """
    if n < 1:
        return ''
    return os.urandom(ceil(n / 2)).hex()[:n]
