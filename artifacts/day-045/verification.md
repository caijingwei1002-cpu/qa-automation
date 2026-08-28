# Day 45 验证证据

日期：2026-08-26
主题：API Client

## API 全量回归

命令：

```text
.\.venv\Scripts\python.exe -m pytest test-projects/03-restful-booker-api/tests -q
```

结果：

```text
..............                                                           [100%]
14 passed in 0.37s
```

## 结构验证

- Client 实现位于 `test-projects/03-restful-booker-api/src/api_client.py`。
- `tests/conftest.py` 提供 `api_client` fixture，统一注入 base URL 和 timeout。
- API 测试不再直接调用 `requests.get/post/put/patch/delete`。
- 默认 `Accept` header、URL 拼接和 timeout 由 Client 统一处理。
- Client 不断言业务状态码；网络异常上下文包含 method、URL、params、timeout 和脱敏响应摘要。
- Token、Cookie 和密码不会被写入错误摘要。
