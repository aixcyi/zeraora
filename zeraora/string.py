"""
字符、字符串相关工具与常量。
"""
__all__ = [
    'Notations',
    'Chars',
    'SafeChars',
    'randb64',
    'randb64y',
    'randb62',
    'randb16',
    'case_camel_to_snake',
]

import os
import re
from base64 import b64encode, urlsafe_b64encode
from itertools import chain
from math import ceil
from random import getrandbits


class Notations:
    """
    进位制数码。
    """
    BASE8 = '01234567'
    """包含：阿拉伯数字 ``0`` 到 ``7`` 。"""
    BASE10 = '0123456789'
    """包含：阿拉伯数字 ``0`` 到 ``9`` 。"""
    BASE16 = ''.join(chain(BASE10, map(chr, range(ord('A'), ord('F') + 1))))
    """包含：阿拉伯数字 ``0`` 到 ``9``、大写字母 ``A`` 到 ``F`` 。"""
    BASE36 = ''.join(chain(BASE10, map(chr, range(ord('A'), ord('Z') + 1))))
    """包含：阿拉伯数字 ``0`` 到 ``9``、大写字母 ``A`` 到 ``Z`` 。"""
    BASE62 = ''.join(chain(BASE36, map(chr, range(ord('a'), ord('z') + 1))))
    """包含：阿拉伯数字 ``0`` 到 ``9``、大写字母 ``A`` 到 ``Z``、小写字母 ``a`` 到 ``z``。"""
    BASE64 = BASE62 + '+/'
    """包含：阿拉伯数字 ``0`` 到 ``9``、大写字母 ``A`` 到 ``Z``、小写字母 ``a`` 到 ``z``、符号 ``+`` 和 ``/``。"""
    BASE64SAFE = BASE62 + '-_'
    """包含：阿拉伯数字 ``0`` 到 ``9``、大写字母 ``A`` 到 ``Z``、小写字母 ``a`` 到 ``z``、符号 ``-`` 和 ``_``。"""


class Chars:
    """
    不同类型的字符。
    """
    DIGIT = Notations.BASE10
    """包含：阿拉伯数字 ``0`` 到 ``9`` 。"""
    UPPER = ''.join(map(chr, range(ord('A'), ord('Z') + 1)))
    """包含：大写字母 ``A`` 到 ``Z`` 。"""
    LOWER = ''.join(map(chr, range(ord('a'), ord('z') + 1)))
    """包含：小写字母 ``a`` 到 ``z``。"""
    LETTER = UPPER + LOWER
    """包含：大写字母 ``A`` 到 ``Z``、小写字母 ``a`` 到 ``z``。"""
    SYMBOL = ''.join(chain(
        map(chr, range(0x21, 0x2F + 1)),
        map(chr, range(0x3A, 0x40 + 1)),
        map(chr, range(0x5B, 0x60 + 1)),
        map(chr, range(0x7B, 0x7E + 1)),
    ))
    """包含 ``0x21`` 到 ``0x7e`` 之间的所有可见符号，即除了空格、控制符、数字、大小写字母。"""


class SafeChars:
    DIGIT = Chars.DIGIT.replace('0', '').replace('1', '')
    """除了 ``0`` 和 ``1`` 以外的阿拉伯数字。"""
    UPPER = Chars.UPPER.replace('I', '').replace('O', '')
    """包含：大写字母 ``A`` 到 ``Z``，除了 ``I`` 和 ``O``。"""
    LOWER = Chars.LOWER.replace('l', '')
    """包含：小写字母 ``a`` 到 ``z``，除了 ``l``。"""
    LETTER = UPPER + LOWER
    """包含：大写字母 ``A`` 到 ``Z`` 和小写字母 ``a`` 到 ``z``，除了大写字母 ``I``、``O`` 和小写字母 ``l``。"""
    SYMBOL_NORMAL = r"`-=[]\;',./"
    SYMBOL_SHIFT = r'~!@#$%^&*()_+{}|:"<>?'


def randb64(n: int, safe=False, use_os=False) -> str:
    """
    快速生成 n 个 Base64（不包含 ``=``）随机字符。

    - ``safe`` 决定是否生成 URL-Safe Base64 字符串。
    - ``use_os=False`` 时会受 random.seed() 影响。
    - ``use_os=True`` 则使用 :mod:`os` 库，在大量调用时可能会耗费略少的时间。
    """
    if n < 1:
        return ''
    if not safe:
        if use_os:
            return b64encode(os.urandom(ceil(n * 6 / 8))).decode('ASCII')[:n]
        else:
            return b64encode(getrandbits(n * 6).to_bytes(ceil(n * 6 / 8), 'little')).decode('ASCII')[:n]
    else:
        if use_os:
            return urlsafe_b64encode(os.urandom(ceil(n * 6 / 8))).decode('ASCII')[:n]
        else:
            return urlsafe_b64encode(getrandbits(n * 6).to_bytes(ceil(n * 6 / 8), 'little')).decode('ASCII')[:n]


def randb64y(n: int, safe=False, use_os=False) -> str:
    """
    快速生成 n 字节的 Base64 随机字符（可能包含 ``=``）。

    - 不移除尾缀的 ``=`` 则生成长度为 ``ceil(n/3)*4`` 。
    - 移除尾缀的 ``=`` 的话生成长度为 ``ceil(n/3*4)`` 。
    - ``safe`` 决定是否生成 URL-Safe Base64 字符串。
    - ``use_os=False`` 时会受 random.seed() 影响。
    - ``use_os=True`` 则使用 :mod:`os` 库，在大量调用时可能会耗费略少的时间。

    >>> randb64y(13)
    NP4W8LAhbqz6sSRuNg==

    >>> randb64y(13).rstrip('=')
    NP4W8LAhbqz6sSRuNg
    """
    if n < 1:
        return ''
    if not safe:
        if use_os:
            return b64encode(os.urandom(n)).decode('ASCII')
        else:
            return b64encode(getrandbits(n * 8).to_bytes(n, 'little')).decode('ASCII')
    else:
        if use_os:
            return urlsafe_b64encode(os.urandom(n)).decode('ASCII')
        else:
            return urlsafe_b64encode(getrandbits(n * 8).to_bytes(n, 'little')).decode('ASCII')


def randb62(n: int, use_os=False) -> str:
    """
    生成 n 个 Base62 随机字符。

    - ``use_os=False`` 时会受 random.seed() 影响。
    - ``use_os=True`` 则使用 :mod:`os` 库，在大量调用时可能会耗费略少的时间。
    """
    if n < 1:
        return ''
    if use_os:
        return ''.join(Notations.BASE62[i % 62] for i in os.urandom(n))
    else:
        return ''.join(Notations.BASE62[i % 62] for i in getrandbits(n * 8).to_bytes(n, 'little'))


def randb16(n: int, use_os=False) -> str:
    """
    生成 n 个 Base16（即 Hex）随机字符。

    - ``use_os=False`` 时会受 random.seed() 影响。
    - ``use_os=True`` 则使用 :mod:`os` 库，在大量调用时可能会耗费略少的时间。

    >>> randb16(8)
    'd7d3d2ed'

    >>> randb16(8).upper()
    'D7D3D2ED'
    """
    if n < 1:
        return ''
    if use_os:
        return os.urandom(ceil(n / 2)).hex()[:n]
    else:
        return getrandbits(n * 4).to_bytes(ceil(n / 2), 'little').hex()[:n]


def case_camel_to_snake(name: str) -> str:
    """
    将类似 ``CombineOrderSKUModel`` 大小写形式的字符串
    转换为 ``combine_order_sku_model`` 。
    """
    # "CombineOrderSKUModel"
    # -> "Combine OrderSKU Model"
    # -> "Combine Order SKU Model"
    # -> "combine_order_sku_model"
    mid = re.sub('(.)([A-Z][a-z]+)', r'\1 \2', name)
    words = re.sub('([a-z0-9])([A-Z])', r'\1 \2', mid)
    return '_'.join(word.lower() for word in words.split())
