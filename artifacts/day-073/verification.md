# Day 73 验证证据

日期：2026-09-17
阶段：Restful Booker Platform
项目：test-projects/04-booker-platform
主题：UI/API 依赖边界与只读契约勘察

## 目标测试

命令：

```text
git diff --check
```

结果：

```text
exit_code=0 (passed)
warning: in the working copy of 'LEARNING-NOTES.md', LF will be replaced by CRLF the next time Git touches it
```

## 全量回归

命令：

```text
git diff --check
```

结果：

```text
exit_code=0 (passed)
warning: in the working copy of 'LEARNING-NOTES.md', LF will be replaced by CRLF the next time Git touches it
```

## 关键验证

- 依赖地图与原始结果：[ui-api-dependency-map.md](ui-api-dependency-map.md)。
- A 层源码确认：`assets/package.json` 的 UI dev/start 端口为 `3003`；`assets/next.config.js` 默认 `BOOKING_API=3000`、`ROOM_API=3001`、`AUTH_API=3004`，并存在对应 `/api/*` rewrite。
- B 层端口结果：`3000`、`3003`、`3004` 无监听；`3001` 由 PID `29528` 监听。
- `GET /booking/actuator/health`、`GET http://localhost:3003/`、`GET /auth/actuator/health` 均 connection refused，分类为 `SERVICE_UNREACHABLE`。
- `GET /room/actuator/health` 和 `GET /room/` 均为 `404 Not Found` + `X-Powered-By: Express`；PID 为 `node.exe`，命令行为 `node ./bin/www`，父进程指向外部 `restful-booker`，分类为 `SERVICE_IDENTITY_MISMATCH`。
- 未启动 `run_locally.cmd` 或 UI，未发送 POST/PUT/PATCH/DELETE，未生成业务数据，未修改端口/env/源码。
- `python tools/validate_repo.py`：`exit_code=0`；`git diff --check`：`exit_code=0`。

## 环境问题与结论

- 工作目录：`D:\qa-automation-learning`。
- 当前结论：源码依赖地图和 live 只读分类完成，但不等于 `E2EReady`。Room 默认 `3001` 仍为 `SERVICE_IDENTITY_MISMATCH`，Booking/Auth/UI 分别不可达或未启动；不进入 UI E2E 或业务闭环。
- 当前结果属于依赖/环境勘察，不是 Platform UI、API 或业务产品缺陷结论。
- 本次运行：30387cd4b08b42c8a07b85321b0e344f，来源 runner，时间 2026-09-17T07:45:21.906856+00:00；target=0，regression=0。
