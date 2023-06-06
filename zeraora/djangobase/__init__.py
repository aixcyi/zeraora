from .models import (
    SnakeModel,
    CreateTimeMixin,
    TimeMixin,
    DeletionMixin,
)
from .viewsets import (
    EasyViewSetMixin,
    SoftDeleteModelMixin,
)

SnakeModel.__module__ = 'zeraora.djangobase'
TimeMixin.__module__ = 'zeraora.djangobase'
DeletionMixin.__module__ = 'zeraora.djangobase'
CreateTimeMixin.__module__ = 'zeraora.djangobase'
EasyViewSetMixin.__module__ = 'zeraora.djangobase'
SoftDeleteModelMixin.__module__ = 'zeraora.djangobase'
