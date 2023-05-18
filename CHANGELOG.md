# 更新

> 仅列出不兼容旧版的修改，其余变动见git历史。

## v0.2

### 0.2.11（2023-5-18）

- 紧急修复 0.2.10 中 `RadixInteger` 的类型标注错误，该错误会导致引入了Zeraora的项目都无法启动。

### 0.2.8（2023-5-11）

- 省份枚举 `Province` 的值从 `int` 改为 `str` 。

### 0.2.7（2023-5-09）

- 快捷函数 `casting` 更名为 `safecast` ，调用参数保持一致。
- 更改了内部包结构。使用了 `ReprMixin` 的 Django 模型的迁移文件（migration）中 `CreateModel` 的 `base` 参数可能会因为 `ReprMixin` 而传入了错误值，更新后可能因为找不到 `zeraora.typing.ReprMixin` 而无法进行迁移（`manage.py migrate`）。点击[这里](https://github.com/aixcyi/zeraora/blob/master/docs/zeraora/ReprMixin.md)查看解决方案。

### 0.2.5（2023-5-02）

- `OnionObject.__repr__()` 不再进行嵌套递归，因为在调试模式中可以展开嵌套，在此递归并无意义。现在OnionObject对象内的OnionObject对象在 `repr()` 后会显示为 `OnionObject(...)` 。
- 去除 `OnionObject.__str__()` 方法，可以用 `import json` 后 `json.dumps(OnionObject())` 实现原来的效果。
- 更改 `BearTimer` 的默认打印格式。
- 将 `BearTimer.output()` 拆分为负责准备打印的 `record()` 和实现打印的 `handle()` 。

### 0.2.0（2023-4-12）

- 将递归转化的 `JSONObject` 与仅表层转化的 `JsonObject` 合并为 `OnionObject` ，并删去前述两个类。

## v0.1

略
