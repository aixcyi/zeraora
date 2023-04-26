# `ReprMixin()`

> 生成通用格式的 representation（ [`repr()`](https://docs.python.org/zh-cn/3/library/functions.html#repr) 的返回值，是调试代码时对象内部状况的人为表述）。

这个类是一个mixin，重写了 `__repr__()` 方法，使其返回类似于下列格式的字符串：

```
<User(314) male username="leo" birthday=[2000-01-23]>
```

## 用法

将其作为第一父类继承，然后在类里面添加内部类 `AttributeMeta` 以控制属性的显示，添加内部类 `TagMeta` 来控制标签的显示。

```Python
from zeraora import ReprMixin

class MyObject(ReprMixin):

    # 原有代码...

    class AttributeMeta:  # 控制 MyObject 对象的属性的显示
        pass

    class TagMeta:  # 根据 MyObject 对象的属性生成特定标签
        pass

obj = MyObject()
print(repr(obj))
# <MyObject ...>
```

如果继承的类具有名为 `pk` 或 `id` 的属性，将会被用作主键（优先获取前者）：

```Python
from zeraora import ReprMixin

class MyObject(ReprMixin):

    @property
    def pk(self):
        return 'edc1d0a1d2ed'

obj = MyObject()
print(repr(obj))
# <MyObject(edc1d0a1d2ed) ...>
```

### `AttributeMeta`

> 这是一个内部类，放在需要控制representation的类内。它不会也不应被实例化。

它的变量名是外部类对象的属性名，变量值是需要展示的属性标题。`ReprMixin` 会按照 `AttributeMeta` 变量**定义的顺序**来展示外部类的属性。

没有被定义的属性将不会展示。如果没有任何属性需要展示，可以不必声明这个类。

```Python
from zeraora import ReprMixin

class User(ReprMixin):

    def __init__(self):
        self.age = 18
    	self.name = '叶秋然'
        self.school = '哔哩哔哩矿业无限大学'

    class AttributeMeta:
        school  # 必须被赋值，否则不会被展示
        name = '姓名'
        age = '年龄'

user = User()
print(repr(user))
# <User 姓名="叶秋然" 年龄=18>
```

如果需要对外部类对象的属性值进行转换，只需要将转换函数[注解](https://docs.python.org/zh-cn/3/glossary.html#term-variable-annotation)到变量中即可。转换函数只能接收一个参数，并且返回值必须是字符串，否则会引发类型错误 `TypeError` 。

`ReprMixin` 默认使用 `zeraora.represent()` 自动转换外部类的属性值，例如会为字符串自动添加双引号、为日期生成一个漂亮的格式，等等。

如果不需要默认转换，必需手动注解一个不可被调用的任意值。换句话说，只需要注解一个不可调用的东西，就可以按照属性值原样输出。注意！如果属性值**不是**一个字符串，同样会引发类型错误 `TypeError` ！

```Python
from datetime import date
from zeraora import ReprMixin, represent

class User(ReprMixin):

    def __init__(self):
    	self.name = '叶秋然'
        self.birth = date(2000, 1, 23)
        self.join_date = date(2023, 9, 1)
        self.school_name = '哔哩哔哩矿业无限大学'

    class AttributeMeta:
        name = '姓名'
        birth = '生日'  # 相当于 birthday: represent = '生日'
        join_date: str = '入学日期'  # 展示的内容是 str(self.join_date) 得到的
        school_name: None = '学校'  # 禁用默认转换

user = User()
print(repr(user))
# <User 姓名="叶秋然" 生日=[2000-01-23] 入学日期=2023-09-01 学校=哔哩哔哩矿业无限大学>
```

### `TagMeta`

> 这是一个内部类，放在需要控制representation的类内。它不会也不应被实例化。

与 `AttributeMeta` 的定义类似，`TagMeta` 的变量名是外部类对象的属性名，但变量值是需要在representation中展示的内容。

默认情况下，如果外部类对象的属性值判定为 `False` 将不会显示。如果需要更改这个逻辑，需要提供一个二元元组；当某个值是空字符串时，就不会被显示。

同样地，`ReprMixin` 会按照 `TagMeta` 变量**定义的顺序**来展示标签。没有被定义的属性将不会被展示。如果没有任何属性需要展示，可以不必声明这个类。

所有标签都比属性优先展示。

```Python
from zeraora import ReprMixin

class User(ReprMixin):
    active = True

    def __init__(self):
    	self.name = '叶秋然'
        self.gender = False
        self.graduated = True

	class AttributeMeta:
        name = '姓名'

    class TagMeta:
        graduated = '已毕业'  # 为True时展示，为False时不展示
        active = '已注销', ''  # False时展示，True时不展示
        gender = '男', '女'  # 前者在False时展示，后者在True时展示

user = User()
print(repr(user))
# <User 已毕业 姓名="叶秋然">
```

如果需要展示多种可能，可以提供一个列表或字典，会自动根据属性值进行下标取值：

```Python
from zeraora import ReprMixin

class User(ReprMixin):

    def __init__(self):
    	self.name = '叶秋然'
        self.subject = 0
        self.ethnicity = 'Han'

	class AttributeMeta:
        name = '姓名'

    class TagMeta:
        subject = ['工学','哲学','法学','文学','理学','农学','医学']
        ethnicity = {'Han': '汉族', 'Manchu': '满族', 'Zhuang': '壮族', ...}

user = User()
print(repr(user))
# <User 工学 汉族 姓名="叶秋然">
```

## 底层

重写 `_obtain_attrs()` 方法可以实现控制 `AttributeMeta` 的行为；
重写 `_obtain_tags()` 方法可以实现控制 `TagMeta` 的行为；
重写 `_obtain_pk()` 方法可以改变自动读取 `pk` 或 `id` 属性的行为；
重写 `_obtain_kls()` 方法可以改变被展示的类名。

代码框架：

```Python
from zeraora import ReprMixin

class MyObject(ReprMixin):

    # 业务代码……

    class AttributeMeta:
        pass

    class TagMeta:
        pass

    def __repr__(self) -> str:
        kls = self._obtain_kls()
        pkv = self._obtain_pk()
        tags = self._obtain_tags()
        attrs = self._obtain_attrs()
        content = (
                (f'({pkv})' if pkv else '') +
                (f' {tags}' if tags else '') +
                (f' {attrs}' if attrs else '')
        )
        return f'<{kls}{content}>'

    def _obtain_kls(self) -> str:
        pass

    def _obtain_pk(self) -> str:
        pass

    def _obtain_tags(self) -> str:
        pass

    def _obtain_attrs(self) -> str:
        pass
```

