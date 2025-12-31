---
title: "`time` — 时间与计时"
outline: deep
excerpt:
---

# <pre>zeraora.time</pre>

此模块提供了一些与计时有关的工具。

## `MomentMark`

一个具名元组，用于锚定某一个时刻，有以下属性：

| 下标 | 属性      | 类型                                                                                              | 说明                              |
|---:|---------|-------------------------------------------------------------------------------------------------|---------------------------------|
|  0 | `head`  | <pre>[datetime](https://docs.python.org/zh-cn/3/library/datetime.html#datetime-objects)</pre>   | 开始时刻。即自上一次停止之后开始计时的时刻。          |
|  1 | `prev`  | <pre>[datetime](https://docs.python.org/zh-cn/3/library/datetime.html#datetime-objects)</pre>   | 上一时刻。即上一次标记的时刻。                 |
|  2 | `curr`  | <pre>[datetime](https://docs.python.org/zh-cn/3/library/datetime.html#datetime-objects)</pre>   | 当前时刻。即这一次标记的时刻。                 |
|  3 | `msg`   | <pre>str</pre>                                                                                  | 相关消息。                           |
|  4 | `total` | <pre>[timedelta](https://docs.python.org/zh-cn/3/library/datetime.html#timedelta-objects)</pre> | 当前时刻 `curr` 减去开始时刻 `head` 的时间差。 |
|  5 | `delta` | <pre>[timedelta](https://docs.python.org/zh-cn/3/library/datetime.html#timedelta-objects)</pre> | 当前时刻 `curr` 减去上一时刻 `prev` 的时间差。 |

## `FoxStopwatch(name=None)`

狸子秒表。

对代码运行进行正向计时，并通过 `print()` 在控制台打印。内部维护了一个
[`MomentMark`](#MomentMark) 列表，用于随时提取记下的所有时刻。

```text
[FoxStopwatch.name] [0.000000000] [+0.000000000]: 开始计时……
[FoxStopwatch.name] [0.114514000] [+0.114514000]: 标记1
[FoxStopwatch.name] [0.314159000] [+0.199645000]: 标记2
[FoxStopwatch.name] [0.358979000] [+0.044820000]: 停止计时。
```

最简单是使用 `with` 语句包裹需要计时的部分：

```python
from zeraora.time import FoxStopwatch

with FoxStopwatch() as fox:
    # 业务逻辑
    pass
```

如需对一整个函数进行计时，可以作为装饰器使用，此时狸子会将构造参数 _name_ 设置为被装饰的函数名。

```python
from zeraora.time import FoxStopwatch

@FoxStopwatch()
def do_somthing():
    # 业务逻辑
    pass
```

带有多个装饰器时，秒表放哪里取决于你的计时范围：

```python
from rest_framework.decorators import api_view
from zeraora.time import FoxStopwatch

@FoxStopwatch()  # 从请求转发过来那一刻开始计时
@api_view(['GET'])
def query_status(request):
    # 业务逻辑
    pass

@api_view(['POST'])
@FoxStopwatch()  # 从login()执行那一刻开始计时
def login(request):
    # 业务逻辑
    pass
```

此外还可以实例化成一个对象，每个对象都是独立的秒表，互不影响：

```python
from zeraora.time import FoxStopwatch

fox = FoxStopwatch()
fox.start()
# 业务逻辑
fox.stop()
```

### `start(msg='开始计时……')` {#FoxStopwatch.start}

开始计时。

清除当前秒表中的所有 [`MomentMark`](#MomentMark)，重新标记并返回一个 `MomentMark`，然后触发打印。

### `lap(msg='')` {#FoxStopwatch.lap}

标记此刻。

标记并返回一个 [`MomentMark`](#MomentMark)，然后触发打印；如果计时尚未开始，改为调用 `start()`。

### `stop(msg='停止计时。')` {#FoxStopwatch.stop}

停止计时。

标记一个 [`MomentMark`](#MomentMark) 后触发打印，然后停止计时，返回所有秒表中的所有 `MomentMark` 后清除。

### `print()` {#FoxStopwatch.print}

使用 `print()` 打印所有 [`MomentMark`](#MomentMark)。

```text
[23:04:00.000] [##1] [0.000000000 +0.000000000]: 开始计时……
[23:04:00.114] [##2] [0.114514000 +0.114514000]: 标记1
[23:04:00.314] [##3] [0.314159000 +0.199645000]: 标记2
[23:04:00.358] [##4] [0.358979000 +0.044820000]: 停止计时。
```

## `BearStopwatch(name=None)`

熊牌秒表。

对代码运行进行正向计时，并向 Python 发送日志。大多数对象方法的用法同 [`FoxStopwatch`](#FoxStopwatch)。

```text
[23:04:00.000] [DEBUG] [zeraora.bear] [FoxStopwatch.name] [0.000000000] [+0.000000000]: 开始计时……
[23:04:00.114] [DEBUG] [zeraora.bear] [FoxStopwatch.name] [0.114514000] [+0.114514000]: 标记1
[23:04:00.314] [DEBUG] [zeraora.bear] [FoxStopwatch.name] [0.314159000] [+0.199645000]: 标记2
[23:04:00.358] [DEBUG] [zeraora.bear] [FoxStopwatch.name] [0.358979000] [+0.044820000]: 停止计时。
```

使用前，需要先调用 [`configit()`](#BearStopwatch.configit) 启用日志输出。

对于使用 Django 的项目，可以省去这一步，但需要在 settings.py 中为秒表配置处理器及记录器：

```python :line-numbers
from zeraora.time import BearStopwatch

LOGGING = {
    'version': 1,
    'formatters': {...},
    'filters': {...},
    'handlers': {
        'Console': {  # 确保有一个控制台输出
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
        # ...
    },
    'loggers': {
        BearStopwatch.LOGGER: {  # 添加相应的日志记录器
            'level': BearStopwatch.LEVEL,
            'handlers': ['Console'],
        },
    },
}
```

### `LEVEL` {#BearStopwatch.LEVEL}

熊牌秒表发送到 Python
日志系统的[日志级别](https://docs.python.org/zh-cn/3/library/logging.html#logging-levels)，默认是
`"DEBUG"`。

### `LOGGER` {#BearStopwatch.LOGGER}

熊牌秒表在 Python
日志系统注册的[记录器名称](https://docs.python.org/zh-cn/3/library/logging.html#logging.Logger.name)，默认是
`"zeraora.bear"`。

### `CONFIG` {#BearStopwatch.CONFIG}

熊牌秒表的默认[日志记录配置](https://docs.python.org/zh-cn/3/library/logging.config.html)，值如下：

```python :line-numbers
from zeraora.time import BearStopwatch

dict(
    version=1,
    formatters={
        'bear': dict(
            format='[%(asctime)s] [%(levelname)s] %(message)s',
        ),
        'bear_plus': dict(
            format='[%(asctime)s] [%(levelname)s] '
                   '[%(module)s.%(funcName)s:%(lineno)d] '
                   '%(message)s',
        ),
    },
    filters={},
    handlers={
        'Console': {
            'level': BearStopwatch.LEVEL,
            'class': 'logging.StreamHandler',
            'filters': [],
            'formatter': 'bear',
        },
    },
    loggers={
        BearStopwatch.LOGGER: dict(
            level=BearStopwatch.LEVEL,
            handlers=['Console'],
            propagate=False,
        ),
    },
)
```

### `configit(name=None)` {#BearStopwatch.configit}

_**一个类方法**_。配置日志系统，创建并返回一个熊牌秒表，参数与构造器一致。

最基础的用法是

```python
from zeraora.time import BearStopwatch

bear = BearStopwatch.configit()
bear.start()
bear.lap('标记1')
bear.lap('标记2')
bear.stop()
```

若是使用装饰器，则可以

```python
from zeraora.time import BearStopwatch

@BearStopwatch.configit()
def main():
    pass
```

### `start(msg='开始计时……')` {#BearStopwatch.start}

见 [`FoxStopwatch.start()`](#FoxStopwatch.start)

### `lap(msg='')` {#BearStopwatch.lap}

见 [`FoxStopwatch.lap()`](#FoxStopwatch.lap)

### `stop(msg='停止计时。')` {#BearStopwatch.stop}

见 [`FoxStopwatch.stop()`](#FoxStopwatch.stop)

### `print()` {#BearStopwatch.print}

见 [`FoxStopwatch.print()`](#FoxStopwatch.print)
