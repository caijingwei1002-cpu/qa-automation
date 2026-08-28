"""验证 booking 字段类型错误时的拒绝行为和异常资源清理。"""

import pytest

from factories import build_booking_payload


INVALID_TYPE_CASES = [
    pytest.param(
        ("totalprice",),
        "200",
        400,
        marks=pytest.mark.xfail(
            strict=True,
            raises=AssertionError,
            reason=(
                "当前接口接受字符串 totalprice，返回 200，"
                "并将其转换为数字；契约预期为 400。"
            ),
        ),
        id="totalprice-as-string",
    ),
    pytest.param(
        ("depositpaid",),
        "true",
        400,
        marks=pytest.mark.xfail(
            strict=True,
            raises=AssertionError,
            reason=(
                "当前接口接受字符串 depositpaid，返回 200，"
                "并将其转换为布尔值；契约预期为 400。"
            ),
        ),
        id="depositpaid-as-string",
    ),
    pytest.param(
        ("bookingdates", "checkin"),
        12345,
        400,
        marks=pytest.mark.xfail(
            strict=True,
            raises=AssertionError,
            reason=(
                "当前接口接受数字 bookingdates.checkin，返回 200，"
                "并将其转换为日期字符串；契约预期为 400。"
            ),
        ),
        id="checkin-as-number",
    ),
]


def _set_field(payload, field_path, invalid_value):
    """按照字段路径，将目标字段替换为错误类型值。"""
    if not field_path:
        raise ValueError("field_path must not be empty")

    target = payload

    for field_name in field_path[:-1]:
        target = target[field_name]

    target[field_path[-1]] = invalid_value


def _extract_booking_id(response):
    """安全提取创建接口可能返回的 bookingid。"""
    try:
        body = response.json()
    except ValueError:
        return None

    if not isinstance(body, dict):
        return None

    booking_id = body.get("bookingid")
    return booking_id if isinstance(booking_id, int) else None


def _response_summary(response, limit=300):
    """生成适合失败消息使用的简短响应摘要。"""
    text = response.text.replace("\n", " ").strip()

    if len(text) > limit:
        return f"{text[:limit]}..."

    return text


@pytest.mark.parametrize(
    ("field_path", "invalid_value", "expected_status"),
    INVALID_TYPE_CASES,
)
def test_create_booking_rejects_invalid_field_type(
    booking_client,
    api_client,
    auth_credentials,
    field_path,
    invalid_value,
    expected_status,
):
    payload = build_booking_payload()

    # 每次只修改一个字段，保持其他字段为合法基线。
    _set_field(payload, field_path, invalid_value)

    response = None
    booking_id = None
    cleanup_error = None

    try:
        response = booking_client.create_booking(payload)
        booking_id = _extract_booking_id(response)

    finally:
        # 即使负向请求被接口错误接受，也要清理意外创建的资源。
        if booking_id is not None:
            try:
                auth_response = api_client.post(
                    "/auth",
                    json=auth_credentials,
                )

                auth_body = auth_response.json()
                token = auth_body.get("token")

                if token is None:
                    raise RuntimeError(
                        f"Cleanup authentication failed: "
                        f"status={auth_response.status_code}, "
                        f"response={_response_summary(auth_response)}"
                    )

                delete_response = booking_client.delete_booking(
                    booking_id,
                    token,
                )

                if delete_response.status_code != 201:
                    raise RuntimeError(
                        f"Cleanup failed for booking_id={booking_id}: "
                        f"status={delete_response.status_code}, "
                        f"response={_response_summary(delete_response)}"
                    )

            except Exception as exc:
                cleanup_error = exc

    field_name = ".".join(field_path)
    response_summary = _response_summary(response)

    # RuntimeError 不属于 xfail 接受的 AssertionError，避免掩盖清理失败。
    if cleanup_error is not None:
        raise RuntimeError(
            f"Unexpected booking cleanup failed: "
            f"field={field_name}, "
            f"invalid_value={invalid_value!r}, "
            f"booking_id={booking_id!r}, "
            f"error={cleanup_error}"
        ) from cleanup_error

    # 已知缺陷是接口返回 200；若行为变成其他错误状态，需要重新调查。
    if response.status_code not in (expected_status, 200):
        raise RuntimeError(
            f"Invalid type behavior changed unexpectedly: "
            f"field={field_name}, "
            f"invalid_value={invalid_value!r}, "
            f"expected_status={expected_status}, "
            f"actual_status={response.status_code}, "
            f"response={response_summary}"
        )

    assert response.status_code == expected_status, (
        f"Invalid field type was not rejected: "
        f"field={field_name}, "
        f"invalid_value={invalid_value!r}, "
        f"expected_status={expected_status}, "
        f"actual_status={response.status_code}, "
        f"response={response_summary}"
    )

    assert booking_id is None, (
        f"Invalid request unexpectedly created a booking: "
        f"field={field_name}, "
        f"invalid_value={invalid_value!r}, "
        f"actual_status={response.status_code}, "
        f"booking_id={booking_id!r}, "
        f"response={response_summary}"
    )
