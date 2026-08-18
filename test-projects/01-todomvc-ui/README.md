# TodoMVC 自动化测试工程

被测项目：`D:\qa-automation-targets\todomvc`

来源：[tastejs/todomvc](https://github.com/tastejs/todomvc)

本目录只保存 TodoMVC 的 Playwright/Pytest 测试代码、配置、数据和测试文档。先在外部被测项目目录按其 README 启动页面，再通过 `TODO_MVC_URL` 配置测试地址。

学习重点：定位、交互、业务断言、筛选、参数化、fixture、失败截图和 Trace。

## Pytest 配置与运行

本项目的 pytest 配置位于 `pytest.ini`，测试目录默认为 `tests/`，并注册了两个测试标记：

- `smoke`：快速验证新增、完成、删除和筛选 Todo 等关键路径；
- `regression`：完整回归测试，包含全部现有用例。

在本目录执行：

```powershell
..\..\.venv\Scripts\python.exe -m pytest -m smoke -q
..\..\.venv\Scripts\python.exe -m pytest -m regression -q
..\..\.venv\Scripts\python.exe -m pytest -q
```

也可以从仓库根目录指定测试目录执行：

```powershell
.\.venv\Scripts\python.exe -m pytest test-projects/01-todomvc-ui/tests -m smoke -q
```
