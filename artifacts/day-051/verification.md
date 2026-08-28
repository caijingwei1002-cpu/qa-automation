# Day 51 验证证据

日期：2026-08-28
阶段：Restful Booker API
项目：test-projects/03-restful-booker-api
主题：类型错误

## 目标测试

命令：

```text
.\.venv\Scripts\python.exe -m pytest test-projects/03-restful-booker-api/tests/test_invalid_types.py -q
```

结果：

```text
exit_code=0 (passed)
xxx                                                                      [100%]
3 xfailed in 0.15s
```

## 全量回归

命令：

```text
.\.venv\Scripts\python.exe -m pytest test-projects/03-restful-booker-api/tests -q
```

结果：

```text
exit_code=0 (passed)
.........xxxxxx..........xxxxxxxxxx...                                   [100%]
22 passed, 16 xfailed in 1.36s
```

## 关键验证

- 目标测试退出码：`0`。
- 全量回归退出码：`0`。
- 三组参数分别覆盖字符串价格、字符串布尔值和嵌套日期字段数字类型；每组都只破坏一个字段，业务预期保持为 `400 Bad Request`。
- 本地接口对三组错误类型均返回 `200` 并创建 booking：`"200"` 被转换为数字 `200`，`"true"` 被转换为布尔值 `true`，数字 `12345` 被转换为日期字符串 `"1970-01-01"`。
- 三组已确认缺陷均使用 `strict=True` 和 `raises=AssertionError` 的 xfail 留证；接口正确返回 400 时会触发 XPASS，清理异常或其他新状态不会被已知缺陷标记吞掉。
- 测试会提取意外创建的整数 `bookingid`，并在契约断言前完成清理；本次目标测试和全量回归均未报告清理失败。

## 环境问题与结论

- 工作目录：`D:\qa-automation-learning`。
- 测试解释器：`D:\qa-automation-learning\.venv\Scripts\python.exe`。
- 当前事实是接口接受并转换三种错误类型；“数字日期可能经过时间戳转换”只是根据响应作出的假设，尚未通过服务端源码确认。
- 结论：接口缺少严格的输入类型边界，调用方错误可能被静默转换并持久化；缺陷行为已可重复回归，且测试未把实际 200 偷换成正确预期。
