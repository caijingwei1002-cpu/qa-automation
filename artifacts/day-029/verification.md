# Day 29 验证证据

## 验证命令

在 `test-projects/02-saucedemo-ui` 目录执行：

```powershell
& D:\qa-automation-learning\.venv\Scripts\python.exe -m pytest tests/test_inventory.py tests/test_cart.py -q
```

## 实际结果

```text
3 passed in 12.86s
```

## 验证范围

- `test_inventory_list_is_complete`：通过 `LoginPage` 登录和 `InventoryPage` 读取商品列表，测试保留数量、名称集合、价格和图片属性断言。
- `test_add_one_item`：通过 `InventoryPage` 加购并进入购物车，通过 `CartPage` 验证商品身份和价格跨页面一致。
- `test_add_multiple_items_and_verify_cart`：通过页面对象批量加购，通过 `CartPage.item_records()` 提取名称—价格数据，测试保留集合和 Decimal 合计断言。
- 静态检查确认目标测试不再直接使用登录、商品卡片或购物车结构 locator；`git diff --check` 通过。

## 问题、根因与处理

### 重构中变量定义遗漏

- 问题：`test_add_one_item` 使用 `expected_name` 和 `expected_price`，但替换页面操作时一并删除了它们的定义。
- 根因：把业务 Expected 与页面操作代码一起替换，混淆了页面对象抽取和测试数据保留边界。
- 处理：恢复独立的商品名称和价格预期，继续让测试负责业务断言。

### 旧数据提取循环未删除

- 问题：多商品测试已经调用 `CartPage.item_records()`，但旧的逐项 locator 循环仍保留，造成重复追加和直接 locator 残留。
- 根因：抽取页面对象后没有删除被替代的旧实现。
- 处理：删除旧循环，只使用 `item_records()` 读取页面数据；数量、集合和 Decimal 断言保持在测试中。

### 环境与运行入口

- 目标测试在项目目录使用授权环境运行通过；仓库根目录运行 Page Object 测试时需要显式加入 SauceDemo 项目路径，沿用 Day 28 已记录的运行入口约束。
- 本次未修改 pytest 配置，也未处理工作区中既有的 TodoMVC 截图目录。
