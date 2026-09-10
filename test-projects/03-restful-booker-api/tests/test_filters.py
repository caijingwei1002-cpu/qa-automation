"""验证 booking 列表过滤参数与详情字段之间的关联。"""

from copy import deepcopy
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


def _build_filter_payloads(case):
    base_payload = build_booking_payload()
    matching_payload = deepcopy(base_payload)
    noise_payload = deepcopy(base_payload)
    unique_suffix = uuid4().hex[:8]

    if case["query_param"] == "firstname":
        matching_payload["firstname"] = f"FilterMatch{unique_suffix}"
        noise_payload["firstname"] = f"FilterNoise{unique_suffix}"

    elif case["query_param"] == "lastname":
        matching_payload["lastname"] = f"FilterMatch{unique_suffix}"
        noise_payload["lastname"] = f"FilterNoise{unique_suffix}"

    elif case["query_param"] == "checkin":
        boundary = date.today() + timedelta(days=1)

        matching_payload["bookingdates"] = {
            **base_payload["bookingdates"],
            "checkin": (boundary + timedelta(days=6)).isoformat(),
        }

        noise_payload["bookingdates"] = {
            **base_payload["bookingdates"],
            "checkin": boundary.isoformat(),
        }

    return matching_payload, noise_payload


def _extract_booking_id(response):
    try:
        data = response.json()
    except ValueError:
        return None

    if not isinstance(data, dict):
        return None

    booking_id = data.get("bookingid")
    return booking_id if isinstance(booking_id, int) else None


def _cleanup_booking(booking_client, booking_id, token):
    """清理本测试登记的 booking，兼容资源已被删除的情况。"""
    if booking_id is None:
        return

    current_response = booking_client.get_booking(booking_id)

    if current_response.status_code == 404:
        return

    assert current_response.status_code == 200, (
        f"Unexpected cleanup status: {current_response.status_code}; booking_id={booking_id}"
    )

    delete_response = booking_client.delete_booking(
        booking_id,
        token,
    )

    assert delete_response.status_code == 201, (
        f"Unexpected delete status: {delete_response.status_code}; booking_id={booking_id}"
    )

    deleted_response = booking_client.get_booking(booking_id)
    assert deleted_response.status_code == 404, (
        f"Booking still exists after cleanup: "
        f"booking_id={booking_id}; status={deleted_response.status_code}"
    )


def _get_filter_value(payload, case):
    if case["comparison"] == "after":
        # 工厂生成的 checkin 是今天之后 7 天，使用更早的动态边界。
        return (date.today() + timedelta(days=1)).isoformat()

    return read_nested_value(payload, case["payload_path"])


@pytest.fixture
def filter_booking(booking_client, api_client, auth_credentials, request):
    case = request.param
    matching_payload, noise_payload = _build_filter_payloads(case)
    filter_value = None
    matching_booking_id = None
    noise_booking_id = None

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
        matching_response = booking_client.create_booking(matching_payload)

        # 先保存匹配资源 ID，再做状态断言。
        matching_booking_id = _extract_booking_id(matching_response)

        assert matching_response.status_code == 200
        assert isinstance(matching_booking_id, int)

        noise_response = booking_client.create_booking(noise_payload)

        # 先保存干扰资源 ID，再做状态断言。
        noise_booking_id = _extract_booking_id(noise_response)

        assert noise_response.status_code == 200
        assert isinstance(noise_booking_id, int)

        filter_value = _get_filter_value(matching_payload, case)

        yield {
            "matching_booking_id": matching_booking_id,
            "noise_booking_id": noise_booking_id,
            "token": token,
            "params": {case["query_param"]: filter_value},
            "detail_path": case["payload_path"],
            "expected_value": filter_value,
            "comparison": case["comparison"],
        }
    finally:
        cleanup_errors = []

        for booking_id in (matching_booking_id, noise_booking_id):
            try:
                _cleanup_booking(
                    booking_client,
                    booking_id,
                    token,
                )
            except AssertionError as exc:
                cleanup_errors.append(exc)

        if cleanup_errors:
            raise cleanup_errors[0]


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

    matching_booking_id = filter_booking["matching_booking_id"]
    noise_booking_id = filter_booking["noise_booking_id"]

    # 自己创建的匹配 booking 必须出现，避免依赖环境中的预置数据。
    returned_ids = {item.get("bookingid") for item in data if isinstance(item, dict)}
    assert matching_booking_id in returned_ids, (
        f"Matching booking was not returned for params={params!r}; "
        f"booking_id={matching_booking_id}; "
        f"request_url={response.request.url}"
    )

    # 干扰 booking 不应出现在当前过滤结果中。
    assert noise_booking_id not in returned_ids, (
        f"Noise booking should not be returned for params={params!r}; "
        f"booking_id={noise_booking_id}; "
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
