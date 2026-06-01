__all__ = [
    'uuid7',
    'uuid8',
    'uuid8i',
    'RichUUID',
]

import sys
from random import getrandbits
from time import time_ns
from uuid import UUID, uuid1, uuid3, uuid4, uuid5, uuid6

from typing_extensions import Self

if sys.version_info >= (3, 14):
    from uuid import uuid7
else:
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

if sys.version_info >= (3, 14):
    from uuid import uuid8
else:
    def uuid8(
            a: int | None = None,
            b: int | None = None,
            c: int | None = None,
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


class RichUUID(UUID):
    """
    信息更加丰富的 UUID 对象。
    """

    NIL: 'RichUUID'
    MAX: 'RichUUID'

    @classmethod
    def fromuuid(cls, __uuid: UUID, /):
        return cls(int=__uuid.int)

    @classmethod
    def v1(cls, node: int | None = None, clock_seq: int | None = None):
        return cls(int=uuid1(node, clock_seq).int)

    @classmethod
    def v3(cls, namespace: UUID | Self, name: str | bytes):
        return cls(int=uuid3(namespace, name).int)

    @classmethod
    def v4(cls):
        return cls(int=uuid4().int)

    @classmethod
    def v5(cls, namespace: UUID | Self, name: str | bytes):
        return cls(int=uuid5(namespace, name).int)

    @classmethod
    def v6(cls, node: int | None = None, clock_seq: int | None = None):
        return cls(int=uuid6(node, clock_seq).int)

    @classmethod
    def v7(cls):
        return cls(int=uuid7().int)

    @classmethod
    def v8(cls, a: int | None = None, b: int | None = None, c: int | None = None):
        return cls(int=uuid8(a, b, c).int)

    @classmethod
    def v8i(cls, i: int):
        return cls(int=uuid8i(i).int)

    @property
    def uuid(self) -> UUID:
        return UUID(int=self.int)

    @property
    def parts5(self) -> tuple[int, int, int, int, int]:
        """
        按出现顺序获取 version 和 variant 以及被它们分割的三个部分。
        """
        a, b, c, d, e, f = self.fields
        return (
            a << 16 | b,
            c >> 12,  # version
            c & 0x0FFF,
            d >> 6,  # variant
            (d & 0x3F) << 56 | e << 48 | f,
        )

    @property
    def parts3(self) -> tuple[int, int, int]:
        """
        按出现顺序获取 variant 以及被它分割的两个部分。
        """
        a, b, c, d, e, f = self.fields
        return (
            a << 32 | b << 16 | c,
            d >> 6,  # variant
            (d & 0x3F) << 56 | e << 48 | f,
        )


RichUUID.NIL = RichUUID(int=0)
RichUUID.MAX = RichUUID(int=0xFFFFFFFF_FFFFFFFF_FFFFFFFF_FFFFFFFF)
