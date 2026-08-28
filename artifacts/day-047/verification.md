# Day 47 验证证据

日期：2026-08-27
主题：Fixture 生命周期

## 目标测试

命令：

```text
.\.venv\Scripts\pytest.exe tests/test_delete_booking.py tests/test_update_booking.py::test_update_booking_without_token_returns_403 -q
```

结果：

```text
...                                                                      [100%]
3 passed in 0.07s
```

## API 全量回归

命令：

```text
.\.venv\Scripts\pytest.exe tests -q
```

结果：

```text
..............                                                           [100%]
14 passed in 0.56s
```

## 关键验证

- `created_booking` Fixture 在 `yield` 前获取 Token 并创建动态 booking。
- `yield` 后通过 `finally` 查询同一个动态 `bookingid` 并执行清理。
- 测试主动删除资源后，teardown 收到 `404` 会视为清理完成，不重复制造失败。
- 删除和无 Token 更新测试已实际使用 `created_booking` Fixture。
- Fixture 对 Token 和 `bookingid` 的响应结构进行校验，未打印或记录真实 Token。
