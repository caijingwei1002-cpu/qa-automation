# Day 37 验证证据：查询列表

## 目标测试

验证命令：

```powershell
python -m pytest test-projects\03-restful-booker-api\tests\test_get_bookings.py -q
```

实际结果：

```text
1 passed in 0.13s
```

目标测试验证：

- `GET /booking` 返回状态码 `200`；
- 响应可以解析为 JSON；
- 顶层响应是列表；
- 每个元素是对象；
- 每个元素包含 `bookingid`。

## API 项目回归

验证命令：

```powershell
python -m pytest test-projects\03-restful-booker-api\tests -q
```

实际结果：

```text
2 passed in 0.11s
```

## 代码审查记录

初版代码审查发现两个脚本问题：

1. 使用固定 `localhost` 地址，绕过了仓库约定的 `RESTFUL_BOOKER_URL`；
2. 使用了未定义的 `REQUEST_TIMEOUT_SECONDS`。

修正后，测试使用环境变量加本地默认地址，并定义 `3.0s` 请求超时。错误消息保留元素索引、实际类型和实际对象，便于定位集合中的坏元素。

## 失败分类边界

如果未来出现 `200` 但顶层不是列表，或某元素缺少 `bookingid`，首先记录为“响应结构不符合接口契约”。只有在确认契约和测试预期无误后，才能进一步判断是产品返回错误、脚本预期错误，还是环境/响应被篡改；不能仅凭 `AssertionError` 自动归因。
