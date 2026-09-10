# Day 58 验证证据

日期：2026-09-09
阶段：Restful Booker 收尾与测试代码质量
项目：test-projects/03-restful-booker-api
主题：过滤测试数据隔离

## 目标测试

命令：

```text
.\.venv\Scripts\python.exe -m pytest test-projects/03-restful-booker-api/tests/test_filters.py -q
```

结果：

```text
exit_code=0 (passed)
...                                                                      [100%]
3 passed in 0.18s
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
63 passed, 18 xfailed in 1.27s
```

## 关键验证

- 目标测试退出码：`0`。
- 独立迁移测试 `test_get_bookings.py`：`1 passed`，验证两个自建 booking 都出现在无过滤集合中，并在 teardown 中分别清理。
- 目标过滤测试覆盖 firstname、lastname 和 checkin 三组匹配/干扰数据，验证包含与排除关系。
- 全量回归退出码：`0`。
- 服务重启前后目标过滤测试均为 `3 passed`，全量回归均为 `63 passed, 18 xfailed`；重启后的 `/ping` 返回 `201`。
- Ruff check 与 Ruff format check 均通过，涉及文件为 `test_filters.py` 和 `test_get_bookings.py`。
- 测试命令由本运行脚本绑定到仓库虚拟环境。

## 环境问题与结论

- 工作目录：`D:\qa-automation-learning`。
- 测试解释器：`D:\qa-automation-learning\.venv\Scripts\python.exe`。
- 服务地址：`http://127.0.0.1:3001`。
- 结论：过滤测试不再依赖固定 Jim/Brown 预置数据；目标、迁移、全量和重启后验证均满足 Day 58 契约。
