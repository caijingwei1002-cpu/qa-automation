# Day 34 验证证据

## 验证目标

- HTML 报告包含可追踪的测试步骤；
- 失败报告包含错误堆栈和页面截图；
- 人工确认的失败分类及理由进入同一报告；
- 恢复受控错误后，完整 SauceDemo UI 回归通过。

## 受控失败

登录用例曾临时把商品页标题的正确预期 `Products` 改成 `Products-INTENTIONAL-FAILURE`，用于验证失败证据和分类机制。

在 `test-projects/02-saucedemo-ui` 目录执行：

```powershell
python -m pytest `
  .\tests\test_login.py::test_standard_user_login `
  -q `
  --failure-category=script `
  --failure-reason="页面实际显示 Products，测试脚本故意使用了错误预期值" `
  --html=..\..\artifacts\day-034\day34-classified-failure.html `
  --self-contained-html
```

实际结果：`1 failed in 8.49s`，进程退出码为 1。该失败是受控场景的预期结果，不代表报告生成失败。

## 报告证据核对

本地 canonical 报告为 `day34-classified-failure.html`。报告已核对包含：

- 三条 `STEP:` Captured log；
- 错误预期 `Products-INTENTIONAL-FAILURE`；
- 实际值 `Products` 和成功解析的 `.title` 元素；
- `Failure Screenshot` 自包含 PNG 附件；
- `Failure Classification` 文本附件；
- 分类：脚本缺陷；
- 理由：页面实际显示 `Products`，测试脚本故意使用了错误预期值。

截图附件解码后为 290,209 字节，PNG 文件签名为 `89 50 4E 47 0D 0A 1A 0A`。

仓库的 `.gitignore` 默认忽略生成的 HTML 报告，因此该 Markdown 保存验证摘要和重建命令；HTML 保留在本地 `artifacts/day-034/` 中。

## 分类结论

- 现象：登录测试在商品页标题断言处失败；
- 产品证据：登录成功，URL 为 `/inventory.html`，`.title` 正常渲染为 `Products`；
- 环境证据：Python、pytest、Playwright、浏览器和目标页面执行链均正常；
- 脚本证据：自动化代码使用了人为错误的预期值；
- 结论：脚本缺陷，不是产品缺陷或环境问题。

报告 hook 只采集客观证据。分类由人分析后，通过 `--failure-category` 和 `--failure-reason` 显式写入报告。

## 恢复与正式验证

取证完成后，标题预期已恢复为 `Products`。在 `test-projects/02-saucedemo-ui` 目录执行：

```powershell
python -m pytest .\tests -q
```

实际结果：`21 passed in 73.87s`，进程退出码为 0。

## 分析边界

- 当前截图 hook 只覆盖已有 `saucedemo_page` 的测试主体失败；setup 阶段的浏览器或环境失败可能没有截图；
- `AssertionError` 只能证明预期与实际不一致，不能自动确定责任归属；
- 单次失败不能证明 flaky，需要在相同代码、数据和环境条件下重复执行并观察通过/失败波动。
