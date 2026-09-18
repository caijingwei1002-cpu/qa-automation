# Day 74 验证证据

日期：2026-09-17
阶段：Restful Booker Platform
项目：test-projects/04-booker-platform
主题：BFF 只读路由与错误归因

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

- `artifacts/day-074/read-only-scope.md` 存在，且包含 Scope、Evidence Gates、R1/R2/B1/B2、Evidence Field Matrix、Current Stop Summary 和 Conclusion。
- 证据矩阵明确记录 default/override/resolved target、BFF 可达、下游监听、服务身份、认证前置、分类和停止层。
- 文档明确禁止启动服务、终止进程、修改环境变量以及执行 POST/PUT/PATCH/DELETE。
- 文档没有新增 Day 74 live HTTP 结果；`3001` 的身份不符、`3000` 无监听、UI/BFF 未启动和无现成 token 均引用 Day 73 已有证据或当前已知事实。
- 当前四条用例均在最早可确定的前置层停止：R1/R2/B1/B2 的首层为 `BFF_UNAVAILABLE`；更深层的 `3001 SERVICE_IDENTITY_MISMATCH`、`3000 DOWNSTREAM_UNAVAILABLE` 和 Booking `AUTH_PRECONDITION_UNMET` 单独保留，未升级为目标 API 契约结论。

## 环境问题与结论

- 工作目录：`D:\qa-automation-learning`。
- 本次验证未启动服务、未新增 HTTP 请求、未产生业务状态变更；`--skip-service` 是本课安全范围的一部分，不代表 Platform API 已通过。
- 失败需先记录根因、修复或当前阻塞，再完成当天学习；本次没有未解释的失败。
- 本次运行：`dae86bedc4a346419c94abd69a8f4fb3`，来源 runner，时间 `2026-09-17T09:08:12.084484+00:00`；target=0，regression=0。
