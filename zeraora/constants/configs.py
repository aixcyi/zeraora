"""
默认配置。
"""
from typing import Any

STANDARD_LOG_FMT = (
    '[%(asctime)s] [%(levelname)s] '
    '[%(module)s.%(funcName)s:%(lineno)d] '
    '%(message)s'
)


def fix(**kwargs: Any):
    return dict(
        (k.rstrip('_'), v) for k, v in kwargs.items()
    )


LOG_CONF_BEAR = dict(
    version=1,
    formatters={
        'bear': dict(
            format='[%(asctime)s] [%(levelname)s] %(message)s',
        ),
        'bear_plus': dict(
            format=STANDARD_LOG_FMT,
        ),
    },
    filters={},
    handlers={
        'Console': fix(
            level='DEBUG',
            class_='logging.StreamHandler',
            filters=[],
            formatter='bear',
        ),
    },
    loggers={
        'zeraora.bear': dict(
            level='DEBUG',
            handlers=['Console'],
            propagate=False,
        ),
    },
)
