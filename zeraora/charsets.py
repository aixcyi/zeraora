"""
常用字符集。包括按分类定义和按编码定义两大类。
"""

# print(''.join(map(chr, range(32, 127))))

# 按分类定义的字符集
DIGITS = '0123456789'
UPPERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
LOWERS = 'abcdefghijklmnopqrstuvwxyz'
SYMBOL = r'''!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~'''
SYMBOL_NORMAL = r"`-=[]\;',./"
SYMBOL_SHIFT = r'~!@#$%^&*()_+{}|:"<>?'
LETTERS = UPPERS + LOWERS
assert sorted(SYMBOL) == sorted(SYMBOL_NORMAL + SYMBOL_SHIFT)

# 去除易混淆字符后的字符集
DIGITS_SAFE = '23456789'
UPPERS_SAFE = 'ABCDEFGHJKLMNPQRSTUVWXYZ'
LOWERS_SAFE = 'abcdefghijklmnpqrstuvwxyz'
LETTERS_SAFE = UPPERS_SAFE + LOWERS_SAFE

# 按编码定义的字符集
BASE8 = '01234567'
BASE16 = '0123456789ABCDEF'
BASE36 = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
BASE62 = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
BASE64 = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz+/'
BASE64SAFE = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_'
OCTDIGITS = BASE8
HEXDIGITS = '0123456789ABCDEFabcdef'
