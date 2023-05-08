# `BearTimer()`

> 这是一个用于对代码运行计时的纯工具类。

## 用法

最简单的是使用 [with](https://docs.python.org/zh-cn/3/reference/compound_stmts.html#the-with-statement) 语句包裹需要计时的代码。被包裹的代码在开始执行前会自动开始计时，在执行完毕或因异常而离开计时范围后就会自动停止计时。

计时开始和停止时都且只会各自打印一条消息，计时开始后可以使用 `.step()` 方法打印需要的消息。

```Python
from zeraora import BearTimer

with BearTimer() as bear:
    summary = 0
    for i in range(1000000):
        if not i % 67:
            bear.step(f'loop cycle to {i} now.')
        summary += i
```

打印的格式由 `.fmt` 控制，默认的格式如下，其中

- head 代表打印的时刻；
- level 代表日志等级，默认是 `"DEBUG"` ；
- total 代表计时开始到现在的总计秒数，以小数形式包含毫秒和微秒；
- delta 代表自上一条打印到此刻的间隔秒数，以小数形式包含毫秒和微秒；
- title 是每一个 `BearTimer` 对象的名称，在实例化时传入，默认是调用计时器的函数的名称；
- msg 是自定义的消息。

如需添加更多参数，可以继承重写 `.record()` 方法。

```Python
fmt = '[{head:%H:%M:%S.%f}] [{level}] [{title}] [{total:.6f} +{delta:.6f}]: {msg}'
```

对于跨函数或复杂嵌套代码等不方便使用 with 的场景，可以实例化 `BearTimer` 后使用。实例化的对象可以反复使用。

不同对象的计时是相互独立的。某一个对象的计时的启停不会影响到其它对象。

```Python
from zeraora import BearTimer

bear = BearTimer()

def prepare_order():
    # 获取上下文
    bear.start()
    # 创建订单

def pay_now():
    # 对请求进行鉴权
    prepare_order()
    # 拉起支付
    # 将结果写回订单中
    bear.stop()
    # 序列化订单数据并返回
```

### `.start(msg='Bear timer was started.')`

重置所属对象后，再开始计时，并打印一条消息。

### `.stop(msg='Timer was stop by Bear.')`

停止所属对象的计时，并打印一条消息。

### `.step(msg='')`

打印一条消息。

