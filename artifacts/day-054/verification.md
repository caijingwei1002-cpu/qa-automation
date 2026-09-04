# Day 54 验证证据

日期：2026-09-04
阶段：Restful Booker API
项目：test-projects/03-restful-booker-api
主题：业务断言

## 目标测试

命令：

```text
.\.venv\Scripts\python.exe -m pytest test-projects/03-restful-booker-api/tests/test_business_rules.py -q
```

结果：

```text
exit_code=0 (passed)
..x.x                                                                    [100%]
3 passed, 2 xfailed in 0.17s
```

## 全量回归

命令：

```text
.\.venv\Scripts\python.exe -m pytest test-projects/03-restful-booker-api/tests -q
```

结果：

```text
exit_code=1 (failed)
.........xxxxxx..x.x.....FF...xxxxxxxxxx......                           [100%]
================================== FAILURES ===================================
_______________________ test_filter_bookings[firstname] _______________________

params = {'firstname': 'Jim'}, detail_path = ('firstname',)
expected_value = 'Jim', comparison = 'equals'
booking_client = <src.booking_client.BookingClient object at 0x000002B36506CDD0>

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
booking_client = <src.booking_client.BookingClient object at 0x000002B3650B0590>

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
2 failed, 26 passed, 18 xfailed in 0.71s
```

## 关键验证

- 目标测试退出码：`0`。
- 全量回归退出码：`1`。
- 目标测试共验证五个业务场景：日期先后关系、同日日期边界、反向日期拒绝、零价格允许、负价格拒绝。
- 目标结果为 `3 passed`、`2 xfailed`；两个 `xfail` 均是已经在既有边界测试中确认的接口校验缺陷。
- `strict xfail` 保留了业务预期：如果接口修复，测试会以 XPASS 失败，提醒移除缺陷标记。
- 合法场景在创建后使用动态 `bookingid` 回查 GET，并验证业务字段持久化。
- 非法场景在断言前提取可能返回的 `bookingid`，并在 `finally` 中清理意外创建的资源。
- 全量回归结果为 `26 passed`、`18 xfailed`、`2 failed`；新增业务规则测试没有引入额外失败。

## 环境问题与结论

- 工作目录：`D:\qa-automation-learning`。
- 测试解释器：`D:\qa-automation-learning\.venv\Scripts\python.exe`。
- 两个全量失败仍是既有 `test_filters.py` 依赖 `firstname=Jim`、`lastname=Brown` 预置数据；当前服务返回空列表，属于测试数据前置条件问题，不是 Day 54 代码导致。
- 结论：Day 54 已将结构 Schema 与跨字段/数值业务规则分层验证；当前接口对反向日期和负价格仍缺少拒绝校验，已用严格 xfail 留证。
