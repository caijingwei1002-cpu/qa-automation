# Day 31 验证证据

## 验证命令

在 `test-projects/02-saucedemo-ui` 目录执行：

```powershell
python -m pytest tests -q
```

## 实际结果

```text
21 passed in 51.03s
```

运行输出保存在 `artifacts/day-031/pytest-full.txt`。

## 验证范围

- 登录测试、特殊用户测试和会话测试继续使用统一账号数据。
- 商品列表、商品详情、购物车、移除商品和排序相关测试继续通过。
- 结算校验、金额概览和完整下单流程继续通过。
- 用户、地址和商品事实数据集中在 `test-projects/02-saucedemo-ui/test_data.py`。
- `selected_products`、`CHECKOUT_REQUIRED_FIELD_CASES` 等场景组合仍由测试保留。
- 静态扫描确认测试文件不再重复包含具体用户、地址、商品名称和价格字面量。

## 问题、根因与处理

### SauceDemo 瞬时连接关闭

- 问题：第一次执行完整下单测试时出现 `net::ERR_CONNECTION_CLOSED`。
- 根因：外部 SauceDemo 连接在 fixture 导航阶段被关闭，未进入业务断言。
- 处理：保留该环境波动记录；稍后重试成功，最终回归结果为 `21 passed`。

### 从仓库根目录运行的模块路径问题

- 问题：从仓库根目录直接执行项目测试时，`test_data` 无法导入。
- 根因：当前测试工程的模块路径以 `test-projects/02-saucedemo-ui` 为工作目录。
- 处理：进入 SauceDemo 项目目录再运行测试，并在证据中记录正确运行边界。

## 结构验证

`test_data.py` 现在集中提供用户、结算地址、六个商品和完整商品目录；测试文件只保留场景选择、字段映射、参数组合和业务断言。
