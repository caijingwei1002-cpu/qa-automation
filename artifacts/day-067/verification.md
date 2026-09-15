# Day 67 验证证据

日期：2026-09-15
阶段：Restful Booker 收尾与测试代码质量
项目：test-projects/03-restful-booker-api
主题：缺陷案例与报告

## 目标测试

命令：

```text
.\.venv\Scripts\python.exe -m pytest test-projects/03-restful-booker-api/tests -q
```

结果：

```text
exit_code=0 (passed)
............................xxxxxx..x.x...........xxxxxxxxxx............ [ 66%]
....................................                                     [100%]
90 passed, 18 xfailed in 1.98s
```

## 全量回归

命令：

```text
.\.venv\Scripts\python.exe -m pytest test-projects/03-restful-booker-api/tests -q
```

结果：

```text
exit_code=0 (passed)
............................xxxxxx..x.x...........xxxxxxxxxx............ [ 66%]
....................................                                     [100%]
90 passed, 18 xfailed in 1.98s
```

## 关键验证

- 服务预检启动本地 Restful Booker，`GET /ping` 返回 HTTP 201，证明本次诊断已进入真实 API 请求。
- 请求由 `test_invalid_payloads.py` 从合法 booking 基线仅删除 `firstname` 后发送；测试断言记录 `expected_status=400`。
- 实际响应为 HTTP 500，响应体为 `Internal Server Error`；`--runxfail` 显式得到 `1 failed`，失败点为 `assert 500 == 400`。
- 该次响应未解析出 `bookingid`，清理逻辑没有发现可登记资源；是否存在未返回 ID 的副作用仍属未知。

## 环境问题与结论

- 工作目录：`D:\qa-automation-learning`。
- 失败需先记录根因、修复或当前阻塞，再完成当天学习。
- 首次直接运行因 `127.0.0.1:3001` 未监听而得到 `WinError 10061`，归类为服务 readiness 问题；随后按登记配置启动本地服务并通过 `/ping` 预检。
- 诊断失败不是环境连接错误：服务启动后稳定复现契约差异 `Expected 400 / Actual 500`。服务端根因尚未由日志或源码确认。
- 本次运行：55a653ed18bc47d5a99b1d1868b321ed，来源 runner，时间 2026-09-15T07:33:25.784998+00:00；target=0，regression=0。
