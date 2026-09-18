# Restful Booker Platform 测试资产

本目录是测试学习工程中的 Day 70 资产登记目录，不是被测项目源码。被测项目源码固定在外部 targets 目录的 `D:\qa-automation-targets\restful-booker-platform\`，当前版本为 `d36bd3f8647a091d406e53bad463c5e5d2ece1`。

Day 70 先完成部署勘察和 API 集成级最小闭环：确认 Auth、Room、Booking 的真实契约，验证管理员认证、创建 Room、访客创建 Booking、查询关联和清理。正式证据位于 `artifacts/day-070/`。

当前尚未把测试代码扩展为完整套件。默认 Room 端口 `3001` 被外部旧项目占用，首轮验证临时使用 `3011`，该环境边界和 Room 删除后查询 `500` 的缺陷候选均已记录。

## Day 72：安全处置与默认 Room 回归

Day 72 将恢复默认端口设计成带授权闸门的环境操作。`stop_authorized` 默认必须为 `false`；没有明确授权时，只执行端口、PID、命令行、父进程、项目来源、版本配置和只读 HTTP 检查，不结束外部进程、不改端口、不改 Platform 产品代码。

本次 pre-snapshot 复核结果：

```text
3001 → PID 29528 → node.exe → node ./bin/www
Parent PID 19668 → D:\qa-automation-targets\restful-booker\...\cross-env.js
GET /room/actuator/health → 404 + X-Powered-By: Express
GET /room/ → 404 + X-Powered-By: Express
Platform HEAD = d36bd3f8647a
```

因此当前结论为 `BLOCKED_BY_AUTHORIZATION`：默认 Room 基线尚未恢复，不能进入 DELETE→GET `500` 回归。恢复时必须依次证明 PID/端口一致、3001 已释放、Platform Java/Room 进程来自 `d36bd3f`、health 为 `200/UP`、基础 Room GET 符合契约。详细 runbook 和原始证据见 `artifacts/day-072/recovery-runbook.md`。

## Day 73：UI/API 依赖边界与只读契约勘察

Day 73 将证据拆成两层：A 层读取 `assets` UI/BFF 源码，确认默认 API 依赖；B 层只对现有端口和 health/基础路径执行 GET，确认当前可达性和服务身份。源码默认配置确认：UI `3003`，Room `3001`，Booking `3000`，Auth `3004`；此外还存在 Branding `3002`、Report `3005`、Message `3006` 的静态依赖。

本次 live survey 结果：

```text
3000 → 无监听 → SERVICE_UNREACHABLE
3001 → PID 29528 / 外部 Node Express → SERVICE_IDENTITY_MISMATCH
3003 → 无监听 → SERVICE_UNREACHABLE
3004 → 无监听 → SERVICE_UNREACHABLE
```

Room 的两个 GET 均返回 Express `404`，不是 Platform Room 响应。今天未启动 `run_locally.cmd` 或 UI，未发送 POST/PUT/PATCH/DELETE，未生成业务数据，也未进入浏览器 E2E。详细依赖地图和原始结果见 `artifacts/day-073/ui-api-dependency-map.md`。

## Day 74：BFF 只读路由与错误归因

Day 74 将 Day 73 的依赖地图收敛为四条只读 BFF 勘察用例：Room 默认/override（R1/R2）和 Booking 默认/override（B1/B2）。统一证据闸门为：源码确认 GET-only → default/override → resolved target → BFF 可达 → 下游监听 → 服务身份 → 认证前置 → 目标 API 契约。

本日不启动 UI/BFF 或后端服务，不终止外部进程，不修改 `ROOM_API`/`BOOKING_API`，不执行登录或任何 POST/PUT/PATCH/DELETE。由于 UI/BFF 未启动、3000 无监听、3001 不是 Platform Room 且没有现成 token，四条用例均停在前置层；没有把代理 `200/500` 或错误服务响应升级为 Room/Booking 契约结论。

证据矩阵见 `artifacts/day-074/read-only-scope.md`，验证记录见 `artifacts/day-074/verification.md`。

## Day 75：BFF 错误映射与可观测性审查

Day 75 采用 BFF route + Mock HTTP client 审查四类受控下游输入：ConnectionError、下游 404、下游 500 和 Timeout。矩阵分别记录 BFF 对外 status/body/headers、内部 bff_status/downstream_status/exception_category、诊断字段和敏感信息隔离。

本日只验证 BFF mapping contract，不访问真实 Room，不启动服务，不修改环境，不执行登录或 POST/PUT/PATCH/DELETE。Mock 能证明 BFF 对受控输入的处理，不能证明真实 Room 的身份、认证、响应、错误原因或 API 契约。

证据矩阵见 `artifacts/day-075/bff-error-mapping-matrix.md`，验证记录见 `artifacts/day-075/verification.md`。
