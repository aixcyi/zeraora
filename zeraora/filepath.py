from __future__ import annotations

__all__ = [
    'RawPath',
    'RawPosixPath',
    'RawWindowsPath',
]

import os
from pathlib import PosixPath, PurePath, PurePosixPath, PureWindowsPath, WindowsPath


class RawPath(PurePath):
    def __new__(cls, *args: str):
        """
        继承 PurePath 但原生风格的地址。它通过检测字符串而不是操作系统来分化不同风格的 PurePath 类。
        """
        if cls is RawPath:
            ws = any('\\' in arg for arg in args)
            cls = RawWindowsPath if ws else RawPosixPath
        return cls._from_parts(args)

    def cast_by_os(self) -> PosixPath | WindowsPath:
        """
        根据操作系统转化成 PosixPath 或 WindowsPath 以获得基于文件系统实现的方法。
        """
        return WindowsPath(self) if os.name == 'nt' else PosixPath(self)

    def cast_by_raw(self) -> PosixPath | WindowsPath:
        """
        根据原生风格转化成 PosixPath 或 WindowsPath 以获得基于文件系统实现的方法。

        :raise NotImplementedError: 转化结果与当前操作系统不匹配。
        """
        raise NotImplementedError


class RawPosixPath(PurePosixPath):

    def cast_by_raw(self) -> PosixPath:
        """
        根据原生风格转化成 PosixPath 或 WindowsPath 以获得基于文件系统实现的方法。

        :raise NotImplementedError: 转化结果与当前操作系统不匹配。
        """
        return PosixPath(self)


class RawWindowsPath(PureWindowsPath):

    def cast_by_raw(self) -> WindowsPath:
        """
        根据原生风格转化成 PosixPath 或 WindowsPath 以获得基于文件系统实现的方法。

        :raise NotImplementedError: 转化结果与当前操作系统不匹配。
        """
        return WindowsPath(self)
