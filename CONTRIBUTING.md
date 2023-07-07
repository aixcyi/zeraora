# 开发指南

- 以 [reStructuredText](https://zh.wikipedia.org/wiki/ReStructuredText) 格式编写的中文文档字符串（[docstring](https://docs.python.org/zh-cn/3/glossary.html#term-docstring)）
- 需要有完备的类型标注（[Type Hints](https://peps.python.org/pep-0484/)）
- 尽量编写测试用例，并使二级包中的单个文件覆盖率 100%

## 包结构

对外公开的结构一般仅限前两级，这样可以尽量避免因为修改子级导致不兼容。

具体来说，如果代码不依赖第三方库，那么按照用途或者存在形式划分二级包，比如：

- `zeraora`
  - `utils`，纯工具，对应了 `./zeraora/utils.py`
  - `typeclasses`，类型类，对应了 `./zeraora/typeclasses.py`
  - `constants`，常量和枚举，对应了 `./zeraora/constants/*.py`
    - 内部划分了 `charsets`、`divison`、`chores` 几个三级包
  - ……

如果只依赖单个第三方库，或者被依赖的第三方库**都是**某个库的前置（比如安装 DRF 时会自动安装它所依赖的 Django），那么按照那个库的名称划分一个单独的二级包，这个包里的所有符号都导入到这个二级包（`__init__.py`）中：

（使用简写和缩写是为了避免命名冲突以及更重要的缩短导入长度）

- `zeraora`
  - `dj`
    - `fields`，对 Django字段类 的增强
    - `models`，对 Django模型类 的增强
    - `lookups`，定制的查找器
  - `drf`，对 Django Rest Framework 的增强，不涉及 Django
    - `filters`，过滤器中间件
    - `viewsets`，对视图集的增强

如果必须要依赖多个不相互依赖的第三方库，那么按照工具的主题作为名称划分一个单独的二级包，同样的，这个包里的所有符号都导入到这个二级包（`__init__.py`）中。

（因为还没有这样的工具，所以就不举栗子了）

## 导入

导入都应尽量放在文件开头。

外部符号用绝对路径导入，并尽量使用 `try-except` 结构告知终端用户解决方案：

```python
# ./zeraora/drf/viewsets.py
from typing import Any, Dict

try:
    from django.utils.decorators import classonlymethod
    from rest_framework import status
    from rest_framework.response import Response
    from rest_framework.viewsets import ViewSetMixin
except ImportError as e:
    raise ImportError(
        '需要安装Django以及DRF框架：\n'
        'pip install django djangorestframework'
    ) from e
```

内部符号应尽可能使用相对路径导入，以避免出现循环依赖问题。当需要测试使用了相对导入的包时，参考如下：

```python
# ./zeraora/mymodule/subpackage.py
import sys
import re
import os

if __name__ == '__main__':
    from ..typeclasses import OnionObject
else:
    from zeraora.typeclasses import OnionObject

# 业务代码...

if __name__ == '__main__':
    assert 1 == 1
```

## 命名规范

1. 包名（包括文件夹和文件）使用下划线风格（snake_style），但尽可能用一个单词搞定，避免下划线。
2. 业务代码中，类名、枚举名使用大驼峰（CamelCase），函数名、方法名、变量名使用下划线风格（snake_style），常量名使用全大写（UPPER_CASE）
3. 测试代码中，文件名使用下划线风格（snake_style），类名使用大驼峰+可选的下划线（Test_CamelCase），方法名可以混合多种风格（test_CamelCase）