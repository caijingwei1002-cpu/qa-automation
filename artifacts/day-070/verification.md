# Day 70 验证证据

日期：2026-09-17
阶段：Restful Booker Platform
项目：test-projects/05-booker-platform
主题：部署勘察与 API 最小闭环

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

- 源码版本固定为 `d36bd3f8647a091d406e53bad463c5e5d2ece1`；契约依据来自 Auth、Room、Booking 的 Controller/Service/Model 和配置。
- 健康检查：Auth `3004`、Booking `3000`、Platform Room 临时 `3011` 均返回 `200` 且 `status=UP`。
- 认证：login `200` 并取得 `token` Cookie；validate `200`。
- 业务闭环：创建 Room `201`、创建 Booking `201`、Room/Booking/按 roomid 查询均 `200`，`booking.roomid == room.roomid == 4`。
- 清理：DELETE Booking 和 Room 均 `202`；删除后 Booking 查询 `404`。
- 完整原始步骤和响应摘要：`artifacts/day-070/api-happy-path.json`。

## 环境问题与结论

- 工作目录：`D:\qa-automation-learning`。
- 默认 Room `3001` 被外部旧项目 Node 进程占用，不能把该端口上的服务当作 Platform Room；未终止无关进程，临时使用 `3011` 完成真实业务验证。
- 完整 Maven Reactor 构建在 Room 集成测试阶段因同一外部 `3001` 占用失败；Auth/Booking 模块通过，三项可执行 JAR 均已产出。
- Room 删除后 `GET /room/{id}` 实际为 `500`；`RoomService` 的 `404` 意图与 `RoomDB.query()` 无条件 `ResultSet.next()` 的实现不一致，作为后续缺陷回归候选记录，未修改产品代码。
- 本次运行：b61949d25af844e999ce1bbf74c85d72，来源 runner，时间 2026-09-17T05:49:08.612615+00:00；target=0，regression=0。
