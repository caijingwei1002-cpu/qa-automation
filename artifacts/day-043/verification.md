# Day 43 验证证据

日期：2026-08-26
阶段：Restful Booker API
主题：部分更新 PATCH

## 目标测试

命令：

```powershell
.\.venv\Scripts\python.exe -m pytest test-projects/03-restful-booker-api/tests/test_update_booking.py -q
```

结果：

```text
...                                                                      [100%]
3 passed in 0.11s
```

覆盖内容：

- 创建 booking 后使用动态 `bookingid`。
- 获取 Token 并通过 Cookie 认证 PATCH。
- 只提交 `totalprice` 和 `additionalneeds`。
- 验证指定字段变更。
- 验证 `firstname`、`lastname`、`depositpaid` 和 `bookingdates` 保持原值。
- 二次 GET 验证部分更新已持久化。

## API 全量回归

命令：

```powershell
.\.venv\Scripts\python.exe -m pytest test-projects/03-restful-booker-api/tests -q
```

结果：

```text
............                                                             [100%]
12 passed in 0.48s
```

## 风险记录

本日测试创建的 booking 尚未自动清理，暂不影响当前验证结果，但可能造成长期测试数据污染；后续在 fixture 生命周期和 DELETE 清理任务中处理。
