"""
`Snowflake ID <https://en.wikipedia.org/wiki/Snowflake_ID>`_ 生成算法相关应用。
"""
__all__ = [
    'SnowflakeWorker',
    'SnowflakeMultiWorker',
    'SnowflakeSingleWorker',
]

import logging
from time import time

logger = logging.getLogger('zeraora.snowflake')


class SnowflakeWorker(object):
    STAMP = (1 << 41) - 1
    """
    时间戳最大值。
    """

    WORKER = (1 << 10) - 1
    """
    设备编号最大值。
    """

    SEQUENCE = (1 << 12) - 1
    """
    序号最大值。
    """

    EPOCH1970 = 0
    """
    时间戳起点。
    """

    EPOCH2000 = 946656000
    """
    2000年1月1日零点时间戳。
    """

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
        """
        时间回拨的处理方法。仅限继承重写。
        """
        exc = self.TimeRedirected(self)
        logger.exception(type(self).__name__, exc_info=exc)
        raise exc

    def overflow(self):
        """
        序号上溢的处理方法。仅限继承重写。
        """
        exc = self.SequenceOverflow(self)
        logger.exception(type(self).__name__, exc_info=exc)
        raise exc

    def dump(self) -> dict:
        """
        将属性以字典形式导出。
        """
        return {
            "stamp": self._stamp,
            "worker": self._worker,
            "sequence": self._sequence,
        }

    def load(self, data: dict, **kwargs):
        """
        载入相关属性。

        :param data: 字典。
        :param kwargs: 解包传参。
        """
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
        """
        时钟回拨。
        """

        def __str__(self):
            return 'Time redirected. ' \
                   '(stamp=%s, worker=%s, sequence=%s)' % self.args

    class SequenceOverflow(_Error):
        """
        序号上溢。
        """

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
            logger.exception(cls.__name__, exc_info=exc)
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
            logger.exception(cls.__name__, exc_info=exc)
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
