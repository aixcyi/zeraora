"""
用于随机生成和特定顺序生成的生成器。
"""

__all__ = [
    'randbytes', 'SnowflakeWorker',
    'randb62', 'SnowflakeMultiWorker',
    'randb64', 'SnowflakeSingleWorker',
]

import logging
import os
from random import getrandbits
from time import time

from .constants.charsets import BASE62, BASE64

snow_logger = logging.getLogger('zeraora.snowflake')


def randbytes(n: int) -> bytes:
    """
    生成 n 个随机字节。

    此函数用于在 Python 3.9 以前代替 random.randbytes(n) 方法。
    """
    assert n >= 0
    return getrandbits(n * 8).to_bytes(n, 'little')


def randb62(n: int) -> str:
    """
    生成 n 个 base62 随机字符。
    """
    return ''.join(BASE62[i % 62] for i in os.urandom(n))


def randb64(n: int) -> str:
    """
    生成 n 个 base64 随机字符。
    """
    return ''.join(BASE64[i >> 2] for i in os.urandom(n))


class SnowflakeWorker(object):
    STAMP = (1 << 41) - 1
    WORKER = (1 << 10) - 1
    SEQUENCE = (1 << 12) - 1
    EPOCH1970 = 0
    EPOCH2000 = 946656000
    EPOCH2020 = 1577808000

    def __init__(self, worker: int, *, epoch: int = EPOCH1970):
        """
        雪花ID生成的基本实现。

        雪花ID是一个64位整数，包含1位符号+41位时间戳+10位设备编号+12位毫秒内序号。

        :param worker: 设备编号。取值范围 0-1023。
        :param epoch: 时间戳起点（计算用的时间戳与标准时间戳的差，单位为毫秒）。
        """
        assert all([worker.__class__ is int,
                    epoch.__class__ is int])
        self._epoch = epoch
        self._stamp = 0
        self._worker = abs(worker) & self.WORKER
        self._sequence = 0

    def next_int(self) -> int:
        """
        获取下一个ID。

        :raise SnowflakeWorker.TimeRedirected: 时钟发生回拨。
        :raise SnowflakeWorker.SequenceOverflow: 同一毫秒内序号超出编码空间。
        """
        prev, curr = self._stamp, int(time() * 1000) - self._epoch

        if prev < curr:
            sequence = 1
        elif prev == curr:
            sequence = self._sequence + 1
        else:
            sequence = self.redirect()  # 时钟回拨

        if sequence & self.SEQUENCE != sequence:
            self.overflow()  # 序号上溢

        self._stamp = curr
        self._sequence = sequence
        return (self._stamp << 22) | (self._worker << 12) | sequence

    def redirect(self):
        exc = self.TimeRedirected(self)
        snow_logger.exception(type(self).__name__, exc_info=exc)
        raise exc

    def overflow(self):
        exc = self.SequenceOverflow(self)
        snow_logger.exception(type(self).__name__, exc_info=exc)
        raise exc

    def dump(self) -> dict:
        return {
            "stamp": self._stamp,
            "worker": self._worker,
            "sequence": self._sequence,
        }

    def load(self, data: dict, **kwargs):
        values = data | kwargs
        self._stamp = values.get('stamp', self._stamp)
        self._worker = values.get('worker', self._worker)
        self._sequence = values.get('sequence', self._sequence)

    class _Error(Exception):
        def __init__(self, parent: "SnowflakeWorker"):
            self.args = (
                parent._stamp,
                parent._worker,
                parent._sequence,
            )

    class TimeRedirected(_Error):
        def __str__(self):
            return 'Time redirected. ' \
                   '(stamp=%s, worker=%s, sequence=%s)' % self.args

    class SequenceOverflow(_Error):
        def __str__(self):
            return 'Snowflake ID sequence overflow. ' \
                   '(stamp=%s, worker=%s, sequence=%s)' % self.args


class SnowflakeMultiWorker(SnowflakeWorker):
    _objects_ = []

    def __new__(cls, worker: int, *, epoch: int = 0):
        """
        雪花ID生成的多例实现。

        雪花ID是一个64位整数，包含1位符号+41位时间戳+10位设备编号+12位毫秒内序号。

        :param worker: 设备编号。取值范围 0-1023。
        :param epoch: 时间戳起点（计算用的时间戳与标准时间戳的差，单位为毫秒）。
        :raise RuntimeError: 试图创建相同worker的类实例。
        """
        if worker in cls._objects_:
            exc = RuntimeError(f'存在相同的 SnowflakeMultiWorker(worker={worker})')
            snow_logger.exception(cls.__name__, exc_info=exc)
            raise exc
        cls._objects_.append(worker)
        return SnowflakeWorker.__new__(cls)


class SnowflakeSingleWorker(SnowflakeWorker):
    _instanced_ = False

    def __new__(cls, *, epoch: int = 0):
        """
        雪花ID生成的单例实现。

        雪花ID是一个64位整数，包含1位符号+41位时间戳+10位设备编号+12位毫秒内序号。
        其中设备编号从0开始，当发生时钟回拨时自动递增，因此总计容许 1023 次时钟回拨。

        :param epoch: 时间戳起点（计算用的时间戳与标准时间戳的差，单位为毫秒）。
        :raise RuntimeError: 试图创建第二个类实例。
        """
        if cls._instanced_ is True:
            exc = RuntimeError('已实例化过 SnowflakeSingleWorker 。')
            snow_logger.exception(cls.__name__, exc_info=exc)
            raise exc
        cls._instanced_ = True
        return SnowflakeWorker.__new__(cls)

    def __init__(self, *, epoch: int = 0):
        super().__init__(0, epoch=epoch)

    def redirect(self) -> int:
        worker = self._worker + 1
        if worker & self.WORKER != worker:
            super().redirect()
        self._worker = worker
        return self._sequence
