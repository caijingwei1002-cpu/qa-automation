# Day 21 验证证据

日期：2026-08-19

## 验证命令

```powershell
pytest test-projects/02-saucedemo-ui/tests/test_cart.py::test_add_one_item -q
```

## 实际结果

```text
1 passed in 3.48s
```

## 验证范围

- 使用标准用户登录并进入商品列表
- 在 `Sauce Labs Backpack` 商品卡片内点击 `Add to cart`
- 验证购物车徽标为 `1`
- 验证进入购物车页面且只有一个商品项
- 验证购物车商品名称为 `Sauce Labs Backpack`
- 验证购物车商品价格为 `$29.99`

## 结论

Day 21 单商品加入购物车测试通过，数量状态、商品身份和价格在列表页与购物车页之间保持一致。

## 问题与阻塞

本次没有业务断言失败，也没有环境阻塞。

## 工作区观察

目标文件 `test_cart.py` 当前工作区包含完整实现；Git 暂存区存在旧的空版本，收尾提交前需要确认只提交完整文件。
