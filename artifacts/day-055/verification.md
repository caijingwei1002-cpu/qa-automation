# Day 55 验证证据

日期：2026-09-04
阶段：Restful Booker API
项目：test-projects/03-restful-booker-api
主题：接口链路

## 目标测试

命令：

```text
.\.venv\Scripts\python.exe -m pytest test-projects/03-restful-booker-api/tests/test_booking_lifecycle.py -q
```

结果：

```text
exit_code=0 (passed)
.                                                                        [100%]
1 passed in 0.16s
```

## 全量回归

命令：

```text
.\.venv\Scripts\python.exe -m pytest test-projects/03-restful-booker-api/tests -q
```

结果：

```text
exit_code=1 (failed)
..........xxxxxx..x.x.....FF...xxxxxxxxxx......                          [100%]
================================== FAILURES ===================================
_______________________ test_filter_bookings[firstname] _______________________

params = {'firstname': 'Jim'}, detail_path = ('firstname',)
expected_value = 'Jim', comparison = 'equals'
booking_client = <src.booking_client.BookingClient object at 0x000001A369EB0790>

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
booking_client = <src.booking_client.BookingClient object at 0x000001A369EBF550>

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
2 failed, 27 passed, 18 xfailed in 1.14s
```

## 关键验证

- 目标测试退出码：`0`。
- 全量回归退出码：`1`。
- 目标测试验证一条完整生命周期：POST 创建、GET 查询、Token 鉴权、PUT 更新、GET 回查、DELETE 删除和删除后 GET 404。
- 测试使用数据工厂生成唯一 firstname 和动态日期，并始终使用 POST 返回的动态 bookingid。
- 创建响应和两次详情响应均通过既有 JSON Schema 验证，随后再做字段一致性和持久化断言。
- 在创建响应的其他断言前提取 bookingid；中途任何断言失败都进入 finally 清理路径。
- 清理先查询资源状态：若仍为 200，则 DELETE 必须返回 201，并再次 GET 确认 404；若已为 404，则视为清理完成。
- 目标结果为 `1 passed`；全量回归结果为 `27 passed`、`18 xfailed`、`2 failed`，新增生命周期测试没有引入额外失败。

## 环境问题与结论

- 工作目录：`D:\qa-automation-learning`。
- 测试解释器：`D:\qa-automation-learning\.venv\Scripts\python.exe`。
- 两个全量失败仍是既有 `test_filters.py` 依赖 `firstname=Jim`、`lastname=Brown` 固定预置数据；当前服务返回空列表，属于测试数据前置条件问题，不是生命周期测试导致。
- 结论：完整资源链路已用局部断言和动态 ID 串联，清理逻辑能覆盖正常删除和中途失败两条路径。
