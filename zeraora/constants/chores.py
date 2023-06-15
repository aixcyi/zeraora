__all__ = [
    'Degree',
]

from zeraora.typeclasses import Items


class Degree(int, Items):
    """
    描述程度的五个档位。
    """
    HIGHEST = 100, '最高'
    HIGH = 50, '高'
    NORMAL = 0, '正常'
    LOW = -50, '低'
    LOWEST = -100, '最低'

    __properties__ = 'label',
