__all__ = [
    'Alphabet',
    'Notation',
    'Char',
    'StringBuilder',
    'PathBuilder',
]

from collections import deque
from itertools import chain, repeat, zip_longest
from types import EllipsisType
from typing import Iterable

from typing_extensions import Self, Writer


class Alphabet:
    """
    不同编码的字符集，大多参照 `RFC4648 <https://datatracker.ietf.org/doc/html/rfc4648>`_ 。
    """
    BASE16 = b'0123456789ABCDEF'
    BASE32 = b'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567'
    BASE32HEX = b'0123456789ABCDEFGHIJKLMNOPQRSTUV'
    BASE62 = b'ABCDEFGHIJKLMNOPQRSTUVWXYZ' b'abcdefghijklmnopqrstuvwxyz' b'0123456789'
    BASE64 = b'ABCDEFGHIJKLMNOPQRSTUVWXYZ' b'abcdefghijklmnopqrstuvwxyz' b'0123456789+/'
    BASE64SAFE = b'ABCDEFGHIJKLMNOPQRSTUVWXYZ' b'abcdefghijklmnopqrstuvwxyz' b'0123456789-_'
    BASE85 = b'0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ' b'abcdefghijklmnopqrstuvwxyz!#$%&()*+-;<=>?@^_`{|}~'
    ASCII85 = b'!"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstu'
    Z85 = b'0123456789abcdefghijklmnopqrstuvwxyz' b'ABCDEFGHIJKLMNOPQRSTUVWXYZ.-:+=^!/*?&<>()[]{}@%$#'


class Notation:
    """
    不同进位制的字符集。
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
    DIGIT_SAFE = '23456789'
    UPPER_SAFE = 'ABCDEFGHJKLMNPQRSTUVWXYZ'
    LOWER_SAFE = 'abcdefghijkmnopqrstuvwxyz'
    LETTER_SAFE = 'ABCDEFGHJKLMNPQRSTUVWXYZ' 'abcdefghijkmnopqrstuvwxyz'
    SYMBOL_NORMAL = r"`-=[]\;',./"
    SYMBOL_SHIFT = r'~!@#$%^&*()_+{}|:"<>?'


class StringBuilder:

    def __init__(self, *blocks, sep='', end=''):
        """
        字符串构建器。

        - 用于一次性聚合多个短小字符串，来构建一个较长的字符串。
        - 支持链式调用与 C++ 风格的流式输入。

        :param blocks: 初始内容。
        :param sep: 分隔符。
        :param end: 结尾。
        """
        self._queue = deque()
        self.write(*blocks, sep=sep, end=end)

    # () << 'navifox'
    def __lshift__(self, block) -> Self:
        self.write(block)
        return self

    def writeline(self, *blocks, sep='', end='\n') -> Self:
        """
        直接追加字符串，默认在结尾添加换行符。
        """
        self.write(*blocks, sep=sep, end=end)
        return self

    def writelines(self, *blocks, sep='\n', end='\n') -> Self:
        """
        直接追加字符串，默认以换行符分隔，且默认在结尾添加换行符。
        """
        self.write(*blocks, sep=sep, end=end)
        return self

    def write(self, *blocks, sep='', end='') -> Self:
        """
        直接追加字符串。

        :param blocks: 要追加的内容。
        :param sep: 分隔符。
        :param end: 结尾。
        :return: 自身。
        """
        if sep:
            blocks = chain.from_iterable(zip_longest(
                blocks,
                repeat(sep, len(blocks) - 1),
                fillvalue=end,
            ))
        elif end:
            blocks = *blocks, end

        self.writes(blocks)
        return self

    def writes(self, iterable: Iterable) -> Self:
        """
        从可迭代对象中追加字符串。
        """
        self._queue.extend(str(s) for s in iterable if s)
        return self

    # () >> fileobject
    def __rshift__(self, hole: Writer[str]) -> Self:
        hole.write(str(self))
        return self

    def __str__(self) -> str:
        return ''.join(self._queue)

    def build(self) -> str:
        """
        构建字符串，但不会清空构建器内部的缓存。
        """
        return ''.join(self._queue)

    def clear(self) -> Self:
        """
        清空构建器内部的缓存。
        """
        self._queue.clear()
        return self


class PathBuilder:

    def __init__(self, path='', /, *, slash='/', slashes='//'):
        """
        路径构建器。

        - 用于一次性聚合多个短小字符串，来构建一个较长的、带有特定间隔符的字符串（例如路径）。
        - 目前支持通过 ``/`` 和 ``//`` 两个运算符来进行拼接。

        :param path: 初始路径。
        :param slash: 斜线。用于控制使用 ``/`` 拼接时内部的分隔符。
        :param slashes: 斜线。用于控制使用 ``//`` 拼接时内部的分隔符。
        """
        self._queue = deque([path])
        self._slash = slash
        self._slashes = slashes
        assert type(path) is str
        assert type(slash) is str
        assert type(slashes) is str

    def __str__(self) -> str:
        return ''.join(self._queue)

    # () / 'navifox' / ...
    def __truediv__(self, path: str | EllipsisType) -> Self:
        return self._concat(self._slash, path)

    # () // 'navifox' / ...
    def __floordiv__(self, path: str | EllipsisType) -> Self:
        return self._concat(self._slashes, path)

    def _concat(self, delimiter: str, path: str | EllipsisType) -> Self:
        """
        检测分隔符拼接。

        :param delimiter: 分隔符。
        :param path: 拼接的路径。
        :return: 自身。
        """
        parent = '' if not self._queue else self._queue.pop().removesuffix(delimiter)
        child = '' if path is ... else str(path).removeprefix(delimiter)
        self._queue.extend(s for s in (parent, delimiter, child) if s)
        return self
