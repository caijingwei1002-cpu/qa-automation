# Day 59 验证证据

日期：2026-09-10
阶段：Restful Booker 收尾与测试代码质量
项目：test-projects/03-restful-booker-api
主题：鉴权与资源管理重构

## 目标测试

命令：

```text
.\.venv\Scripts\python.exe -m pytest test-projects/03-restful-booker-api/tests -q
```

结果：

```text
exit_code=0 (passed)
...........xxxxxx..x.x...........xxxxxxxxxx............................. [ 88%]
.........                                                                [100%]
63 passed, 18 xfailed in 1.32s
```

## 全量回归

命令：

```text
.\.venv\Scripts\python.exe -m pytest test-projects/03-restful-booker-api/tests -q
```

结果：

```text
exit_code=0 (passed)
...........xxxxxx..x.x...........xxxxxxxxxx............................. [ 88%]
.........                                                                [100%]
63 passed, 18 xfailed in 1.32s
```

## 关键验证

- 目标测试退出码：`0`。
- DELETE、PUT、PATCH 相关测试：`5 passed`，均使用公共 `auth_token` 和 `created_booking` fixture。
- `created_booking` 只返回 `booking_id` 与 `payload`；teardown 统一执行 DELETE，并验证删除后 GET `404`。
- 全量回归退出码：`0`。
- 受控失败测试：预期主体 `1 failed`，失败来自故意的 `assert False`；没有 fixture setup/teardown 错误。
- 受控失败创建的 booking 删除后直接 GET 返回 `404`，证明测试主体失败后资源仍被清理。
- Ruff check 与 Ruff format check 均通过，涉及 `conftest.py`、`test_delete_booking.py` 和 `test_update_booking.py`。
- 测试命令由本运行脚本绑定到仓库虚拟环境。

## 环境问题与结论

- 工作目录：`D:\qa-automation-learning`。
- 测试解释器：`D:\qa-automation-learning\.venv\Scripts\python.exe`。
- 服务地址：`http://127.0.0.1:3001`。
- 首次运行曾因服务未启动导致 `POST /auth` 连接拒绝；启动服务后 `/ping` 返回 `201`，相关测试和全量回归均通过。
- 结论：认证与资源管理已按职责拆分，正常路径和测试主体失败路径的资源清理均满足 Day 59 契约。
