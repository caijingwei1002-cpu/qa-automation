# Day 57 验证证据

日期：2026-09-09
阶段：Restful Booker 收尾与测试代码质量
项目：test-projects/03-restful-booker-api
主题：异常路径资源清理

## 目标测试

命令：

```text
.\.venv\Scripts\python.exe -m pytest test-projects/03-restful-booker-api/tests/test_business_rules.py -q
```

结果：

```text
exit_code=0 (passed)
..x.x.                                                                   [100%]
4 passed, 2 xfailed in 0.39s
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
63 passed, 18 xfailed in 1.11s
```

## 关键验证

- 目标测试退出码：`0`，包含控制性断言失败后清理并验证 404 的场景。
- 迁移测试 `test_booking_lifecycle.py`：`2 passed`，覆盖 PUT 更新断言失败后的清理。
- Ruff check 和 Ruff format check 均通过，修改后的测试文件无静态检查或格式问题。
- 全量回归退出码：`0`，没有新增失败。
- 测试命令由本运行脚本绑定到仓库虚拟环境。

## 环境问题与结论

- 工作目录：`D:\qa-automation-learning`。
- 测试解释器：`D:\qa-automation-learning\.venv\Scripts\python.exe`。
- 首次运行因本地 `127.0.0.1:3001` 服务未启动而连接拒绝；确认环境问题后使用目标项目的 `npm start` 启动服务，`/ping` 返回 HTTP 201。
- 服务启动后目标测试和全量回归均通过；结论是 Day 57 的资源登记与异常路径清理行为满足计划契约。
