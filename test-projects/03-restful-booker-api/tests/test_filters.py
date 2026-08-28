"""验证 booking 列表过滤参数与详情字段之间的关联。"""

import pytest


# 每组数据覆盖一个查询参数及其预期的比较语义。
FILTER_CASES = [
    pytest.param(
        {"firstname": "Jim"},
        ("firstname",),
        "Jim",
        "equals",
        id="firstname",
    ),
    pytest.param(
        {"lastname": "Brown"},
        ("lastname",),
        "Brown",
        "equals",
        id="lastname",
    ),
    pytest.param(
        {"checkin": "2015-01-01"},
        ("bookingdates", "checkin"),
        "2015-01-01",
        "after",
        id="checkin-after",
    ),
]


def read_nested_value(data, path):
    # 读取 bookingdates.checkin 这类嵌套响应字段，供过滤断言使用。
    for key in path:
        data = data[key]
    return data


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
    # 先验证过滤后的集合，再查询每个返回 ID 的详情确认过滤准确性。
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

    # 过滤结果不能为空，否则后面的详情校验没有实际对象可验证。
    assert data, (
        f"Expected at least one booking for params={params!r}; "
        f"request_url={response.request.url}"
    )

    for index, booking_summary in enumerate(data):
        assert isinstance(booking_summary, dict), (
            f"Expected item {index} to be an object, "
            f"got {type(booking_summary).__name__}; "
            f"request_url={response.request.url}"
        )

        assert "bookingid" in booking_summary, (
            f"Item {index} is missing 'bookingid': {booking_summary}; "
            f"request_url={response.request.url}"
        )

        booking_id = booking_summary["bookingid"]

        # 列表接口只返回 ID 摘要，必须回查详情才能验证实际过滤字段。
        detail_response = booking_client.get_booking(booking_id)

        assert detail_response.status_code == 200

        booking_detail = detail_response.json()
        assert isinstance(booking_detail, dict), (
            f"Expected booking detail to be an object, "
            f"got {type(booking_detail).__name__}; "
            f"bookingid={booking_id}"
        )

        # 过滤断言针对详情资源，而不是只检查摘要列表中的 ID。
        actual_value = read_nested_value(booking_detail, detail_path)
        if comparison == "equals":
            matches = actual_value == expected_value
        elif comparison == "after":
            matches = actual_value > expected_value
        else:
            raise AssertionError(f"Unsupported comparison: {comparison!r}")

        assert matches, (
            f"Filter mismatch for bookingid={booking_id}: "
            f"expected {comparison} path {detail_path!r} "
            f"against {expected_value!r}, "
            f"got {actual_value!r}; "
            f"filter_url={response.request.url}"
        )
