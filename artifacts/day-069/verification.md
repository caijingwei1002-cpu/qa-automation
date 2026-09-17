# Day 69 验证证据

日期：2026-09-16
阶段：Restful Booker 收尾与测试代码质量
项目：test-projects/03-restful-booker-api
主题：API 阶段验收

## 目标测试

命令：

```text
.\.venv\Scripts\python.exe -m pytest test-projects/03-restful-booker-api/tests -q
```

结果：

```text
exit_code=0 (passed)
............................xxxxxx..x.x............xxxxxxxxxx........... [ 66%]
.....................................                                    [100%]
91 passed, 18 xfailed in 1.43s
```

## 全量回归

命令：

```text
.\.venv\Scripts\python.exe -m pytest test-projects/03-restful-booker-api/tests -q
```

结果：

```text
exit_code=0 (passed)
............................xxxxxx..x.x............xxxxxxxxxx........... [ 66%]
.....................................                                    [100%]
91 passed, 18 xfailed in 1.43s
```

## 关键验证

- 服务预检按 `config/targets.json` 使用 `npm start` 启动本地目标，`/ping` 返回 HTTP 201；运行编号为 `e5eab0ea23874d1f8253b8fdf539e3ad`。
- Ruff 静态检查通过：`All checks passed!`。
- Ruff 格式检查通过：`31 files already formatted`。
- smoke 复跑通过：`4 passed, 105 deselected in 0.19s`。
- smoke marker 收集为 `4/109 tests collected (105 deselected)`，实际包含认证、生命周期和健康检查。
- 完整回归带 `-rxX` 审查得到 `91 passed, 18 xfailed`，没有 `failed`、`error` 或 `XPASS`；18 条 xfail 均为 `strict=True` 并有登记理由。
- 初次 smoke 的 `WinError 10061 / connection refused` 已定位为服务未启动，服务启动后复跑通过；详见 `artifacts/day-069/additional-checks.md`。

## 环境问题与结论

- 工作目录：`D:\qa-automation-learning`。
- 失败需先记录根因、修复或当前阻塞，再完成当天学习。
- 本次运行：e5eab0ea23874d1f8253b8fdf539e3ad，来源 runner，时间 2026-09-16T02:52:10.834881+00:00；target=0，regression=0。
