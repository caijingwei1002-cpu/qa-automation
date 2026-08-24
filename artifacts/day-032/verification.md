# Day 32 验证证据

## 验证命令

在 `test-projects/02-saucedemo-ui` 目录执行：

```powershell
python -m pytest tests -m smoke -q --base-url=https://www.saucedemo.com/
python -m pytest tests -m smoke -q --base-url=not-a-url
```

## 实际结果

合法地址：

```text
1 passed, 20 deselected in 2.64s
EXIT_CODE=0
```

非法地址：

```text
ValueError: base_url 必须是完整的 http(s) URL
1 error, 20 deselected
EXIT_CODE=1
```

原始输出分别保存在 `smoke-valid.txt` 和 `smoke-invalid.txt`。

## 验证范围

- `config.py` 按命令行参数、`SAUCEDEMO_URL` 环境变量、默认 URL 的顺序解析地址。
- 合法 `--base-url` 被 `saucedemo_page` fixture 使用并完成 smoke 测试。
- 非法 `--base-url` 在 fixture 阶段被明确拒绝，没有静默进入浏览器。
- `page.goto()` 只执行导航；配置解析和页面准备分别由配置函数与 fixture 负责。

## 问题、根因与处理

### 受限执行环境的 Playwright 权限错误

- 问题：第一次由受限执行器运行合法 smoke 时出现 `WinError 5`。
- 根因：浏览器进程创建权限属于执行环境限制，不是 `base_url` 逻辑错误。
- 处理：在允许的本地执行权限下重跑，得到 `1 passed`；最终证据只保留正式结果。
