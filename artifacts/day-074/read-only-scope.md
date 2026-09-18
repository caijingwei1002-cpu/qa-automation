# Day 74 — BFF 只读范围与证据矩阵

## Scope

本文件整理 Day 74 的 BFF 只读路由、前置闸门和错误归因边界。

本阶段只基于源码与已有环境证据，不新增 live HTTP 请求，且明确禁止：

- 启动 UI、BFF、Room、Booking、Auth 或其他服务；
- 终止、重启、替换现有进程，或抢占/释放端口；
- 修改 `ROOM_API`、`BOOKING_API` 或其他环境变量；
- 执行 `POST`、`PUT`、`PATCH`、`DELETE`，包括调用登录接口获取 token；
- 创建、更新或删除 Room/Booking；
- 将错误服务的响应当作 Platform Room/Booking 契约证据。

## Evidence Gates

统一判断顺序：

```text
源码确认 GET-only
→ 默认值 / override 解析
→ resolved target
→ BFF 是否可达
→ 下游是否监听
→ 下游服务身份是否正确
→ 认证前置是否满足
→ 才允许比较目标 API 契约
```

任一硬前置不成立，都在该层停止，不继续比较下游业务契约。`TARGET_API_CONTRACT_OBSERVATION` 只能作为所有前置通过后的结果，不能作为默认结论。

## Current Environment Facts

已有事实为：

- UI/BFF 未启动；
- `3001` 当前由外部 `restful-booker` Node/Express 服务占用，不是 Platform Room；
- `3000` 当前无监听；
- 当前没有现成可复用的合法 token；
- 本阶段不通过登录请求获取 token；
- 本阶段不修改任何 API override。

因此四条用例当前主要产出源码解析、目标解析规则和既有环境证据，不新增 BFF live 证据。

## 最小用例集

### R1 — Room 默认目标只读勘察

| 项目 | 设计 |
| --- | --- |
| 源码依据 | BFF 存在 `GET /api/room`，路由属于读取路径；默认 Room base URL 为 `http://localhost:3001`；Room GET 无额外 token 前置 |
| 默认/override | 无 `ROOM_API` 时使用默认 `3001`；有 `ROOM_API` 时使用已有 override；本阶段只读取，不创建、修改或删除 override |
| 请求 | 仅在 BFF 已可达且其他前置满足时执行 `GET /api/room` |
| 证据 | 时间、method/path、resolved target、target source、BFF 可达、下游监听、服务身份、status、Content-Type、有限响应摘要、分类和停止层 |
| 分类 | BFF 不可达 → `BFF_UNAVAILABLE`；下游无监听 → `DOWNSTREAM_UNAVAILABLE`；身份不是 Platform Room → `SERVICE_IDENTITY_MISMATCH`；身份正确但 BFF 处理失败 → `BFF_FAILURE`；全部前置成立后才可进入 `TARGET_API_CONTRACT_OBSERVATION` |
| 停止 | BFF 不可达、目标无监听、目标身份不符或无法确认身份时停止，不比较 Room 状态码语义、字段或业务数据 |

当前状态：由于 UI/BFF 未启动，首个执行闸门是 `BFF_UNAVAILABLE`。此外，默认 `3001` 已有 `SERVICE_IDENTITY_MISMATCH` 证据；该事实不能被扩展成 Platform Room 契约证据。

### R2 — Room override 解析勘察

| 项目 | 设计 |
| --- | --- |
| 源码依据 | 路由仍为 `GET /api/room`；`ROOM_API` 可覆盖默认地址；override 只改变 resolved target，不改变 GET-only 边界 |
| 解析规则 | `ROOM_API` 存在且有效 → 使用 override；不存在 → fallback 到 `http://localhost:3001` |
| 请求 | 不主动设置或删除 override；只有 BFF、监听、身份等前置成立时，才允许执行同一个 `GET /api/room` |
| 证据 | `ROOM_API` 是否存在、resolved target、target source（default/override）、监听与身份、BFF status/摘要、分类和停止层 |
| 分类 | override 目标无监听 → `DOWNSTREAM_UNAVAILABLE`；目标可达但身份不符 → `SERVICE_IDENTITY_MISMATCH`；身份正确但 BFF 失败 → `BFF_FAILURE`；前置全通过后才可比较目标契约 |
| 停止 | BFF 不可达、override 目标无监听、身份未知或身份不是 Platform Room时停止；即使目标返回 `200`，身份未确认也不能判定 Room 契约通过 |

当前状态：不修改环境且 UI/BFF 未启动，R2 首先停在 `BFF_UNAVAILABLE`。若实际解析回默认 `3001`，则保留已有的 `SERVICE_IDENTITY_MISMATCH` 作为更深层环境证据。

### B1 — Booking 默认目标只读勘察

| 项目 | 设计 |
| --- | --- |
| 源码依据 | BFF 存在 `GET /api/booking`；默认 Booking base URL 为 `http://localhost:3000`；该查询需要管理员 token Cookie |
| 默认/override | 无 `BOOKING_API` 时使用默认 `3000`；有 `BOOKING_API` 时使用已有 override；不修改配置 |
| 认证 | 只有已有合法 token/session 才能执行认证态 GET；不调用 `POST /auth/login`，不伪造或修改 token |
| 请求 | 只有 BFF 可达、目标监听、身份正确且已有合法认证上下文时，才允许执行 `GET /api/booking` |
| 证据 | 时间、method/path、resolved target、target source、auth present/absent（不保存 token/Cookie 值）、BFF 可达、监听、服务身份、status、Content-Type、有限摘要、分类和停止层 |
| 分类 | BFF 不可达 → `BFF_UNAVAILABLE`；目标无监听 → `DOWNSTREAM_UNAVAILABLE`；身份不符 → `SERVICE_IDENTITY_MISMATCH`；无合法 token → `AUTH_PRECONDITION_UNMET`；身份与认证正确但 BFF 失败 → `BFF_FAILURE` |
| 停止 | BFF 不可达、目标无监听、身份未知/不符或无现成 token时停止，不比较 Booking 契约 |

当前状态：UI/BFF 未启动，`3000` 无监听，且无现成 token。因此 B1 首先停在 `BFF_UNAVAILABLE`；更深层还存在 `DOWNSTREAM_UNAVAILABLE` 与 `AUTH_PRECONDITION_UNMET`，不能执行认证态 Booking GET。

### B2 — Booking override 解析勘察

| 项目 | 设计 |
| --- | --- |
| 源码依据 | 路由为 `GET /api/booking`；`BOOKING_API` 可覆盖默认 `http://localhost:3000`；override 不改变认证要求或只读边界 |
| 解析规则 | override 存在 → 使用 `BOOKING_API`；不存在 → fallback 到默认 `3000` |
| 认证 | 无论 default 还是 override，都必须已有合法 token/session；override 不能跳过认证前置 |
| 请求 | 不修改 override；只有 BFF、监听、身份和认证全部成立时，才允许执行 `GET /api/booking` |
| 证据 | `BOOKING_API` 是否存在、resolved target、target source、auth present/absent、监听、服务身份、BFF status/摘要、分类和停止层 |
| 分类 | 目标无监听 → `DOWNSTREAM_UNAVAILABLE`；目标不是 Booking 服务 → `SERVICE_IDENTITY_MISMATCH`；无 token → `AUTH_PRECONDITION_UNMET`；全部前置成立但 BFF 失败 → `BFF_FAILURE` |
| 停止 | BFF 不可达、目标无监听、身份不符/未知、无现成 token，或无法证明请求落到目标 Booking API时停止 |

当前状态：UI/BFF 未启动，B2 首先停在 `BFF_UNAVAILABLE`。若无 override 而 fallback 到默认 `3000`，已有环境事实进一步构成 `DOWNSTREAM_UNAVAILABLE`；无 token 仍构成 `AUTH_PRECONDITION_UNMET`。

## Evidence Field Matrix

| 字段 | R1 | R2 | B1 | B2 |
| --- | --- | --- | --- | --- |
| route / method | 必须 | 必须 | 必须 | 必须 |
| default target | 必须 | 必须 | 必须 | 必须 |
| override key | 必须 | 必须 | 必须 | 必须 |
| resolved target / source | 必须 | 必须 | 必须 | 必须 |
| auth required | 记录 | 记录 | 记录 | 记录 |
| auth present/absent | optional | optional | required | required |
| BFF reachable | 必须 | 必须 | 必须 | 必须 |
| downstream listening | 必须 | 必须 | 必须 | 必须 |
| downstream identity | 必须 | 必须 | 必须 | 必须 |
| HTTP status/body | live only | live only | live only | live only |
| classification / stop layer | 必须 | 必须 | 必须 | 必须 |

允许使用的分类：

```text
BFF_UNAVAILABLE
DOWNSTREAM_UNAVAILABLE
SERVICE_IDENTITY_MISMATCH
AUTH_PRECONDITION_UNMET
BFF_FAILURE
TARGET_API_CONTRACT_OBSERVATION
```

## Current Stop Summary

| 用例 | 当前停止层 | 依据 |
| --- | --- | --- |
| R1 | `BFF_UNAVAILABLE` | UI/BFF 未启动；默认 `3001` 另有身份不符证据 |
| R2 | `BFF_UNAVAILABLE` | 不修改 override，当前无法建立 BFF live 链路 |
| B1 | `BFF_UNAVAILABLE` | UI/BFF 未启动；同时 `3000` 无监听且无 token |
| B2 | `BFF_UNAVAILABLE` | 不修改 override；默认路径仍受 `3000` 无监听和无 token 阻断 |

## Conclusion

Day 74 当前有效结论是：证据链必须在最早失败的前置层停止。当前不足以进入 Room 或 Booking 的目标 API 契约比较，因此只保留源码解析、default/override/resolved target 规则，以及已有监听与服务身份事实；不新增 HTTP 证据，不产生状态变更。

来源：

- `artifacts/day-073/ui-api-dependency-map.md`
- `artifacts/day-073/verification.md`
- `config/project-lessons.json`
