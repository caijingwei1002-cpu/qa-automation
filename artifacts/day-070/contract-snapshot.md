# Day 70 契约快照

来源：外部 checkout `D:\qa-automation-targets\restful-booker-platform`，commit `d36bd3f8647a091d406e53bad463c5e5d2ece1`。

- Auth：`POST /auth/login`，管理员凭据 `admin/password`，成功 `200` 并设置 `token` Cookie；`POST /auth/validate` 成功 `200`。
- Room：默认 `3001`、context `/room`；创建 `POST /room/` 需 Cookie，成功 `201`；删除成功 `202`；Room 标识为 `roomid`。
- Booking：默认 `3000`、context `/booking`；创建 `POST /booking/` 不要求认证，成功 `201`；Booking 标识为 `bookingid`；管理查询和删除使用 `token` Cookie。
- 关联：Booking 使用 `roomid` 引用 Room；首轮日期使用未来、`checkin < checkout` 的动态区间。
- 首轮不填 `email/phone`，避免引入 message 服务依赖；首轮只启动 auth、room、booking。

## 证据边界

这些是固定版本源码与运行结果支持的首轮契约，不等于已经覆盖全部权限、日期冲突、并发、UI 或其他服务规则。默认 `3001` 被旧 Node 服务占用，因此首轮 Room 运行验证曾使用 `3011`；正式默认端口复核仍是后续动作。
