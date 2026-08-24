# SauceDemo 自动化测试工程

被测目标：`https://www.saucedemo.com/`

本目录只保存 SauceDemo 的 UI 测试代码、Page Object、测试数据和报告说明。SauceDemo 没有需要放进本仓库的完整官方 Web 源码，也不对在线站点做压力测试。

学习重点：登录、异常用户、商品、购物车、结算、Page Object、浏览器矩阵和稳定性。

## Day 34：HTML 报告与失败分类

以下命令均从仓库根目录 `D:\qa-automation-learning` 执行。

### 安装与运行

安装当前项目已验证的 Python 依赖与 Playwright 浏览器：

```powershell
python -m pip install -r test-projects\02-saucedemo-ui\requirements.txt
python -m playwright install chromium firefox
```

执行完整回归：

```powershell
python -m pytest test-projects\02-saucedemo-ui\tests -q
```

生成自包含 HTML 报告：

```powershell
python -m pytest test-projects\02-saucedemo-ui\tests -q `
  --html=artifacts\day-034\day34-report.html `
  --self-contained-html
```

### 报告包含的证据

自动化代码负责采集客观证据，不自动判断责任归属：

- 测试中的 `STEP:` 日志说明失败前执行到了哪个动作；
- pytest 与 Playwright 的错误堆栈保存预期值、实际值、定位器和调用日志；
- `pytest_runtest_makereport` 在测试主体的 `call` 阶段失败时截取当前页面；
- PNG 截图以 base64 附件嵌入 self-contained HTML，不依赖外部图片文件；
- `--failure-category` 和 `--failure-reason` 保存人工分析后的分类与理由。

分类必须由人根据证据明确传入。当前支持的稳定标识为：

| 参数值 | 报告中的分类 |
| --- | --- |
| `product` | 产品缺陷 |
| `script` | 脚本缺陷 |
| `environment` | 环境问题 |

未传入 `--failure-category` 时，hook 不猜测分类。`AssertionError` 只说明预期与实际不一致，本身不能证明责任属于产品或脚本。

### 产品、脚本与环境问题的判断标准

| 分类 | 判断标准 | 典型支持证据 |
| --- | --- | --- |
| 产品缺陷 | 页面、环境和测试步骤正常，但产品实际行为仍不符合正确预期 | 正确 URL 已加载；定位器有效；人工也能复现错误行为；截图或接口响应显示产品状态错误 |
| 脚本缺陷 | 产品行为正常，但自动化实现、数据或预期值错误 | DOM 中目标存在；定位器或等待策略失效；测试预期与需求不符；修正脚本后稳定通过 |
| 环境问题 | 产品逻辑和测试实现没有明显错误，失败由运行条件造成 | 浏览器无法启动；服务不可达；网络或资源超时；环境变量、浏览器版本或权限与正常环境不同 |

“找不到元素”“断言失败”和“测试超时”只是失败现象，不是分类结论。结论必须能引用报告中的 URL、步骤、堆栈、截图或环境差异。

### 本次受控失败分析

为了验证报告能力，登录用例曾临时把商品页标题的正确预期 `Products` 改为 `Products-INTENTIONAL-FAILURE`。该临时改动只用于生成失败证据，随后已恢复。

- 现象：`test_standard_user_login` 在商品页标题断言处失败；
- 步骤：登录、验证商品列表 URL、验证商品列表标题三条 `STEP:` 均进入 Captured log；
- 页面状态：已成功进入 `https://www.saucedemo.com/inventory.html`；
- 元素证据：`.title` 成功定位，实际文本为 `Products`；
- 错误预期：测试脚本要求 `Products-INTENTIONAL-FAILURE`；
- 截图证据：报告中的 `Failure Screenshot` 显示商品页已正常渲染；
- 分类：脚本缺陷；
- 理由：产品返回了正确标题，浏览器和页面链路均正常，失败由测试代码中的错误预期值直接造成。

带步骤、堆栈、截图和分类附件的报告位于：

```text
artifacts/day-034/day34-classified-failure.html
```

受控失败命令如下。它应在临时错误预期存在时返回 `1 failed`，不能把该退出码误判为报告机制失败：

```powershell
python -m pytest `
  test-projects\02-saucedemo-ui\tests\test_login.py::test_standard_user_login `
  -q `
  --failure-category=script `
  --failure-reason="页面实际显示 Products，测试脚本故意使用了错误预期值" `
  --html=artifacts\day-034\day34-classified-failure.html `
  --self-contained-html
```

### 恢复、验证与分析边界

受控失败取证后，标题断言已恢复为 `Products`。正式验证结果为：

```text
21 passed in 73.87s
```

正式验证命令：

```powershell
python -m pytest test-projects\02-saucedemo-ui\tests -q
```

当前截图 hook 只处理已有 `saucedemo_page` 的测试主体失败。浏览器启动失败、fixture setup 失败等环境问题可能发生在页面创建之前，因此不会有页面截图，需要结合错误堆栈、权限、网络和环境配置判断。

单次失败也不能直接称为 flaky。只有在代码、数据和环境条件保持一致时重复执行，并观察到结果在通过与失败之间波动，才有证据将其作为 flaky 问题继续分析。
