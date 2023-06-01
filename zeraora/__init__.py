from .checkers import start
from .converters import (
    remove_exponent,
    delta2hms,
    delta2ms,
    delta2s,
    represent,
    datasize,
    datasize as dsz,
    true,
    SafeCaster,
    safecast,
    safecasts,
)
from .divisions import (
    Region,
    Province,
)
from .generators import (
    randbytes,
    randb62,
    randb64,
    SnowflakeWorker,
    SnowflakeMultiWorker,
    SnowflakeSingleWorker,
)
from .typeclasses import (
    OnionObject,
    RadixInteger,
    ChoicesMeta,
    Choices,
    IntegerChoices,
    TextChoices,
    ItemsMeta,
    Items,
)
from .utils import (
    BearTimer,
    ReprMixin,
)

__version__ = (0, 2, 14)
version = '0.2.14'

# Django makemigrations 会在 CreateModel 里插入参数
# bases=(zeraora.utils.ReprMixin, models.Model)
# 导致对 zeraora 产生依赖，这里改变 ReprMixin 所在包地址，
# 尽量减少因为改变内部包结构导致对外部的影响。
ReprMixin.__module__ = 'zeraora'
