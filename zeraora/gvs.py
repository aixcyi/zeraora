"""
包内全局变量。
"""

__all__ = [
    'ad_map',
    'ad_tree',
]

from typing import Dict

from .structures import DivisionCode

ad_map: Dict[DivisionCode, str] = dict()
ad_tree: Dict[str, dict] = dict()
