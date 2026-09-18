# Day 75 — BFF 错误映射与可观测性 Mock 测试矩阵

## Scope

主测试层确定为 **BFF route 测试 + Mock HTTP client**。本层验证 route 是否实际进入异常处理、对外 `status/body/headers`、下游状态的诊断保留以及敏感信息泄漏；纯错误映射函数单测只能作为补充，不能替代 route-level 验证。

本阶段只验证 BFF mapping contract，不验证真实 Room 服务行为。禁止启动真实服务、修改 Platform 代码或环境、调用登录接口、执行 POST/PUT/PATCH/DELETE，以及把 Mock 结果写成真实 Room 契约结论。

## Test Shape

```text
BFF GET route
    ↓
Mock HTTP client
    ↓
注入受控下游结果
    ↓
调用 route
    ↓
检查外部 response
    +
检查内部 observability / logger
```

每条用例同时区分：

```text
bff_status
downstream_status
exception_category
```

三者不能合并成一个模糊的 `status` 字段。

## Mock Matrix

| 用例 | Mock 下游输入 | BFF 对外预期 | 内部诊断预期 | 允许结论 | 禁止的 Room 结论 |
| --- | --- | --- | --- | --- | --- |
| M1 ConnectionError | HTTP client 抛 `ConnectionError`，没有 HTTP response | `status=500`；`body=[]`；不透传下游 headers | `failure_category=connection_error`；`downstream_status=None`；记录 route/service/operation/trace（若已有） | BFF 能将连接异常映射为统一错误 | 不能说 Room API 返回 500 或 Room 契约失败；下游可能根本未产生 HTTP response |
| M2 下游 404 | HTTP client 返回可控 `404`、测试 body 和 headers | `status=500`；`body=[]`；不直接透传敏感 body/header | `failure_category=downstream_http_error`；`downstream_status=404`；保留安全 correlation 信息（若已有） | BFF 能将模拟下游 404 映射为自己的 500 | 不能证明真实 Room GET 返回 404，也不能判断 Room 的 404 契约正确/错误 |
| M3 下游 500 | HTTP client 返回可控 `500`、测试 body 和 headers | `status=500`；`body=[]`；不暴露原始内部错误 | `failure_category=downstream_http_error`；`downstream_status=500`；记录安全 request/trace 信息（若已有） | BFF 能映射并脱敏模拟下游 500 | 不能说真实 Room 发生内部错误，不能确定根因或 Room 契约失败 |
| M4 Timeout | HTTP client 抛 `Timeout`/`TimeoutError`，没有 HTTP response | `status=500`；`body=[]`；不伪造下游 HTTP status/header | `failure_category=timeout`；`downstream_status=None`；记录 timeout operation/trace（若已有） | BFF 能将超时异常映射为统一错误 | 不能说真实 Room API 返回 500，也不能证明真实 Room 发生超时 |

## Required Assertions

### 外部行为

已知产品行为可断言：

```text
response.status == 500
response.json() == []
```

对每种输入都要确认 route 确实使用了统一异常分支，而不是未处理异常泄漏。下游 404/500 的原始 body 和 headers 不应未经筛选直接出现在 BFF response。

### 三类状态区分

```text
ConnectionError:
  bff_status = 500
  downstream_status = None
  exception_category = connection_error

Downstream 404:
  bff_status = 500
  downstream_status = 404
  exception_category = downstream_http_error

Downstream 500:
  bff_status = 500
  downstream_status = 500
  exception_category = downstream_http_error

Timeout:
  bff_status = 500
  downstream_status = None
  exception_category = timeout
```

M3 必须同时记录 BFF `500` 和下游 `500`。两个数值相同，但语义不同；只保存一个 `status=500` 会丢失故障来源。

### 外部 headers 与敏感信息

Mock 下游可注入：

```text
Authorization: Bearer mock-secret-do-not-leak
Set-Cookie: session=mock-secret-do-not-leak
X-Internal-Token: mock-secret-do-not-leak
```

如果下游 body 含有同一测试 secret、内部 host、堆栈或数据库错误，至少检查两个出口：

```text
BFF response
captured diagnostic/log call（如果已有日志调用可观察）
```

外部 response 和已有诊断日志中不得出现 token、Cookie、Authorization、API key、内部凭据、未经筛选的敏感 body、数据库密码、SQL、完整内部路径或内部拓扑。

如果产品已有安全诊断字段，例如 `X-Request-ID` 或 `X-Correlation-ID`，可以验证其保留；不能凭空假设产品必须新增某个 header。

## Observability Review

理想的受控诊断信息包括：

```text
route
logical_downstream_service
operation
bff_status
downstream_status
exception_category
request_id / trace_id
timestamp
```

其中：

- 连接拒绝和超时没有下游 HTTP response，`downstream_status` 应为 `None`；
- 下游 404/500 才有 `downstream_status`；
- BFF 自己对外返回的 `bff_status=500` 不能冒充下游 status；
- 如果代码只记录 `request failed`，测试不能凭空要求完整结构化字段通过，应记录为“现有诊断不足以区分故障类型”。

## Evidence Boundary

Mock 测试能够证明：

- BFF route 是否捕获并映射受控异常；
- BFF 对外 status/body/headers 的行为；
- BFF 是否区分下游 HTTP error、connection error 和 timeout；
- 已有诊断字段是否保留安全故障类别；
- 敏感信息是否从 Mock 下游泄漏到 response 或可观察日志。

Mock 测试不能证明：

- 真实 Room 服务身份；
- 真实 Room 认证行为；
- 真实下游 status/body/headers；
- 真实连接拒绝或超时发生在 Room 服务；
- Room API 的真实契约是否通过或失败。

最终结论只能写成：

> 四类 Mock 用例证明 BFF Room GET route 在受控下游异常条件下的错误映射和可观测性行为；由于下游由 Mock 替代，没有访问真实 Room 服务，因此不形成 Room 服务身份、真实状态码、真实错误原因或 Room API 契约结论。

## Prohibited Actions

- 不启动 UI、BFF、Room、Booking、Auth；
- 不修改 `ROOM_API`、`BOOKING_API` 或其他环境变量；
- 不结束或迁移外部 Node 进程；
- 不执行登录、POST/PUT/PATCH/DELETE；
- 不将 Mock 404/500、connection error 或 timeout 写成 Platform Room live 证据。
