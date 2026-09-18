# Day 72 验证证据

日期：2026-09-17
阶段：Restful Booker Platform
项目：test-projects/05-booker-platform
主题：安全处置与默认 Room 回归

## 目标测试

命令：

```text
git diff --check
```

结果：

```text
exit_code=0 (passed)
<no output>
```

## 全量回归

命令：

```text
git diff --check
```

结果：

```text
exit_code=0 (passed)
<no output>
```

## 关键验证

- 恢复 runbook 与 pre-snapshot：[recovery-runbook.md](recovery-runbook.md)。
- 操作前复核时间：`2026-09-17T15:17:14.2873156+08:00`。
- `3001` 仍由 PID `29528` 监听；该 PID 为 `node.exe`，命令行为 `node ./bin/www`，父进程 PID `19668` 指向 `D:\qa-automation-targets\restful-booker` 的 `cross-env.js`。
- Platform 源码 HEAD 为 `d36bd3f8647a`，Room 默认配置为 `3001` 和 `/room`，工作区状态无输出。
- `GET /room/actuator/health` → `404 Not Found` + `X-Powered-By: Express`。
- `GET /room/` → `404 Not Found` + `X-Powered-By: Express`。
- 本轮 `stop_authorized=false`，未执行停止、迁移、启动服务或状态变更 API。
- `python tools/validate_repo.py`：`exit_code=0`；`git diff --check`：`exit_code=0`。

## 环境问题与结论

- 工作目录：`D:\qa-automation-learning`。
- 当前结论：`BLOCKED_BY_AUTHORIZATION`。3001 外部 Node/Express 占用已复核，但没有明确停止授权；Platform Room 默认基线未恢复，不进入 DELETE→GET `500` 回归。
- 本次不是 Platform 产品缺陷结论，也不是 Room 启动失败；只记录环境前置未满足。
- 本次运行：f0229f47caa94d57baf9056fb7e7bdd2，来源 runner，时间 2026-09-17T07:18:44.351768+00:00；target=0，regression=0。
