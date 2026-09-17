# Day 69 附加验收检查

日期：2026-09-16
项目：`test-projects/03-restful-booker-api`

## 工作区范围

`git status --short` 显示仓库存在大量课程历史改动和未跟踪的工作流文件。本日新增的项目文件是 `test-projects/03-restful-booker-api/README.md`；这些既有改动没有被归入 Day 69 代码产出。

## 静态质量

命令：

```text
.\.venv\Scripts\python.exe -m ruff check test-projects/03-restful-booker-api
```

结果：`All checks passed!`

命令：

```text
.\.venv\Scripts\python.exe -m ruff format --check test-projects/03-restful-booker-api
```

结果：`31 files already formatted`

## 服务前置与 smoke

初次执行 smoke 时服务未启动，学习者提供的结果为：`4 failed, 105 deselected`；失败均为访问 `127.0.0.1:3001` 时的 `WinError 10061 / connection refused`。该结果归类为环境前置失败，不作为 API 业务回归结论。

统一验证器随后按 `config/targets.json` 使用 `npm start` 启动本地服务，健康检查 `/ping` 返回 HTTP 201，进程 PID 为 47980。

服务启动后的 smoke 命令：

```text
.\.venv\Scripts\python.exe -m pytest test-projects/03-restful-booker-api/tests -m smoke -q
```

结果：`4 passed, 105 deselected in 0.19s`

## Marker 收集

命令：

```text
.\.venv\Scripts\python.exe -m pytest test-projects/03-restful-booker-api/tests --collect-only -m smoke -q
```

结果：`4/109 tests collected (105 deselected in 0.15s)`；收集到认证有效/无效、完整生命周期和健康检查四条 smoke 用例。

## 完整回归与 xfail 审查

统一运行记录见 `run-record.json`，运行编号为 `e5eab0ea23874d1f8253b8fdf539e3ad`。目标与完整回归均为 `91 passed, 18 xfailed in 1.43s`，退出码均为 0。

18 条 xfail 均使用 `strict=True`，并按边界规则、业务规则、缺失必填字段和非法类型分组；带 `raises` 的用例还限定了预期异常类型。带 `-rxX` 的回归摘要逐项显示了登记原因，没有出现 `XPASS`、`failed` 或 `error`。

缺失 `firstname` 等 7 条用例的 xfail 原因记录的是当前实际 HTTP 500 与契约预期 400 的差异；该记录证明已观察行为，不扩展为未验证的服务端内部根因。

## 验收边界

本证据包支持的结论是：当前 API 测试项目在本次服务可用的执行环境中通过静态检查、smoke 和完整回归；18 条 xfail 均为已登记且受控的已知失败。结论不覆盖未执行的跨环境行为、未登记的产品缺陷或被测服务内部根因。
