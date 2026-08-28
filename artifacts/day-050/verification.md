# Day 50 验证证据

日期：2026-08-28
阶段：Restful Booker API
项目：test-projects/03-restful-booker-api
主题：缺失字段

## 目标测试

命令：

```text
.\.venv\Scripts\python.exe -m pytest test-projects/03-restful-booker-api/tests/test_invalid_payloads.py -q
```

结果：

```text
exit_code=0 (passed)
xxxxxxx                                                                  [100%]
7 xfailed in 0.20s
```

## 全量回归

命令：

```text
.\.venv\Scripts\python.exe -m pytest test-projects/03-restful-booker-api/tests -q
```

结果：

```text
exit_code=0 (passed)
.........xxxxxx..........xxxxxxx...                                      [100%]
22 passed, 13 xfailed in 1.28s
```

## 关键验证

- 目标测试退出码：`0`。
- 全量回归退出码：`0`。
- 使用参数化逐个删除 `firstname`、`lastname`、`totalprice`、`depositpaid`、`bookingdates`、`bookingdates.checkin` 和 `bookingdates.checkout`。
- 7 组场景的业务预期均为 `400 Bad Request`；当前本地接口实际均返回 `500 Internal Server Error`，因此以 `strict=True` 标记为 `xfailed`，没有把 `500` 偷换成正确结果。
- 测试使用独立 payload；如果接口错误返回 `200` 并产生动态 `bookingid`，会在断言失败前提取 ID 并通过 `finally` 清理。

## 环境问题与结论

- 工作目录：`D:\qa-automation-learning`。
- 测试解释器：`D:\qa-automation-learning\.venv\Scripts\python.exe`。
- 系统 Python 未安装 pytest，正式验证由项目 `.venv` 执行；这属于运行环境差异，不是测试脚本缺陷。
- 结论：当前接口对缺失必填字段返回 500，错误处理不符合 400 业务预期；该问题已由 7 组严格 xfail 留证，本日不修改被测服务。
