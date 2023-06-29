__all__ = [
    'Weeks',
]

from ..typeclasses import Items


class Weeks(Items):
    Monday = '星期一'
    Tuesday = '星期二'
    Wednesday = '星期三'
    Thursday = '星期四'
    Friday = '星期五'
    Saturday = '星期六'
    Sunday = '星期天'

    __properties__ = 'description',

    @property
    def description(self) -> str:
        return self._description_
