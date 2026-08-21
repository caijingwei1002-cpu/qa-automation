# Day 28 验证证据

## 验证命令

在 `test-projects/02-saucedemo-ui` 目录执行：

```powershell
& D:\qa-automation-learning\.venv\Scripts\python.exe -m pytest tests/test_login.py -q
```

按 daily-plan 中的仓库根目录路径，并临时补充项目模块路径执行：

```powershell
$env:PYTHONPATH = 'D:\qa-automation-learning\test-projects\02-saucedemo-ui'
& D:\qa-automation-learning\.venv\Scripts\pytest.exe test-projects/02-saucedemo-ui/tests/test_login.py -q
```

## 实际结果

```text
3 passed in 14.47s
3 passed in 7.76s
3 passed in 10.75s (清理注释后复验)
```

## 验证范围

- `test_standard_user_login`：通过 `LoginPage.login()` 完成标准用户登录，测试保留 URL 和商品页标题业务断言。
- `test_wrong_password_shows_error`：通过页面对象完成错误密码登录，测试断言精确错误文案和未进入商品页。
- `test_empty_username_shows_error`：通过页面对象完成空用户名登录，测试断言精确必填错误文案和未进入商品页。
- 登录页的用户名、密码、登录按钮和错误提示 locator 集中在 `pages/login_page.py`。

## 问题、根因与处理

### 重构初版语法错误

- 问题：初版把 `login_page = LoginPage(saucedemo_page)` 写进测试函数参数列表。
- 根因：混淆了 fixture 参数声明和函数体内的对象初始化。
- 处理：恢复 fixture 参数签名，在函数体内创建 `LoginPage`，并将登录操作改为 `login_page.login(...)`。

### 仓库根目录导入失败

- 问题：从仓库根目录按计划路径收集时出现 `ModuleNotFoundError: No module named 'pages'`。
- 根因：`pages` 位于 SauceDemo 项目目录内，仓库根目录启动 pytest 时该项目目录未自动进入模块搜索路径。
- 处理：默认验证在 `test-projects/02-saucedemo-ui` 项目目录执行；为复现 daily-plan 的仓库根目录路径，又用仅作用于当前进程的 `PYTHONPATH` 重跑通过，未引入额外路径配置。

### Playwright 权限阻塞

- 问题：受限环境首次在项目目录运行时出现 `WinError 5`，Playwright 子进程无法创建。
- 根因：当前执行环境的进程/命名管道权限限制，不是测试断言失败。
- 处理：在授权环境重跑同一目标测试，最终 3 条用例通过。
