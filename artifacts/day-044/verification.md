# Day 44 验证证据

日期：2026-08-26
主题：删除与清理

## 目标测试

命令：

```text
.\.venv\Scripts\python.exe -m pytest test-projects/03-restful-booker-api/tests/test_delete_booking.py -q
```

结果：

```text
..                                                                       [100%]
2 passed in 0.18s
```

## API 全量回归

命令：

```text
.\.venv\Scripts\python.exe -m pytest test-projects/03-restful-booker-api/tests -q
```

结果：

```text
..............                                                           [100%]
14 passed in 0.86s
```

## 关键验证

- 主场景创建本次测试自己的 booking，读取动态 `bookingid`。
- DELETE 使用 Token 鉴权，响应状态为 `201`。
- 删除后使用同一个动态 ID GET，响应状态为 `404`。
- 重复删除挑战验证第二次 DELETE 返回 `405`。
- 本日新增测试未打印或记录真实 Token。
