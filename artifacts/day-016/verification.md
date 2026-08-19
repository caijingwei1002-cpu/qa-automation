# Day 16 验证证据

日期：2026-08-18
阶段：SauceDemo UI 框架
主题：登录负向场景与错误信息断言

## 目标

- 在 `test-projects/02-saucedemo-ui/tests/test_login.py` 中增加错误密码和空用户名两个独立负向测试。
- 每个负向测试都验证正确错误提示，并确认没有进入 `/inventory.html`。
- 保留标准用户成功登录 smoke 测试，并确认新增场景没有破坏它。

## 运行记录

目标测试：

```powershell
.\.venv\Scripts\python.exe -m pytest test-projects/02-saucedemo-ui/tests/test_login.py::test_wrong_password_shows_error -q
```

结果：`1 passed in 5.40s`

空用户名测试：

```powershell
.\.venv\Scripts\python.exe -m pytest test-projects/02-saucedemo-ui/tests/test_login.py::test_empty_username_shows_error -q
```

结果：`1 passed in 6.12s`

完整登录测试文件：

```powershell
.\.venv\Scripts\python.exe -m pytest test-projects/02-saucedemo-ui/tests/test_login.py -q
```

首次完整验证结果：`3 passed in 10.84s`
补充文件末尾换行后重新验证：`3 passed in 12.67s`

静态检查：`git diff --check` 无错误；仅出现 Windows LF/CRLF 转换提示。

## 场景与断言覆盖

| 场景 | 操作 | 错误提示 | 成功状态排除 |
| --- | --- | --- | --- |
| 标准用户登录 | 有效用户名 + 有效密码 | 无 | URL 为 `/inventory.html`，标题为 `Products` |
| 错误密码 | 有效用户名 + `wrong_password` | `Username and password do not match any user in this service` | 不进入 `/inventory.html` |
| 空用户名 | 空用户名 + 有效密码 | `Username is required` | 不进入 `/inventory.html` |

## 范围检查

- 实际修改只有目标文件 `test-projects/02-saucedemo-ui/tests/test_login.py`。
- 未修改 `conftest.py`、`pytest.ini` 或其他项目代码。
- `test-projects/01-todomvc-ui/screenshots/` 保持未跟踪，未纳入本日产出。
- 本日没有业务断言失败；测试使用项目虚拟环境并在允许启动 Playwright 子进程的环境中执行。此前记录的 `WinError 5` 属于浏览器启动环境阻塞，不是本日登录逻辑失败。

## 知识落地

负向测试按不同业务规则拆分为独立函数：错误密码验证认证失败，空用户名验证必填字段校验。每个场景同时断言“正确错误反馈”和“没有进入成功页面”，避免只验证没有跳转而漏掉错误文案错误或页面卡死等问题。
