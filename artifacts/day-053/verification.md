# Day 53 验证证据

日期：2026-09-04
阶段：Restful Booker API
项目：test-projects/03-restful-booker-api
主题：JSON Schema

## 目标测试

命令：

```text
.\.venv\Scripts\python.exe -m pytest test-projects/03-restful-booker-api/tests/test_schema.py test-projects/03-restful-booker-api/tests/test_create_booking.py::test_create_booking test-projects/03-restful-booker-api/tests/test_booking_flow.py::test_create_booking_can_be_retrieved -q
```

结果：

```text
exit_code=0 (passed)
.....                                                                    [100%]
5 passed in 0.14s
```

## 全量回归

命令：

```text
.\.venv\Scripts\python.exe -m pytest test-projects/03-restful-booker-api/tests -q
```

结果：

```text
exit_code=1 (failed)
.........xxxxxx.....FF...xxxxxxxxxx......                                [100%]
================================== FAILURES ===================================
_______________________ test_filter_bookings[firstname] _______________________

params = {'firstname': 'Jim'}, detail_path = ('firstname',)
expected_value = 'Jim', comparison = 'equals'
booking_client = <src.booking_client.BookingClient object at 0x000001E0387690D0>

    @pytest.mark.parametrize(
        ("params", "detail_path", "expected_value", "comparison"),
        FILTER_CASES,
    )
    def test_filter_bookings(
        params,
        detail_path,
        expected_value,
        comparison,
        booking_client,
    ):
        # ����֤���˺�ļ��ϣ��ٲ�ѯÿ������ ID ������ȷ�Ϲ���׼ȷ�ԡ�
        response = booking_client.get_bookings(params=params)

        assert response.status_code == 200, (
            f"Expected status code 200, got {response.status_code}; "
            f"request_url={response.request.url}"
        )

        data = response.json()

        assert isinstance(data, list), (
            f"Expected response body to be a list, got {type(data).__name__}; "
            f"request_url={response.request.url}"
        )

        # ���˽������Ϊ�գ�������������У��û��ʵ�ʶ������֤��
>       assert data, (
            f"Expected at least one booking for params={params!r}; "
            f"request_url={response.request.url}"
        )
E       AssertionError: Expected at least one booking for params={'firstname': 'Jim'}; request_url=http://127.0.0.1:3001/booking?firstname=Jim
E       assert []

test-projects\03-restful-booker-api\tests\test_filters.py:66: AssertionError
_______________________ test_filter_bookings[lastname] ________________________

params = {'lastname': 'Brown'}, detail_path = ('lastname',)
expected_value = 'Brown', comparison = 'equals'
booking_client = <src.booking_client.BookingClient object at 0x000001E0384C7D50>

    @pytest.mark.parametrize(
        ("params", "detail_path", "expected_value", "comparison"),
        FILTER_CASES,
    )
    def test_filter_bookings(
        params,
        detail_path,
        expected_value,
        comparison,
        booking_client,
    ):
        # ����֤���˺�ļ��ϣ��ٲ�ѯÿ������ ID ������ȷ�Ϲ���׼ȷ�ԡ�
        response = booking_client.get_bookings(params=params)

        assert response.status_code == 200, (
            f"Expected status code 200, got {response.status_code}; "
            f"request_url={response.request.url}"
        )

        data = response.json()

        assert isinstance(data, list), (
            f"Expected response body to be a list, got {type(data).__name__}; "
            f"request_url={response.request.url}"
        )

        # ���˽������Ϊ�գ�������������У��û��ʵ�ʶ������֤��
>       assert data, (
            f"Expected at least one booking for params={params!r}; "
            f"request_url={response.request.url}"
        )
E       AssertionError: Expected at least one booking for params={'lastname': 'Brown'}; request_url=http://127.0.0.1:3001/booking?lastname=Brown
E       assert []

test-projects\03-restful-booker-api\tests\test_filters.py:66: AssertionError
=========================== short test summary info ===========================
FAILED test-projects/03-restful-booker-api/tests/test_filters.py::test_filter_bookings[firstname]
FAILED test-projects/03-restful-booker-api/tests/test_filters.py::test_filter_bookings[lastname]
2 failed, 23 passed, 16 xfailed in 0.87s
```

## 关键验证

- 目标测试退出码：`0`。
- 全量回归退出码：`1`。
- 目标覆盖 `test_schema.py`、POST 创建响应和 GET 详情响应，共 `5 passed`；Schema 单元测试包含合法基线、缺失 `lastname` 和 `totalprice` 字符串类型变化。
- `booking.json` 使用 `$defs` 复用 booking 结构，分别约束创建响应 envelope 和详情响应；`$ref` 在根 Schema 上下文中解析，`FormatChecker` 实际启用日期格式校验。
- 全量回归共有 `23 passed`、`16 xfailed` 和 `2 failed`；新增 Schema 验证未引入额外失败。

## 环境问题与结论

- 工作目录：`D:\qa-automation-learning`。
- 测试解释器：`D:\qa-automation-learning\.venv\Scripts\python.exe`。
- 两个全量失败仍是既有 `test_filters.py` 依赖 `firstname=Jim`、`lastname=Brown` 预置数据；当前服务重启后没有这些记录，属于测试数据隔离问题，不是 Schema 改动造成的。
- 结论：创建和查询响应结构契约已接入并通过；缺失字段和类型变化能够稳定触发 Schema 失败，跨字段日期顺序继续由业务测试负责。
