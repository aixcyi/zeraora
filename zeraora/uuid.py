"""
全局唯一身份标识符 Universally Unique IDentifier 相关工具。
"""

__all__ = [
    'uuid7',
    'uuid8',
]

from random import getrandbits
from time import time_ns
from uuid import UUID


def uuid7() -> UUID:
    """
    生成 RFC 4122 定义的第七版 UUID。

    注意：此函数使用了 :class:`random.Random`，因此不应将其用于安全目的。

    第七版 UUID 的高 48 位使用大端字节序存储毫秒级 Unix 时间戳，对应第 128~81
    位；低 80 位中的第 76~65、62~1 位共计 74 比特存储随机数，剩余的第
    80、79、78、77、64、63 位共计 6 个比特存储 RFC 4122 UUID 标准的版本及种类。

    获取时间戳的方式如下：

    >>> # 毫秒时间戳
    >>> mseconds: int = uuid7().int >> 80
    >>> # 秒时间戳
    >>> seconds: float = (uuid7().int >> 80) / 1000

    ----

    第七版 UUID 的鉴别方式如下：

    >>> import uuid
    >>>
    >>> assert uuid7().variant == uuid.RFC_4122
    >>> assert uuid7().version == 7

    第一个断言是第二个断言成立的前置条件。
    """
    return UUID(int=(
            (time_ns() // 1000_000 << 80 | getrandbits(80))
            & 0xFFFFFFFF_FFFF_0FFF_3FFF_FFFFFFFFFFFF
            | 0b10 << 62  # OSF's DCE UUID
            | 0x7 << 76  # OSF's DCE UUIDv7
    ))


def uuid8(integer: int) -> UUID:
    """
    生成 RFC 4122 定义的第八版 UUID。

    第八版 UUID 约定其结构由使用者自定义，其中有 122 个比特位可以自由使用，剩余
    6 个比特位存储 RFC 4122 UUID 标准的版本及种类。被占用的比特位位于第 80、79、78、77、64、63
    位。换句话说，第 128~81、76~65、62~1 位都是自由使用的。

    ----

    第八版 UUID 的鉴别方式如下：

    >>> from random import getrandbits
    >>> import uuid
    >>>
    >>> assert uuid8(getrandbits(128)).variant == uuid.RFC_4122
    >>> assert uuid8(getrandbits(128)).version == 8

    第一个断言是第二个断言成立的前置条件。
    """
    return UUID(int=(
            integer
            & 0xFFFFFFFF_FFFF_0FFF_3FFF_FFFFFFFFFFFF
            | 0b10 << 62  # OSF's DCE UUID
            | 0x8 << 76  # OSF's DCE UUIDv8
    ))
