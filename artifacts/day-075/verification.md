# Day 75 验证证据

日期：2026-09-18
阶段：Restful Booker Platform
项目：test-projects/05-booker-platform
主题：BFF 错误映射与可观测性审查

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

- `artifacts/day-075/bff-error-mapping-matrix.md` 存在，且包含 Scope、Test Shape、M1-M4 Mock Matrix、Required Assertions、Observability Review、Evidence Boundary 和 Prohibited Actions。
- 矩阵分别覆盖 `ConnectionError`、下游 `404`、下游 `500` 和 `Timeout`，并明确 `bff_status`、`downstream_status`、`exception_category` 三类字段不能合并。
- 矩阵同时记录外部 response 断言、已有诊断字段的审查边界和 `mock-secret-do-not-leak` 脱敏检查；没有凭空要求产品已经实现新的诊断 header。
- 矩阵明确 Mock 只能证明 BFF mapping contract，不能证明真实 Room 身份、真实下游响应或 Room API 契约。
- 验证过程没有启动真实服务、没有访问真实 Room、没有修改产品代码/环境，也没有执行状态变更请求。

## 环境问题与结论

- 工作目录：`D:\qa-automation-learning`。
- 失败需先记录根因、修复或当前阻塞，再完成当天学习；本次没有未解释的失败。
- `--skip-service` 只验证 artifact 和仓库边界，不代表真实 Room/Booking API live 契约通过。
- 本次运行：`b327518206074a01b88121f23164bf9f`，来源 runner，时间 `2026-09-18T03:02:59.039742+00:00`；target=0，regression=0。
