# DEFECT-001：POST /booking 缺失必填字段 `firstname` 时返回 HTTP 500

## 前置条件

- RESTful Booker API 服务可访问。
- `POST /booking` 接口可正常接收合法 booking 请求。
- 使用一份已验证能够成功创建 booking 的合法请求数据作为基线。
- 请求方法、接口地址、请求头以及除 `firstname` 之外的所有字段均保持合法。
- 本次复现唯一改变：从合法请求体中完全删除 `firstname` 字段。
- 不将 `firstname` 设置为空字符串或 `null`，也不同时修改其他字段。

## 复现步骤

1. 准备一份完整且合法的 booking 请求体，确保以下字段及其值均符合接口要求：
   - `firstname`
   - `lastname`
   - `totalprice`
   - `depositpaid`
   - `bookingdates.checkin`
   - `bookingdates.checkout`
   - `additionalneeds`
2. 以该合法请求体为基线，仅删除 `firstname` 字段。
3. 保持请求方法、URL、请求头以及其余字段不变。
4. 向 `POST /booking` 发送该请求。
5. 记录接口返回的 HTTP 状态码及响应体。

## Expected Result

依据 API 契约/接口需求中对必填字段和非法请求的约定：

- `firstname` 为必填字段。
- 当请求缺少必填字段 `firstname` 时，服务端应识别为客户端请求参数不合法并拒绝创建 booking。
- 如果当前项目契约约定参数校验失败返回 `400 Bad Request`，则接口应返回：

`HTTP 400 Bad Request`

- 不应创建任何 booking 资源。
- 如接口契约定义了错误响应结构，则响应体还应符合对应错误格式。

## Actual Result

- `POST /booking` 返回：

`HTTP 500 Internal Server Error`

- 当前结果显示：当请求缺失 firstname 字段时，接口实际返回 HTTP 500，响应体为 Internal Server Error。

## 验证证据

命令：

```powershell
.\.venv\Scripts\python.exe -m pytest -vv -s --runxfail test-projects/03-restful-booker-api/tests/test_invalid_payloads.py::test_create_booking_rejects_missing_required_field[missing-firstname]
```

结果：
- `expected_status=400`
- 实际响应：HTTP 500
- 响应体：`Internal Server Error`
- pytest：`1 failed`

## 影响

- 客户端提交缺少必填字段的非法请求时，无法获得明确、可预期的参数校验结果。
- HTTP 500 会将可预期的输入错误表现为服务端内部故障，降低接口错误语义的准确性。
- 调用方可能无法区分“请求参数不合法”与“服务端真实内部异常”，增加错误处理和问题定位成本。
- 如果同类必填字段缺失场景采用相同处理逻辑，问题可能不只影响 `firstname`，但这一点目前尚未验证。
- 若服务端在异常路径中仍可能创建资源，可能导致无效或不完整的 booking 数据被写入；目前尚未确认是否发生。

## 未知项

以下内容当前尚未验证或确认，不应作为已知事实写入结论：

- API 契约是否明确规定缺少必填字段时必须返回 `400 Bad Request`，还是规定其他 4xx 状态码（例如 422）。
- 当前 HTTP 500 的完整响应体、错误结构及服务端错误信息。
- 缺少 `firstname` 时，服务端是否实际上创建了 booking 资源。
- 如果意外创建了 booking，其返回响应中是否包含可用于清理的 `bookingid`。
- 其他必填字段缺失时是否也会出现相同的 HTTP 500。
- 不同非法形式，例如 `firstname=""`、`firstname=null`、错误数据类型，是否存在相同问题。
- 当前问题是否只发生在特定环境、版本或数据条件下。
- 缺陷的最终 Severity / Priority 尚未评估。
