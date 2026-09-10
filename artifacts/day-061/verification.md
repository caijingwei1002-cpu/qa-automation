# Day 61 验证证据

日期：2026-09-10  
阶段：Restful Booker 收尾与测试代码质量  
项目：test-projects/03-restful-booker-api  
主题：Client 单元测试与 Mock

## 目标测试

命令：

```text
.\.venv\Scripts\python.exe -m pytest test-projects/03-restful-booker-api/tests/test_api_client.py -q
```

结果：

```text
exit_code=0 (passed)
5 passed in 0.07s
```

目标测试完全 Mock `src.api_client.requests.request`，覆盖 timeout 与 URL/方法/params 传递、网络异常统一转换、异常上下文和敏感信息隔离、请求间 Header 隔离，以及调用方 Header 字典不被修改。

## 全量回归

命令：

```text
.\.venv\Scripts\python.exe -m pytest test-projects/03-restful-booker-api/tests -q
```

首次执行时端口 `3001` 没有监听，真实 HTTP 测试在 fixture/setup 阶段连接失败；Mock 测试不受影响。启动本地 Restful Booker 后 `/ping` 返回 `201`，重新执行结果：

```text
exit_code=0 (passed)
68 passed, 18 xfailed in 1.17s
```

## 静态检查

命令：

```text
.\.venv\Scripts\ruff.exe check test-projects/03-restful-booker-api/tests/test_api_client.py
.\.venv\Scripts\ruff.exe format --check test-projects/03-restful-booker-api/tests/test_api_client.py
```

结果：

```text
All checks passed!
1 file already formatted
```

## 关键验证

- timeout 测试通过 `assert_called_once_with` 检查 `GET`、完整 URL、params、默认 Header 和 `timeout=6.25`，并确认原始 Mock Response 原样返回。
- 异常测试参数化覆盖 `requests.Timeout` 与 `requests.ConnectionError`，均转换为 `ApiRequestError`，错误链中的 `__cause__` 保留底层异常。
- 异常消息包含方法、URL、timeout 和底层异常类型，但不包含 `secret-token`。
- 连续请求测试确认第一次的 `X-Trace` 和 Cookie 不会出现在第二次请求，`client.default_headers` 仍只有默认 `Accept`。
- 独立迁移测试确认 Client 不会修改调用方传入的 `custom_headers` 字典。

## 环境问题与结论

- 测试解释器：`D:\qa-automation-learning\.venv\Scripts\python.exe`。
- Mock 目标测试无需 Restful Booker 服务；全量回归中的真实 API 测试需要 `http://127.0.0.1:3001` 监听。
- 首次全量失败的根因为本地服务未启动；启动后 `/ping` 返回 `201`，全量回归恢复通过。
- 结论：HTTP Client 的 timeout 传递、异常边界、错误诊断和请求状态隔离均有可执行证据，Day 61 完成标准满足。
