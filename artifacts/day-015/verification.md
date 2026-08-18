# Day 15 验证证据

## 学习主题

理解电商业务流和测试边界：今天只验证标准用户从登录页进入商品页，不把商品、购物车和结账流程混入登录测试。

## 目标产出

初始化 `test-projects/02-saucedemo-ui` 的最小测试结构，并完成标准用户登录测试：

- `pytest.ini`：配置测试发现、严格 marker 和 smoke/regression 标记；
- `tests/conftest.py`：提供浏览器、独立 context、页面、登录页和标准用户凭据 fixture；
- `tests/test_login.py`：填写标准用户凭据，点击 Login，验证 inventory URL 和 Products 标题。

## 运行记录

### 受限环境首次运行

命令：

```powershell
.\.venv\Scripts\python.exe -m pytest test-projects/02-saucedemo-ui/tests/test_login.py::test_standard_user_login -q
```

结果：测试未进入登录步骤，在 `browser` fixture 启动 Playwright 时遇到：

```text
PermissionError: [WinError 5] Access is denied
```

根因：当前受限环境禁止创建 Windows named pipe、启动 Playwright 浏览器驱动子进程。这不是账号、定位器、断言或 SauceDemo 产品行为失败。

### 授权环境目标测试

同一命令在允许启动 Playwright 子进程的环境中运行：

```text
1 passed in 6.00s
```

### 注释补充后的回归验证

为 `tests/conftest.py` 补充 fixture 职责和环境配置注释后，重新运行同一命令：

```text
1 passed in 4.16s
```

## 失败清单

- 测试断言失败：无。
- 环境阻塞：1 次，Playwright named pipe 遇到 `WinError 5`；已在允许启动浏览器驱动的环境中重跑通过。
- 产品 Bug：未发现。
- 测试代码或定位器问题：未发现。

## 证据与范围检查

- 证据目录：`artifacts/day-015/`。
- 本日目标文件：`test-projects/02-saucedemo-ui/tests/test_login.py`。
- 相关初始化文件：`test-projects/02-saucedemo-ui/pytest.ini`、`tests/conftest.py`。
- 未提前创建 Page Object、商品测试、购物车测试或结账测试。
- 未修改 TodoMVC 项目；既有 `test-projects/01-todomvc-ui/screenshots/` 未跟踪目录保持不变。
- 目标测试最终通过，因此没有新增失败截图或 Trace。

## 历史代码注释补充

按学习要求，为 Day 1–14 的 TodoMVC Python 代码补充了学习型注释，涉及 10 个文件：

- fixture 生命周期、context 隔离和失败证据逻辑；
- helper 的动作职责与不隐藏断言的边界；
- 输入边界、参数化数据和状态转换的业务含义；
- 语义 locator、集合断言、自动等待和回归范围的选择理由。

注释修改只增加说明，没有改变测试操作、定位器或断言逻辑。

### 注释后的旧代码验证

首次运行旧测试时，TodoMVC 服务未启动，所有 15 条测试在 `page.goto` 阶段遇到：

```text
Page.goto: net::ERR_CONNECTION_REFUSED at http://127.0.0.1:8080/
```

根因：测试约定的本地 TodoMVC 服务没有监听 8080；不是注释修改导致的测试失败。

启动已有 React 构建产物的本地静态服务器到 8080 后，重新运行：

```powershell
python -m pytest test-projects/01-todomvc-ui/tests -q
```

结果：

```text
15 passed in 13.01s
```
