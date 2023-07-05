"""
包内全局变量。
"""
from __future__ import annotations

__all__ = [
    'ad_map',
    'ad_tree',
]

from .structures import DivisionCode

ad_map: dict[DivisionCode, str] = dict()
ad_tree: dict[str, dict] = dict()
