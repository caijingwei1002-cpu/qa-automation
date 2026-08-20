# Day 25 验证证据

日期：2026-08-20

## 验证命令

```powershell
pytest test-projects/02-saucedemo-ui/tests/test_checkout_summary.py -q
```

## 实际结果

首次执行结果：`1 failed in 34.10s`

修复后重新执行结果：

```text
1 passed in 4.67s
```

## 验证范围

- 登录标准用户、加入 Sauce Labs Backpack 并进入 Checkout overview 页面。
- 使用独立预期价格 `$29.99` 验证商品小计。
- 从概览页读取小计、税费和总价，并转换为 `Decimal`。
- 验证税费为正数。
- 验证总价等于商品小计加税费。

## 问题或阻塞及根因

- 现象：首次执行在 `.summary_subtotal` 的 `inner_text()` 处超时，1 条测试失败。
- 根因：SauceDemo 概览页实际使用 `.summary_subtotal_label`、`.summary_tax_label`、`.summary_total_label`；页面文本还包含 `Item total: $29.99` 一类标签前缀，原定位器和简单去除 `$` 的解析逻辑都不匹配。
- 修复：改用真实 `_label` 定位器，并用正则提取 `$` 后金额再转换为 `Decimal`。
- 复验：修复后目标测试通过，结果为 `1 passed in 4.67s`；无剩余阻塞。

## 产出检查

- 目标文件：`test-projects/02-saucedemo-ui/tests/test_checkout_summary.py`
- 知识落实：独立金额预期、Decimal 解析、税费正数和总价不变量均已写入测试。
- 目标文件以外：本日代码产出只新增目标测试和本证据文件；既有工作区修改保持原样。
