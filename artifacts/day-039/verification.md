# Day 39 验证证据：创建后查询

## 目标测试

验证命令：

```powershell
python -m pytest test-projects\03-restful-booker-api\tests\test_booking_flow.py -q
```

实际结果：

```text
1 passed in 0.16s
```

目标测试验证：

- POST `/booking` 返回状态码 `200`；
- 从本次 POST 响应读取整数 `bookingid`；
- 使用该动态 ID GET `/booking/{bookingid}`；
- GET 返回状态码 `200` 且响应为对象；
- 查询到的姓名、价格、押金状态、日期和附加需求与原始 payload 一致。

## 失败与修复记录

首次代码审查发现 `test_booking_flow.py` 使用了 `BOOKING_URL`，但未定义该变量。若直接运行，会在发出 POST 前触发 `NameError`，属于脚本缺陷/测试配置问题，不是 Restful Booker 产品缺陷。

修正为使用既有 `BASE_URL` 构造：

```python
BOOKING_URL = f"{BASE_URL}/booking"
```

修正后目标测试通过。没有发生实际接口断言失败；因此本次证据是“代码审查发现脚本风险 → 修正 → 复验通过”。

## 归因边界

如果未来出现 GET `200` 但字段与 payload 不一致，应先保留实际 `bookingid`、POST payload、GET 响应和 URL，依次排除取错 ID、URL 拼接、字段比较和环境数据污染。排除这些脚本与环境因素后，才有证据进一步怀疑产品的持久化或查询一致性。

## 当前风险

每次运行都会创建新的 booking，测试还没有删除或隔离测试数据。单次回查通过不能证明并发、重试或长期一致性；后续应考虑清理策略或专用测试环境。
