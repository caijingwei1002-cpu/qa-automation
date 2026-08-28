# Day 42 验证证据

日期：2026-08-26
阶段：Restful Booker API
主题：完整更新 PUT

## 目标测试

命令：

```powershell
.\.venv\Scripts\python.exe -m pytest test-projects/03-restful-booker-api/tests/test_update_booking.py -q
```

结果：

```text
..                                                                       [100%]
2 passed in 0.18s
```

覆盖内容：

- 创建 booking 后使用动态 `bookingid`。
- 通过 `/auth` 获取 Token，并使用 `Cookie: token=<token>` 认证 PUT。
- 发送完整更新 payload。
- 验证 PUT 响应与更新 payload 一致。
- 二次 GET 验证更新结果已持久化。
- 无 Token 的 PUT 返回 `403`。

## API 全量回归

命令：

```powershell
.\.venv\Scripts\python.exe -m pytest test-projects/03-restful-booker-api/tests -q
```

结果：

```text
...........                                                              [100%]
11 passed in 0.31s
```

## 风险记录

本日测试创建的 booking 尚未自动清理，暂不影响当前验证结果，但可能造成长期测试数据污染；后续在 fixture 生命周期和 DELETE 清理任务中处理。
