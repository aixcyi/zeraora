#!/usr/bin/python3

"""
清理 Zeraora 的构建产物。

- 使用 ``--del-mods`` 清理 ./node_modules 文件夹。
- 使用 ``--del-lock`` 清理 ./package-lock.json 文件。
"""

import sys
from pathlib import Path
from typing import Iterable, Iterator

PROJECT_ROOT = Path(__file__).absolute().parent


def walk(root: Path) -> Iterator[tuple[Path, bool]]:
    if root.is_file():
        yield root, False
        return
    if not root.is_dir():
        return
    for item in root.iterdir():
        yield from walk(item)
    else:
        yield root, True


def glob(root: Path, patterns: Iterable[str]) -> Iterator[Path]:
    for pattern in patterns:
        if (file := root / pattern).is_file():
            yield file
        else:
            yield from root.glob(pattern)


def main():
    targets = [
        './cache/',
        './dist/',
        './dist-docs/',
        './*.egg-info/',
    ]
    _, *argv = sys.argv
    if '--del-mods' in argv:
        targets.append('./node_modules/')
    if '--del-lock' in argv:
        targets.append('./package-lock.json')

    for item in glob(PROJECT_ROOT, targets):
        if item.is_file():
            print(f'正在删除文件 {item}')
            item.unlink(missing_ok=True)
            continue
        if not item.is_dir():
            continue
        print(f'正在删除目录 {item}')
        for path, is_dir in walk(item):
            if is_dir:
                path.rmdir()
            else:
                path.unlink(missing_ok=True)


if __name__ == '__main__':
    print('开始清理：')
    main()
    print('清理完毕。')
