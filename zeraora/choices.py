import enum
from types import DynamicClassAttribute


# copy from https://github.com/django/django/blob/stable/4.2.x/django/db/models/enums.py
class ChoicesMeta(enum.EnumMeta):
    """用于创建带有标签文本的枚举的元类。"""

    def __new__(metacls, classname, bases, classdict, **kwds):
        labels = []
        for key in classdict._member_names:
            value = classdict[key]
            if (
                    isinstance(value, (list, tuple))
                    and len(value) > 1
                    and isinstance(value[-1], (str,))
            ):
                *value, label = value
                value = tuple(value)
            else:
                label = key.replace("_", " ").title()
            labels.append(label)
            # Use dict.__setitem__() to suppress defenses against double
            # assignment in enum's classdict.
            dict.__setitem__(classdict, key, value)
        cls = super().__new__(metacls, classname, bases, classdict, **kwds)
        for member, label in zip(cls.__members__.values(), labels):
            member._label_ = label
        return enum.unique(cls)

    def __contains__(cls, member):
        if not isinstance(member, enum.Enum):
            # Allow non-enums to match against member values.
            return any(x.value == member for x in cls)
        return super().__contains__(member)

    @property
    def names(cls):
        empty = ["__empty__"] if hasattr(cls, "__empty__") else []
        return empty + [member.name for member in cls]

    @property
    def choices(cls):
        empty = [(None, cls.__empty__)] if hasattr(cls, "__empty__") else []
        return empty + [(member.value, member.label) for member in cls]

    @property
    def labels(cls):
        return [label for _, label in cls.choices]

    @property
    def values(cls):
        return [value for value, _ in cls.choices]


# copy from https://github.com/django/django/blob/stable/4.2.x/django/db/models/enums.py
class Choices(enum.Enum, metaclass=ChoicesMeta):
    """用于创建带有标签文本的枚举的类。"""

    @DynamicClassAttribute
    def label(self):
        return self._label_

    @property
    def do_not_call_in_templates(self):
        return True

    def __str__(self):
        """
        Use value when cast to str, so that Choices set as model instance
        attributes are rendered as expected in templates and similar contexts.
        """
        return str(self.value)

    # A similar format was proposed for Python 3.10.
    def __repr__(self):
        return f"{self.__class__.__qualname__}.{self._name_}"


# copy from https://github.com/django/django/blob/stable/4.2.x/django/db/models/enums.py
class IntegerChoices(int, Choices):
    """用于创建值是整数的带有标签文本的枚举的类。"""

    pass


# copy from https://github.com/django/django/blob/stable/4.2.x/django/db/models/enums.py
class TextChoices(str, Choices):
    """用于创建值是字符串的带有标签文本的枚举的类。"""

    def _generate_next_value_(name, start, count, last_values):
        return name
