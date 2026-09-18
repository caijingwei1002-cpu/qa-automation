# Day 73：UI/API 依赖地图与 live 只读勘察

## 范围与安全边界

本日分为两层，二者互不替代：

- **A 层：源码依赖地图**，确认 UI 默认依赖、route、method、认证和环境变量覆盖。
- **B 层：live GET 勘察**，确认端口可达性、PID、进程来源、响应特征和服务身份。

允许源码读取、配置读取、进程查询、端口查询和 HTTP `GET/HEAD`。禁止执行 `npm run dev`、`run_locally.cmd`、POST/PUT/PATCH/DELETE、停止进程、修改端口/env/源码。

## A 层：依赖地图

| UI route / 功能 | UI/BFF 源码 | 后端服务 | 默认地址 | 后端 path/method | 认证 | 只读性 | 环境覆盖 | 证据 |
|---|---|---|---|---|---|---|---|---|
| 首页可用房间/日期筛选 | `assets/src/components/home/Availability.tsx` | Room | `http://localhost:3001` | `/api/room` → `/room/`，GET；带日期时加 query | 无 | Read-only | `ROOM_API` | `next.config.js`、组件源码 |
| 预订详情房间读取 | `assets/src/app/reservation/[id]/page.tsx` | Room | `http://localhost:3001` | `/api/room/{id}` → `/room/{id}`，GET | 无 | Read-only | `ROOM_API` | 页面与 BFF route |
| 管理端房间列表/详情 | `assets/src/components/admin/RoomListings.tsx`, `RoomDetails.tsx` | Room | `http://localhost:3001` | `/api/room`, `/api/room/{id}`，GET | Admin 页面有 token 前置；GET route 本身不读取 token | Read-only | `ROOM_API` | 组件与 `api/room` routes |
| 管理端预订列表/摘要 | `assets/src/components/admin/BookingListings.tsx` | Booking | `http://localhost:3000` | `/api/booking/?roomid=...`、`/api/booking/summary?roomid=...`，GET | BFF 从 Cookie 读取 token | Read-only | `BOOKING_API` | 组件与 BFF route |
| 管理端登录/认证校验 | `assets/src/components/admin/Login.tsx`, `assets/src/app/admin/layout.tsx` | Auth | `http://localhost:3004` | `/api/auth/login`、`/api/auth/validate`，POST | token Cookie/body | Mutating/session-changing | `AUTH_API` | route 源码；本日不调用 |

额外静态依赖：`BRANDING_API → 3002`、`REPORT_API → 3005`、`MESSAGE_API → 3006`。它们由 `next.config.js` 配置，但不在本日核心 live survey 范围内。

源码默认依赖和 live 服务身份必须分开记录，不能用静态配置替代运行时证明。

## B 层：live survey

| 服务 | 端口/PID | 进程身份 | GET | 状态/响应特征 | 分类 | 证据 |
|---|---|---|---|---|---|---|
| Auth | 3004 无监听 | 无 PID | `/auth/actuator/health` | connection refused | `SERVICE_UNREACHABLE` | 端口/GET 原始命令 |
| Booking | 3000 无监听 | 无 PID | `/booking/actuator/health` | connection refused | `SERVICE_UNREACHABLE` | 端口/GET 原始命令 |
| Room | 3001 → PID 29528 | `node.exe`；`node ./bin/www`；父进程指向外部 `restful-booker` | `/room/actuator/health`, `/room/` | 两者均 `404 Not Found`，`X-Powered-By: Express` | `SERVICE_IDENTITY_MISMATCH` | 端口/PID/进程/GET |
| UI | 3003 无监听 | 无 PID | `/` | connection refused；本日未启动 UI | `SERVICE_UNREACHABLE` | 端口/GET 原始命令 |

分类只允许使用：

```text
SERVICE_UNREACHABLE
SERVICE_IDENTITY_MISMATCH
SERVICE_IDENTITY_UNCONFIRMED
CONTRACT_OR_API_FAILURE
```

## 结论门槛

```text
DependencyMapComplete
+ LiveReadOnlySurveyComplete
≠ E2EReady
```

即使 UI 根页面返回 `200`，只要 Room 默认 `3001` 仍不是 Platform Room，不能启动 UI 或进入浏览器 E2E。

## A 层源码证据

```text
assets/package.json:
  dev/start → port 3003

assets/next.config.js:
  BOOKING_API → http://localhost:3000
  ROOM_API    → http://localhost:3001
  AUTH_API    → http://localhost:3004
  rewrites: /api/room/* → <ROOM_API>/room/*
           /api/booking/* → <BOOKING_API>/booking/*
           /api/auth/* → <AUTH_API>/auth/*
```

`assets/src/app/api/room/route.ts` 的 GET 将请求转发到 `${ROOM_API}/room/`，失败时 BFF 返回空数组和 `500`；同文件的 POST 读取 token Cookie，但本日未调用。Booking GET route 读取 token 并要求 `roomid`，Auth login/validate routes 都是 POST，本日只做源码确认。

`run_locally.cmd` 会启动后端和 `npm run dev`，并包含 `taskkill` 清理逻辑；因此本日禁止执行该脚本。

## B 层 live 原始结果

```text
3000: no LISTENING
GET /booking/actuator/health → curl connection refused

3001: LISTENING PID 29528
GET /room/actuator/health → 404 Not Found + X-Powered-By: Express
GET /room/ → 404 Not Found + X-Powered-By: Express

3003: no LISTENING
GET / → curl connection refused

3004: no LISTENING
GET /auth/actuator/health → curl connection refused
```

当前 `3001` 的 PID 证据：`node.exe`，命令行 `node ./bin/www`，父进程 PID `19668`，父命令行指向 `D:\qa-automation-targets\restful-booker` 的 `cross-env.js`，因此分类为 `SERVICE_IDENTITY_MISMATCH`，不是 `CONTRACT_OR_API_FAILURE`。

## Day 73 结论

`d36bd3f` 下 UI 默认依赖关系已由源码确认，3000/3001/3003/3004 的 live 状态已按只读证据分类。源码依赖地图和 live survey 均完成，但这不等于 `E2EReady`：Room 默认 `3001` 仍不是 Platform Room，UI 未启动，Auth/Booking 也不可达，因此本日不证明 UI、API 或业务闭环可用。
