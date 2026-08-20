# Day 27 验证证据

日期：2026-08-20

## 验证命令

```powershell
pytest test-projects/02-saucedemo-ui/tests/test_session.py -q
```

## 实际结果

```text
1 passed in 5.39s
```

## 验证范围

- 使用独立页面上下文登录标准用户，并确认 `/inventory.html` 与 `Products` 页面状态。
- 打开菜单执行 Logout，验证回到登录页且用户名、密码和 Login 控件可见。
- 登出后直接访问 `/inventory.html`，验证仍被重定向到登录页。
- 再次确认登录表单可见，证明受保护商品页不能在失效会话下直接访问。

## 问题或阻塞及根因

无。中间的单测试检查和最终完整命令均通过，没有业务断言失败或环境阻塞；IDE 输出中的 `debugpy` 提示不是测试失败。

## 产出检查

- 目标文件：`test-projects/02-saucedemo-ui/tests/test_session.py`
- 知识落实：登出页面行为、直接访问受保护路由和会话失效后置条件均已写入测试。
- 目标文件以外：本日代码产出只新增目标测试和本证据文件；既有工作区修改保持原样。
