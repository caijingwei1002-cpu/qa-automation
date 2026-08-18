# Day 11 验证证据：标记与套件

日期：2026-08-18

## 目标

验证 `smoke` 是关键路径子集，`regression` 覆盖全部现有测试，并且两个套件都可以独立执行。

## 配置与范围

- 配置：`test-projects/01-todomvc-ui/pytest.ini`
- 注册标记：`smoke`、`regression`
- 全部 13 个测试都属于 `regression`
- `smoke` 包含 4 个关键路径：
  - `test_add_todo`
  - `test_complete_todo`
  - `test_delete_todo`
  - `test_filter_todos`

## 收集检查

```text
smoke: 4/13 tests collected (9 deselected)
regression: 13 tests collected
default: 13 tests collected
```

## 实际执行

命令：

```powershell
..\..\.venv\Scripts\python.exe -m pytest tests -m smoke -q
```

结果：

```text
4 passed, 9 deselected in 4.60s
```

命令：

```powershell
..\..\.venv\Scripts\python.exe -m pytest tests -m regression -q
```

结果：

```text
13 passed in 11.44s
```

## 阻塞与根因

首次在受限环境运行 smoke 时，4 条测试都在 `tests/conftest.py` 的 `browser` fixture 初始化阶段失败，错误为 `PermissionError: [WinError 5] Access is denied`。调用栈显示 Playwright 在创建 Windows named pipe、启动驱动子进程时被环境权限阻止；测试尚未进入业务断言，也不是 TodoMVC 服务或 marker 逻辑失败。

在允许启动 Playwright 子进程的授权环境中重跑同一命令后，4 条 smoke 测试全部通过。该环境阻塞已记录并解决。

## 结论

Day 11 的 smoke/regression 标记策略已落实到配置和测试代码。smoke 可独立快速执行，regression 可覆盖全部 13 个现有测试。
