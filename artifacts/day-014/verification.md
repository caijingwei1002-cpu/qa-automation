# Day 14 验证证据

## 学习主题

总结 UI 自动化基础与局限：用端到端测试验证用户可观察的完整业务流程，同时明确它不能替代单元、API、性能、安全和兼容性测试。

## 目标产出

新增 `test-projects/01-todomvc-ui/tests/test_clear_completed.py`，覆盖：

1. 使用既有 fixture 准备一条 Active Todo 和一条 Completed Todo；
2. 点击用户可见的 `Clear completed` 控件；
3. 验证 Completed Todo 被清除；
4. 验证 Active Todo 保留；
5. 验证列表数量和未完成计数正确。

## 运行记录

### 受限环境首次运行

命令：

```powershell
.\.venv\Scripts\python.exe -m pytest test-projects/01-todomvc-ui/tests/test_clear_completed.py -q
```

结果：测试未进入业务步骤，在 `browser` fixture 启动 Playwright 时失败：

```text
PermissionError: [WinError 5] Access is denied
```

根因：当前受限环境禁止 Playwright 创建 Windows named pipe、启动浏览器驱动子进程。这不是 Clear completed 的定位器、断言或产品行为失败。

### 目标测试重跑

同一命令在允许启动 Playwright 子进程的环境中重跑：

```text
1 passed in 2.10s
```

### 完整回归

命令：

```powershell
python -m pytest test-projects/01-todomvc-ui/tests -q
```

结果：

```text
15 passed in 12.67s
```

## 失败清单

- 测试断言失败：无。
- 环境阻塞：1 次，Playwright named pipe 遇到 `WinError 5`；已在允许启动浏览器驱动的环境中重跑通过。
- 产品 Bug：未发现。
- 测试代码或定位器问题：未发现。
- 测试数据污染或同步问题：未发现。

## 调试证据

目标测试和完整回归最终均通过，因此没有新增失败截图或 Trace。首次环境阻塞的完整现象、调用层级和处理结果已记录在本文件中。

## 范围检查

- 新增文件：`test-projects/01-todomvc-ui/tests/test_clear_completed.py`、本验证文件。
- 未修改已有测试、fixture 或 pytest 配置。
- 原有未跟踪目录 `test-projects/01-todomvc-ui/screenshots/` 与本日任务无关，未删除、未纳入本日产出。
