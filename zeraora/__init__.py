from typing import NamedTuple as _NamedTuple


class _VersionInfo(_NamedTuple):
    major: int
    minor: int
    micro: int
    releaselevel: str
    serial: int

    # https://packaging.python.org/en/latest/specifications/version-specifiers/
    def __str__(self):
        level = {'alpha': 'a', 'beta': 'b', 'final': ''}[self.releaselevel]
        return f'{self.major}.{self.minor}.{self.micro}{level}.{self.serial}'


VERSION = _VersionInfo(0, 4, 0, 'alpha', 5)

__version__ = str(VERSION)
