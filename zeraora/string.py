"""
字符、字符串相关工具与常量。
"""

__all__ = [
    'Alphabet',
    'Notation',
    'Char',
]


class Alphabet:
    """
    不同编码的字符表，基本参照 `RFC4648 <https://datatracker.ietf.org/doc/html/rfc4648>`_ 。
    """
    BASE16 = b'0123456789ABCDEF'
    BASE32 = b'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567'
    """按顺序包含大写字母以及除了 ``1``、``8``、``9`` 之外的阿拉伯数字。"""
    BASE32HEX = b'0123456789ABCDEFGHIJKLMNOPQRSTUV'
    """按顺序包含阿拉伯数字以及除了 ``WXYZ`` 之外的大写字母。"""
    BASE62 = b'ABCDEFGHIJKLMNOPQRSTUVWXYZ' b'abcdefghijklmnopqrstuvwxyz' b'0123456789'
    BASE64 = b'ABCDEFGHIJKLMNOPQRSTUVWXYZ' b'abcdefghijklmnopqrstuvwxyz' b'0123456789+/'
    BASE64SAFE = b'ABCDEFGHIJKLMNOPQRSTUVWXYZ' b'abcdefghijklmnopqrstuvwxyz' b'0123456789-_'
    BASE85 = b'0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ' b'abcdefghijklmnopqrstuvwxyz!#$%&()*+-;<=>?@^_`{|}~'
    Z85 = b'0123456789abcdefghijklmnopqrstuvwxyz' b'ABCDEFGHIJKLMNOPQRSTUVWXYZ.-:+=^!/*?&<>()[]{}@%$#'


class Notation:
    """
    不同进位制的数码。
    """
    BASE8 = '01234567'
    BASE10 = '0123456789'
    BASE16 = '0123456789' 'ABCDEF'
    BASE36 = '0123456789' 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    BASE62 = '0123456789' 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' 'abcdefghijklmnopqrstuvwxyz'
    BASE64 = '0123456789' 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' 'abcdefghijklmnopqrstuvwxyz' '+/'
    BASE64SAFE = '0123456789' 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' 'abcdefghijklmnopqrstuvwxyz' '-_'


class Char:
    """
    不同类型的字符。
    """
    DIGIT = '0123456789'
    UPPER = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    LOWER = 'abcdefghijklmnopqrstuvwxyz'
    LETTER = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' 'abcdefghijklmnopqrstuvwxyz'
    SYMBOL = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
    """按顺序包含 ``\\x21`` 到 ``\\x7e`` 之间的所有可见符号，除了空格、控制符、数字、大小写字母。"""
    DIGIT_SAFE = '23456789'
    """按顺序包含除了 ``0`` 和 ``1`` 以外的阿拉伯数字。"""
    UPPER_SAFE = 'ABCDEFGHJKLMNPQRSTUVWXYZ'
    """按顺序包含除了 ``I`` 和 ``O`` 以外的大写字母。"""
    LOWER_SAFE = 'abcdefghijkmnopqrstuvwxyz'
    """按顺序包含除了 ``l`` 以外的小写字母。"""
    LETTER_SAFE = 'ABCDEFGHJKLMNPQRSTUVWXYZ' 'abcdefghijkmnopqrstuvwxyz'
    """按顺序包含除了大写字母 ``I``、``O`` 和小写字母 ``l`` 以外的大小写字母。"""
    SYMBOL_NORMAL = r"`-=[]\;',./"
    SYMBOL_SHIFT = r'~!@#$%^&*()_+{}|:"<>?'
