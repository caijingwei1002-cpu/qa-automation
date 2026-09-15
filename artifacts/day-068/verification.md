# Day 68 验证证据

日期：2026-09-15
阶段：Restful Booker 收尾与测试代码质量
项目：test-projects/03-restful-booker-api
主题：独立测试设计与编码

## 目标测试

命令：

```text
.\.venv\Scripts\python.exe -m pytest test-projects/03-restful-booker-api/tests/test_independent_scenario.py -q
```

结果：

```text
exit_code=0 (passed)
.                                                                        [100%]
1 passed in 0.02s
```

## 全量回归

命令：

```text
.\.venv\Scripts\python.exe -m pytest test-projects/03-restful-booker-api/tests -q
```

结果：

```text
exit_code=0 (passed)
............................xxxxxx..x.x............xxxxxxxxxx........... [ 66%]
.....................................                                    [100%]
91 passed, 18 xfailed in 1.89s
```

## 关键验证

- 服务预检通过：本地 Restful Booker `/ping` 返回 HTTP 201。
- 测试使用 `build_booking_payload()` 生成合法基线，并在 POST 前完全删除 `additionalneeds`；没有改为 `null` 或空字符串。
- POST 返回 HTTP 200 和整数 `bookingid`；响应中的 firstname、lastname、totalprice、depositpaid、bookingdates 与实际提交 payload 一致。
- GET 同一 `bookingid` 返回 HTTP 200；持久化字段与提交 payload 一致，`additionalneeds` 缺失或为空，没有出现未提交的实际需求值。
- finally 清理路径执行成功：本测试登记的 booking 删除后，GET 同一 ID 返回 HTTP 404。
- 学习者先提供的精确 node id 结果为 `1 passed in 0.05s`；最终代码经统一验证器按计划文件命令复跑为 `1 passed in 0.02s`。

## 环境问题与结论

- 工作目录：`D:\qa-automation-learning`。
- 失败需先记录根因、修复或当前阻塞，再完成当天学习。
- 本次运行：8955f33bbe39478d86799cc8b249dd3b，来源 runner，时间 2026-09-15T09:25:51.766980+00:00；target=0，regression=0。
