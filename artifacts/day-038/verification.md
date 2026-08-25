# Day 38 验证证据：创建预订

## 目标测试

验证命令：

```powershell
python -m pytest test-projects\03-restful-booker-api\tests\test_create_booking.py -q
```

实际结果：

```text
1 passed in 0.12s
```

测试发送的 JSON payload 包含：

- `firstname` / `lastname`；
- `totalprice` / `depositpaid`；
- `bookingdates.checkin` / `bookingdates.checkout`；
- `additionalneeds`。

最终断言验证：

- HTTP 状态码为 `200`；
- 响应包含整数 `bookingid`；
- 响应包含 `booking` 对象；
- `booking` 中每个请求字段与 payload 一致。

## API 项目回归

验证命令：

```powershell
python -m pytest test-projects\03-restful-booker-api\tests -q
```

实际结果：

```text
3 passed in 0.10s
```

## 范围与未覆盖风险

本日证明了创建接口返回了符合当前请求的资源表示，但尚未证明：

- 该 `bookingid` 可以通过后续 GET 查询；
- 缺少字段或错误类型时的负向行为；
- 重复创建场景的数据隔离；
- 测试创建数据是否被清理。

每次运行都会创建一条 booking。后续动态 ID 关联和清理测试应记录创建 ID，并避免依赖固定数据或测试执行顺序。
