# Day 71 验证证据

日期：2026-09-17
阶段：Restful Booker Platform
项目：test-projects/05-booker-platform
主题：默认端口基线与服务身份

## 目标测试

命令：

```text
git diff --check
```

结果：

```text
exit_code=0 (passed)
warning: in the working copy of 'LEARNING-NOTES.md', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'config/targets.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'tools/build_daily_plan.py', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'tools/validate_repo.py', LF will be replaced by CRLF the next time Git touches it
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
warning: in the working copy of 'config/targets.json', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'tools/build_daily_plan.py', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'tools/validate_repo.py', LF will be replaced by CRLF the next time Git touches it
```

## 关键验证

- 只读 preflight 原始记录：[room-3001-preflight.md](room-3001-preflight.md)。
- `3001` → PID `29528` → `node.exe`，命令行和父进程指向 `D:\qa-automation-targets\restful-booker`。
- Platform 源码目录为 `D:\qa-automation-targets\restful-booker-platform`，commit 为 `d36bd3f8647a`，默认配置为 `3001` 和 `/room`。
- `GET /room/actuator/health` 与 `GET /room/` 在当前 `3001` 上均为 Express `404 Not Found`，因此当前端口不是 Platform Room。
- `python tools/validate_repo.py`：`exit_code=0`，仓库结构、目标配置、生成计划和 Git 边界通过。
- 未执行终止进程、修改端口、修改代码/配置、启动服务或 POST/PUT/DELETE 请求。

## 环境问题与结论

- 工作目录：`D:\qa-automation-learning`。
- 失败需先记录根因、修复或当前阻塞，再完成当天学习。
- 本次运行：20b688d4cc894c38995e752b7f9068e8，来源 runner，时间 2026-09-17T06:39:46.866303+00:00；target=0，regression=0。
