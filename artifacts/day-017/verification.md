# Day 17 验证证据

日期：2026-08-19
阶段：SauceDemo UI 框架
主题：特殊用户与风险场景

## 目标

- 使用 `locked_out_user` 验证锁定账号拒绝登录的业务规则。
- 使用 `problem_user` 验证认证成功，并记录登录后商品页面的实际异常状态。
- 不修改公共 fixture 或 pytest 配置，不把未经确认的异常硬编码成通过条件。

## 运行记录

锁定用户目标测试：

```powershell
.\.venv\Scripts\python.exe -m pytest test-projects/02-saucedemo-ui/tests/test_users.py::test_locked_out_user_cannot_login -q
```

结果：`1 passed in 6.06s`

问题用户观察测试：

```powershell
.\.venv\Scripts\python.exe -m pytest test-projects/02-saucedemo-ui/tests/test_users.py::test_problem_user_login_records_product_state -q -s
```

结果：`1 passed in 3.63s`

## 问题用户观察结果

`problem_user` 完成登录并进入 `/inventory.html`，商品页标题为 `Products`，页面渲染出 6 个商品图片节点。

实际收集到的图片状态如下：

```text
Sauce Labs Backpack             → /assets/sl-404-Cq1a9k9X.jpg
Sauce Labs Bike Light           → /assets/sl-404-Cq1a9k9X.jpg
Sauce Labs Bolt T-Shirt         → /assets/sl-404-Cq1a9k9X.jpg
Sauce Labs Fleece Jacket        → /assets/sl-404-Cq1a9k9X.jpg
Sauce Labs Onesie               → /assets/sl-404-Cq1a9k9X.jpg
Test.allTheThings() T-Shirt     → /assets/sl-404-Cq1a9k9X.jpg
```

观察结论：认证和商品列表加载成功，但 6 个不同商品的图片资源都指向同一个 `sl-404` 资源。这是客观观察记录，是否作为产品 Bug 仍需结合产品预期或缺陷记录确认；测试没有为了保持绿色而忽略该现象。

特殊用户完整测试文件：

```powershell
.\.venv\Scripts\python.exe -m pytest test-projects/02-saucedemo-ui/tests/test_users.py -q
```

结果：`2 passed in 8.05s`

## 场景与断言覆盖

| 账号 | 预期 | 实际验证 |
| --- | --- | --- |
| `locked_out_user` | 显示 `Sorry, this user has been locked out.`，不能进入商品页 | 锁定错误提示和非 `/inventory.html` 均通过 |
| `problem_user` | 能进入商品页，并记录页面异常 | URL、`Products` 标题、6 个图片节点通过；图片资源异常已记录 |

## 范围与问题记录

- 目标文件：`test-projects/02-saucedemo-ui/tests/test_users.py`。
- 未修改 `conftest.py`、`pytest.ini` 或其他项目代码。
- Git 暂存区原先存在一个空的 `test_users.py`，工作区是完整实现；提交前会显式重新暂存完整文件，避免只提交空文件。
- `test-projects/01-todomvc-ui/screenshots/` 保持未跟踪，未纳入本日产出。
- 本日没有测试断言失败；Playwright 在授权环境中正常启动。
