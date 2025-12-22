__all__ = [
    'uuid7',
    'uuid8',
    'uuid8i',
]

from random import getrandbits
from time import time_ns
from uuid import UUID


def uuid7() -> UUID:
    """
    根据 RFC 9562 定义的第七版 UUID 生成一个带有毫秒级时间戳和一个随机数的 UUID 对象。

    注意：此函数使用了 :class:`random.Random`，因此不应将其用于安全目的。
    """
    return UUID(int=(
            0
            | time_ns() // 1000_000 << 80
            | 0x7 << 76  # 表明是 RFC 9562 定义的第七版 UUID
            | getrandbits(12) << 64
            | 0b10 << 62  # 表明是 RFC 9562 定义的 UUID
            | getrandbits(62)
    ))


def uuid8(
        a: int = None,
        b: int = None,
        c: int = None,
) -> UUID:
    """
    根据 RFC 9562 定义的第八版 UUID 生成一个自定义结构的 UUID。

    三个参数预期为三个 48、12、62
    比特的非负整数；如果超出长度，则仅保留最低有效位；若为负数，则将会取绝对值；如果没有提供，则替换成适当大小的伪随机数。

    注意：伪随机数使用了 :class:`random.Random` 生成，因此若是不提供参数，那么不应将本函数用于安全目的。
    """
    a = abs(getrandbits(48) if a is None else a) & 0xFFFF_FFFF_FFFF
    b = abs(getrandbits(12) if b is None else b) & 0x0FFF
    c = abs(getrandbits(62) if c is None else c) & 0x3FFF_FFFF_FFFF_FFFF
    return UUID(int=(
            0
            | a << 80
            | 0x8 << 76  # 表明是 RFC 9562 定义的第八版 UUID
            | b << 64
            | 0b10 << 62  # 表明是 RFC 9562 定义的 UUID
            | c
    ))


def uuid8i(integer: int) -> UUID:
    """
    根据 RFC 9562 定义的第八版 UUID 生成一个自定义结构的 UUID。

    可以传入一个 128 比特的整数，但函数会固定其中的 6 比特使其满足第八版
    UUID 的要求，仅剩 122 比特可用于自定义结构。
    """
    return UUID(int=(
            integer
            & 0xFFFFFFFF_FFFF_0FFF_3FFF_FFFFFFFFFFFF
            | 0x8 << 76  # 表明是 RFC 9562 定义的第八版 UUID
            | 0b10 << 62  # 表明是 RFC 9562 定义的 UUID
    ))
