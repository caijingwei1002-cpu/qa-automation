# Day 52 验证证据

日期：2026-09-04
阶段：Restful Booker API
项目：test-projects/03-restful-booker-api
主题：状态码与错误模型

## 目标测试

命令：

```text
.\.venv\Scripts\python.exe -m pytest test-projects/03-restful-booker-api/tests/test_update_booking.py::test_update_booking_without_token_returns_403 test-projects/03-restful-booker-api/tests/test_delete_booking.py::test_delete_booking_twice_returns_405 -q
```

结果：

```text
exit_code=0 (passed)
..                                                                       [100%]
2 passed in 0.07s
```

## 全量回归

命令：

```text
.\.venv\Scripts\python.exe -m pytest test-projects/03-restful-booker-api/tests -q
```

结果：

```text
exit_code=1 (failed)
.........xxxxxx.....FF...xxxxxxxxxx...                                   [100%]
================================== FAILURES ===================================
_______________________ test_filter_bookings[firstname] _______________________

params = {'firstname': 'Jim'}, detail_path = ('firstname',)
expected_value = 'Jim', comparison = 'equals'
booking_client = <src.booking_client.BookingClient object at 0x00000293DDD71F90>

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
booking_client = <src.booking_client.BookingClient object at 0x00000293DDDF39D0>

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
2 failed, 20 passed, 16 xfailed in 0.58s
```

## 关键验证

- 目标测试退出码：`0`。
- 全量回归退出码：`1`。
- 两个迁移场景均通过统一 `assert_error_response()`：无 Token 的 PUT 返回 `403 Forbidden`，重复 DELETE 返回 `405 Method Not Allowed`；状态码、非空响应体和错误文本均被断言。
- 全量回归共有 `20 passed`、`16 xfailed` 和 `2 failed`；失败仅为既有 `test_filters.py` 对 `firstname=Jim`、`lastname=Brown` 预置数据的依赖。
- 未使用“不是 200 就算失败”的宽泛断言；helper 精确校验 4xx/5xx 预期、响应体和可选文本，业务场景仍由具体测试提供。

## 环境问题与结论

- 工作目录：`D:\qa-automation-learning`。
- 测试解释器：`D:\qa-automation-learning\.venv\Scripts\python.exe`。
- 两个全量失败的根因是过滤测试依赖服务重启后的预置数据，当前环境中没有 `Jim` 和 `Brown`；这与本日断言辅助函数改动无关，属于测试数据隔离风险。
- 结论：Day 52 目标重构通过；全量回归为“失败但根因明确”，后续应让过滤测试自己创建、查询和清理测试数据。
