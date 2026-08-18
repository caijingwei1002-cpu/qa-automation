# Day 13 验证证据

## 学习主题

按风险选择回归范围：优先覆盖核心路径、状态联动、边界输入和历史易错点，并区分产品、测试实现、环境、数据污染和同步问题。

## 目标产出

新增 `test-projects/01-todomvc-ui/tests/test_regression.py`，通过一个跨功能场景验证：

1. 创建两个 Todo；
2. 完成其中一个；
3. 验证 Active 和 Completed 筛选；
4. 返回 All 后删除已完成 Todo；
5. 验证剩余文本和未完成计数。

## 运行记录

### 初始命令失败

命令：

```powershell
pytest test-projects/01-todomvc-ui/tests/test_regression.py -q
```

结果：未执行测试。当前 PowerShell 的 PATH 中没有 `pytest` 命令。

根因：项目虚拟环境存在，但没有激活或直接使用其中的 Python 解释器；这不是测试断言、定位器或 TodoMVC 产品行为失败。

处理：激活 `.venv`，使用 `python -m pytest`，确保 pytest 由项目虚拟环境执行。

### 目标测试

命令：

```powershell
python -m pytest test-projects/01-todomvc-ui/tests/test_regression.py -q
```

结果：

```text
1 passed in 2.26s
```

### 完整回归

命令：

```powershell
python -m pytest test-projects/01-todomvc-ui/tests -q
```

结果：

```text
14 passed in 12.08s
```

## 失败清单

- 测试失败：无。
- 环境阻塞：1 次，原因是初始命令未找到 `pytest`；已通过激活项目虚拟环境解决。
- 产品 Bug：未发现。
- 测试代码或定位器问题：未发现。
- 测试数据污染或同步问题：未发现。

## 调试证据

本次目标测试和完整回归均通过，因此没有失败截图或 Trace。运行结果和环境阻塞根因已记录在本文件中。

## 范围检查

- 新增文件：`tests/test_regression.py`、本验证文件。
- 未修改已有测试、fixture 或 pytest 配置。
- 原有未跟踪目录 `test-projects/01-todomvc-ui/screenshots/` 与本日任务无关，未删除、未纳入本日产出。
