# Day 24 验证证据

日期：2026-08-20

## 验证命令

```powershell
pytest test-projects/02-saucedemo-ui/tests/test_checkout_validation.py -q
```

## 实际结果

```text
3 passed in 17.74s
```

## 验证范围

- 参数化用例 `missing-first-name`：只清空 `firstName`，验证 `Error: First Name is required`。
- 参数化用例 `missing-last-name`：只清空 `lastName`，验证 `Error: Last Name is required`。
- 参数化用例 `missing-postal-code`：只清空 `postalCode`，验证 `Error: Postal Code is required`。
- 每个用例都验证校验失败后仍停留在 `checkout-step-one.html`。
- 每个用例从独立页面上下文开始，并经过登录、加入 Backpack、进入结算信息页的统一前置。

## 问题或阻塞及根因

无。用户在项目虚拟环境中执行命令，三个参数化用例全部通过，没有业务断言失败或环境阻塞。

## 产出检查

- 目标文件：`test-projects/02-saucedemo-ui/tests/test_checkout_validation.py`
- 知识落实：单变量隔离、字段—错误映射和未导航断言均已写入测试。
- 目标文件以外：本次未修改其他文件；既有工作区修改保持原样。
