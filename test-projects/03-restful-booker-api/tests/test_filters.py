"""验证 booking 列表过滤参数与详情字段之间的关联。"""

from datetime import date, timedelta
from uuid import uuid4

import pytest
from factories import build_booking_payload

# 每组场景描述查询参数、详情字段和过滤比较语义。
FILTER_CASES = [
    pytest.param(
        {
            "query_param": "firstname",
            "payload_path": ("firstname",),
            "comparison": "equals",
        },
        id="firstname",
    ),
    pytest.param(
        {
            "query_param": "lastname",
            "payload_path": ("lastname",),
            "comparison": "equals",
        },
        id="lastname",
    ),
    pytest.param(
        {
            "query_param": "checkin",
            "payload_path": ("bookingdates", "checkin"),
            "comparison": "after",
        },
        id="checkin-after",
    ),
]


def read_nested_value(data, path):
    # 读取 bookingdates.checkin 这类嵌套响应字段，供过滤断言使用。
    for key in path:
        data = data[key]
    return data


def _build_filter_payload(case):
    overrides = {}

    if case["query_param"] == "lastname":
        # lastname 默认值不是唯一的，需要显式生成本测试专属值。
        overrides["lastname"] = f"Filter{uuid4().hex[:8]}"

    return build_booking_payload(**overrides)


def _get_filter_value(payload, case):
    if case["comparison"] == "after":
        # 工厂生成的 checkin 是今天之后 7 天，使用更早的动态边界。
        return (date.today() + timedelta(days=1)).isoformat()

    return read_nested_value(payload, case["payload_path"])


@pytest.fixture
def filter_booking(booking_client, api_client, auth_credentials, request):
    case = request.param
    payload = _build_filter_payload(case)
    filter_value = None
    booking_id = None

    auth_response = api_client.post(
        "/auth",
        json=auth_credentials,
    )
    assert auth_response.status_code == 200

    auth_data = auth_response.json()
    token = auth_data.get("token")
    assert isinstance(token, str)
    assert token.strip()

    try:
        create_response = booking_client.create_booking(payload)

        # 先登记响应中的 ID，再做状态和 payload 断言，保证失败时仍有清理线索。
        try:
            create_data = create_response.json()
        except ValueError:
            create_data = {}

        if isinstance(create_data, dict):
            booking_id = create_data.get("bookingid")

        assert create_response.status_code == 200
        assert isinstance(booking_id, int)

        filter_value = _get_filter_value(payload, case)
        yield {
            "booking_id": booking_id,
            "token": token,
            "params": {case["query_param"]: filter_value},
            "detail_path": case["payload_path"],
            "expected_value": filter_value,
            "comparison": case["comparison"],
        }
    finally:
        if booking_id is not None:
            current_response = booking_client.get_booking(booking_id)

            if current_response.status_code == 200:
                delete_response = booking_client.delete_booking(
                    booking_id,
                    token,
                )
                assert delete_response.status_code in (201, 404)
            elif current_response.status_code != 404:
                raise AssertionError(
                    f"Unexpected cleanup status: {current_response.status_code}; "
                    f"booking_id={booking_id}"
                )


@pytest.mark.parametrize("filter_booking", FILTER_CASES, indirect=True)
def test_filter_bookings(filter_booking, booking_client):
    params = filter_booking["params"]
    detail_path = filter_booking["detail_path"]
    expected_value = filter_booking["expected_value"]
    comparison = filter_booking["comparison"]

    # 先验证过滤后的集合，再查询每个返回 ID 的详情确认过滤准确性。
    response = booking_client.get_bookings(params=params)

    assert response.status_code == 200, (
        f"Expected status code 200, got {response.status_code}; request_url={response.request.url}"
    )

    data = response.json()

    assert isinstance(data, list), (
        f"Expected response body to be a list, got {type(data).__name__}; "
        f"request_url={response.request.url}"
    )

    # 自己创建的 booking 必须出现在结果中，避免依赖环境中的预置数据。
    returned_ids = {item.get("bookingid") for item in data if isinstance(item, dict)}
    assert filter_booking["booking_id"] in returned_ids, (
        f"Created booking was not returned for params={params!r}; "
        f"booking_id={filter_booking['booking_id']}; "
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
