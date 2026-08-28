# Day 46 验证证据

日期：2026-08-26
主题：Booking Client

## API 全量回归

命令：

```text
.\.venv\Scripts\python.exe -m pytest test-projects/03-restful-booker-api/tests -q
```

结果：

```text
..............                                                           [100%]
14 passed in 0.73s
```

## 关键验证

- `BookingClient` 位于 `src/booking_client.py`，依赖通用 `RestfulBookerClient`。
- booking 创建、列表查询、详情查询、PUT、PATCH 和 DELETE 测试已通过领域方法表达。
- 领域方法返回原始 `Response`，测试继续验证状态码、响应结构和业务字段。
- 鉴权 Token 仍由通用 `api_client` 获取，没有把 AuthClient 扩展到本日范围。
- 无 Token 的 PUT 场景仍验证 `403`，重复 DELETE 场景仍验证 `405`。
