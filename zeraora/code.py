"""
编解码与字符相关。
"""
__all__ = [
    'Symbols',
    'SafeSymbols',
    'Notations',
]

from itertools import chain


class Symbols:
    DIGIT = '0123456789'
    UPPER = ''.join(map(chr, range(ord('A'), ord('Z') + 1)))
    LOWER = ''.join(map(chr, range(ord('a'), ord('z') + 1)))
    LETTER = UPPER + LOWER
    SYMBOL = ''.join(chain(
        map(chr, range(0x21, 0x2F + 1)),
        map(chr, range(0x3A, 0x40 + 1)),
        map(chr, range(0x5B, 0x60 + 1)),
        map(chr, range(0x7B, 0x7E + 1)),
    ))


class SafeSymbols:
    DIGIT = Symbols.DIGIT.replace('0', '').replace('1', '')
    UPPER = Symbols.UPPER.replace('I', '').replace('O', '')
    LOWER = Symbols.LOWER.replace('l', '')
    LETTER = UPPER + LOWER
    SYMBOL_NORMAL = r"`-=[]\;',./"
    SYMBOL_SHIFT = r'~!@#$%^&*()_+{}|:"<>?'


class Notations:
    BASE8 = '01234567'
    BASE16 = ''.join(chain(
        '0123456789',
        map(chr, range(ord('A'), ord('F') + 1)),
    ))
    BASE36 = ''.join(chain(
        '0123456789',
        map(chr, range(ord('A'), ord('Z') + 1)),
    ))
    BASE62 = ''.join(chain(
        '0123456789',
        map(chr, range(ord('A'), ord('Z') + 1)),
        map(chr, range(ord('a'), ord('z') + 1)),
    ))
    BASE64 = BASE62 + '+/'
    BASE64SAFE = BASE62 + '-_'
