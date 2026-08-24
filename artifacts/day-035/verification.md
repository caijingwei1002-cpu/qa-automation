# Day 35 验证证据

## 验证目标

- 新增一条独立的跨页面回归场景。
- 验证商品名称和价格在购物车与结算概览页保持一致。
- 验证订单完成后购物车状态清空。
- 确认新增场景不破坏既有 SauceDemo UI 回归。

## 验证命令

在 `test-projects/02-saucedemo-ui` 目录执行：

```powershell
python -m pytest tests\test_portfolio_scenario.py -q
python -m pytest tests -q
```

## 实际结果

- 目标场景首次执行：`1 passed in 4.71s`。
- 文档与行尾格式整理后复验：`1 passed in 5.36s`。
- 完整回归：`22 passed in 74.70s`。
- 三次执行均成功退出。

## 验证范围

- 使用 `LoginPage` 完成标准用户登录。
- 使用 `InventoryPage` 加入两个商品并进入购物车。
- 使用 `CartPage` 读取购物车商品名称和价格。
- 使用 `CheckoutPage` 填写结算信息，并读取概览页商品名称和价格。
- 测试层负责构造预期集合、比较跨页面记录并断言订单完成状态。

## 结论

新增跨页面场景通过，完整回归由 21 条增加到 22 条且全部通过。页面结构与读取逻辑保留在 Page Object，业务预期、比较规则和断言保留在测试中。
