from typing import (
    Literal as _Literal,
    NamedTuple as _NamedTuple,
)


class _VersionInfo(_NamedTuple):
    major: int
    minor: int
    micro: int
    level: _Literal['alpha', 'beta', 'candidate', 'final']
    serial: int

    # https://packaging.python.org/en/latest/specifications/version-specifiers/
    def __str__(self):
        level = {'alpha': 'a', 'beta': 'b', 'candidate': 'rc', 'final': ''}[self.level]
        return f'{self.major}.{self.minor}.{self.micro}{level}.{self.serial}'

    def __int__(self):
        level = {'alpha': 0xA, 'beta': 0xB, 'candidate': 0xC, 'final': 0xF}[self.level]
        return self.major << 24 | self.minor << 16 | self.micro << 8 | level << 4 | self.serial

    # noinspection SpellCheckingInspection
    @property
    def releaselevel(self):
        return self.level

    @property
    def is_final(self):
        return self.level == 'final'


VERSION = _VersionInfo(0, 4, 0, 'candidate', 1)

__version__ = str(VERSION)
