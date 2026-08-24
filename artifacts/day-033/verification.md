# Day 33 验证证据

## 验证命令

在 `test-projects/02-saucedemo-ui` 目录执行：

```powershell
python -m pytest tests -m smoke -q --browser=chromium --base-url=https://www.saucedemo.com/
python -m pytest tests -m smoke -q --browser=firefox --base-url=https://www.saucedemo.com/
```

## 实际结果

| 浏览器 | 结果 | pytest 用时 | 进程退出码 |
| --- | --- | ---: | ---: |
| Chromium | `1 passed, 20 deselected` | 2.73s | 0 |
| Firefox | `1 passed, 20 deselected` | 5.01s | 0 |

原始输出保存在 `smoke-chromium.txt` 和 `smoke-firefox.txt`。

## 验证范围

- 通过 `--browser=chromium` 和 `--browser=firefox` 选择 Playwright 浏览器。
- 两个浏览器都执行同一组 smoke 测试，避免把浏览器差异混同为测试范围差异。
- 使用 `--base-url` 明确指定同一个目标环境。
- 记录通过结果和执行成本，为后续决定浏览器覆盖范围提供依据。

## 问题、根因与处理

### Firefox 浏览器包缺失

- 问题：初始环境只有 Chromium，Firefox 安装目录不存在。
- 根因：Playwright 浏览器二进制包与 Python `playwright` 库独立安装。
- 处理：安装 Playwright Firefox 1538 浏览器包后重新执行，Firefox smoke 通过。

## 结论

当前兼容性矩阵为 Chromium × smoke、Firefox × smoke。Firefox 用时约为 Chromium 的 1.8 倍，因此后续完整回归应按风险和变更范围选择浏览器，不应机械复制全部执行成本。
