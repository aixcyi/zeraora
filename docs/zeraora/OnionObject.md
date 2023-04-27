# `OnionObject()`

> 将字典转化为对象，使得可以用点分法代替下标访问内容。

## 用法

以以下数据举例：

```Python
data = {
    "code": 0,
    "message": "ok",
    "data": {
        "id": "66a5a0612e2089564b35df189ced94a1",
        "payment": 3.14,
        "customer": {
            "openid": "oj0ed5TechOtakusSaveTheWorld",
            "gender": True,
        },
        "goods": [
            {
                "id": "1eb44e7486066eb660322dc65a673d88",
                "img_url": "/goods/image/1eb44e7486066eb660322dc65a673d88",
                "name": "龟苓膏 300g 杯装",
                "qty": 1,
            },
            {
                "id": "2af405fce650f3ea4b92521155a5019c",
                "img_url": "/goods/image/2af405fce650f3ea4b92521155a5019c",
                "name": "金银花茶 750ml 瓶装",
                "qty": 2,
            },
        ],
    },
}
```

将字典转化为嵌套对象：

```Python
from zeraora import OnionObject

resp = OnionObject(data)
print(resp.code == 0)  # True
print(resp.data.id)  # '66a5a0612e2089564b35df189ced94a1'
print(resp.data.payment)  # 3.14
print(resp.data.customer.gender)  # True
print(resp.data.goods[1].img_url)
# '/goods/image/2af405fce650f3ea4b92521155a5019c'
```

仅转化字典第一层：

```Python
from zeraora import OnionObject

resp = OnionObject(data, depth=1)
print(resp.code == 0)  # True
print(resp.data['id'])  # '66a5a0612e2089564b35df189ced94a1'
print(resp.data['payment'])  # 3.14
print(resp.data['customer']['gender'])  # True
print(resp.data['goods'][1]['img_url'])
# '/goods/image/2af405fce650f3ea4b92521155a5019c'
```

转化字典的前两层：

```Python
from zeraora import OnionObject

resp = OnionObject(data, depth=2)
print(resp.code == 0)  # True
print(resp.data.id)  # '66a5a0612e2089564b35df189ced94a1'
print(resp.data.payment)  # 3.14
print(resp.data.customer['gender'])  # True
print(resp.data.goods[1]['img_url'])
# '/goods/image/2af405fce650f3ea4b92521155a5019c'
```

`OnionObject` 使用[魔术方法](https://docs.python.org/zh-cn/3/glossary.html#term-magic-method)实现以上效果，IDE通常无法推断这样生成的对象的属性及其类型。可以按如下方法解决不能智能提示的问题：

```Python
import requests
from typing import Union, Any
from zeraora import OnionObject

class PlatformResponse(OnionObject):
    code: int
    message: str
    data: Union[OnionObject, Any]

def get_market_data() -> PlatformResponse:
    url = 'http://market.platform.com/api/poi'
    resp = requests.get(url)
    data = PlatformResponse(resp, depth=1)  # 仅转化第一层以避免污染业务数据
    if data.code < 0:
        raise Exception(data.message)
    if data.code == 0:
        raise Exception(
            'Market of platform returns a normal (non-success) response code.'
        )
    return data
```

