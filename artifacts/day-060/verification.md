# Day 60 验证证据

日期：2026-09-10  
阶段：Restful Booker 收尾与测试代码质量  
项目：test-projects/03-restful-booker-api  
主题：预期失败治理

## 目标测试

命令：

```text
.\.venv\Scripts\python.exe -m pytest test-projects/03-restful-booker-api/tests/test_business_rules.py -q
```

结果：

```text
exit_code=0 (passed)
4 passed, 2 xfailed in 0.27s
```

两个 `XFAIL` 分别对应已经确认的业务缺陷：

- `checkout` 早于 `checkin` 时接口仍创建 booking；
- 负数 `totalprice` 时接口仍创建 booking。

## 全量回归

命令：

```text
.\.venv\Scripts\python.exe -m pytest test-projects/03-restful-booker-api/tests -q
```

结果：

```text
exit_code=0 (passed)
63 passed, 18 xfailed in 1.40s
```

## 静态检查

命令：

```text
.\.venv\Scripts\ruff.exe check test-projects/03-restful-booker-api/tests/test_business_rules.py
.\.venv\Scripts\ruff.exe format --check test-projects/03-restful-booker-api/tests/test_business_rules.py
```

结果：

```text
All checks passed!
1 file already formatted
```

## 故障隔离验证

### 网络异常

临时设置 `RESTFUL_BOOKER_URL=http://127.0.0.1:3999` 后运行日期负向测试，认证请求抛出 `ApiRequestError`（底层为连接拒绝），pytest 显示 `FAILED`，没有被 `xfail` 隐藏。清除临时环境变量后恢复默认服务地址。

### `--runxfail` 验证

命令：

```text
.\.venv\Scripts\python.exe -m pytest test-projects/03-restful-booker-api/tests/test_business_rules.py -q --runxfail
```

结果：

```text
exit_code=1 (expected for this diagnostic run)
2 failed, 4 passed in 0.38s
```

两个失败都直接来自 `raise KnownBusinessDefect(...)`。这证明 `xfail` 只是对已知缺陷的报告标记；取消标记后，已确认缺陷会成为真实失败。失败过程中没有出现清理异常，说明 `finally` 仍执行了资源回收。

## 关键验证

- 两个负向测试均使用 `strict=True` 与 `raises=KnownBusinessDefect`，只接受已确认的业务缺陷类型。
- 网络、认证、JSON 解析、代码错误和 `BookingCleanupError` 都不会被该 `xfail` 标记掩盖。
- `_extract_booking_id()` 在业务断言前执行，意外创建的资源可以进入 `finally` 清理。
- `_cleanup_booking()` 对当前资源、DELETE 响应和删除后 GET `404` 分别验证；清理失败使用独立的 `BookingCleanupError`。
- `reason` 与测试场景一致：日期测试说明日期先后校验缺失，价格测试说明 `totalprice >= 0` 校验缺失。

## 环境问题与结论

- 测试解释器：`D:\qa-automation-learning\.venv\Scripts\python.exe`。
- 默认服务地址：`http://127.0.0.1:3001`；网络故障验证使用的临时地址 `http://127.0.0.1:3999` 已清除。
- 结论：已知失败与意外异常已经分离，Day 60 完成标准满足。
