# Day 72：默认 Room 恢复 runbook

## 安全闸门

```text
stop_authorized = false
```

默认只读。没有明确授权时，不执行 `Stop-Process`、`taskkill`、迁移端口、启动替代服务或修改任何代码/配置。

## 恢复证据链

1. **Pre-snapshot**：记录时间、`3001 → PID`、进程名、可执行路径、命令行、父进程、项目来源、当前两个 GET 原始响应、Platform commit 和默认配置。
2. **PID identity re-check**：重新读取预期 PID，并确认进程身份未变；同时确认 `3001` 仍由该 PID 监听。PID 变化或命令行不一致时取消停止动作。
3. **Authorization gate**：只有明确授权、确认无其他依赖、知道恢复方式且不修改 Platform 产品代码/默认端口时，才允许受控停止。
4. **Port release**：停止后重新检查 `3001`；只有无监听者且没有新 PID 接管时，才允许进入启动阶段。否则记录新占用者并退回身份确认。
5. **Room start**：按 `d36bd3f` 的默认配置启动 Room，不绕到其他端口。
6. **Room identity**：证明 `3001 → Java PID → restful-booker-platform/room`，并将启动来源与 `d36bd3f`、工作区状态关联。
7. **Baseline gate**：`health 200/UP` 且 `GET /room/` 符合 Room 契约后，设置 `RoomBaselineReady = true`；否则记录 `PRECONDITION FAILED` 并停止。
8. **Defect regression**：只有 `RoomBaselineReady = true` 才允许后续 DELETE→GET 回归；本 runbook 本轮不执行该业务操作。

## 只读 pre-snapshot 结果

检查时间：`2026-09-17T15:17:14.2873156+08:00`

### 端口与进程

```text
TCP  0.0.0.0:3001  0.0.0.0:0  LISTENING  29528
TCP  [::]:3001     [::]:0     LISTENING  29528

ProcessId         : 29528
Name              : node.exe
CommandLine       : node ./bin/www
ParentProcessId   : 19668
ParentName        : node.exe
ParentCommandLine : "node" "D:\qa-automation-targets\restful-booker\node_modules\.bin\\..\cross-env\dist\bin\cross-env.js" SEED=true node ./bin/www
```

可执行路径仍为 Node.js 安装目录；端口与 PID 身份复核一致，未发生 PID 变化。

### Platform 版本与配置

```text
HEAD: d36bd3f8647a
server.port = 3001
server.servlet.context-path=/room
```

Room 工作区 `git status --short` 无输出。

### 只读 HTTP

```text
GET /room/actuator/health → HTTP/1.1 404 Not Found
X-Powered-By: Express
Body: Not Found

GET /room/ → HTTP/1.1 404 Not Found
X-Powered-By: Express
Body: Not Found
```

### 授权结论

当前没有本轮明确停止授权，因此结论为 `BLOCKED_BY_AUTHORIZATION`。只读检查已完成，身份与端口一致；状态变更动作必须停止。Platform Room 默认 `3001` 基线仍未恢复，不进入 DELETE→GET 回归。

## 失败分类

```text
身份复核失败       → PRECONDITION FAILED / identity_changed
未获停止授权       → BLOCKED_BY_AUTHORIZATION
停止后仍有监听者   → PRECONDITION FAILED / port_not_released
Room 启动失败      → PRECONDITION FAILED / room_startup
health 或基础 GET 失败 → PRECONDITION FAILED / room_baseline
```
