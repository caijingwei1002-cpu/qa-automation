"""验证 booking 缺失必填字段时的负向响应和异常资源清理。"""

from copy import deepcopy

import pytest

from factories import build_booking_payload


# 业务预期是缺失必填字段返回 400，而不是让服务抛出 500。
# 当前本地接口对这些场景均返回 500，因此先用严格 xfail 留存缺陷证据。
MISSING_REQUIRED_FIELD_CASES = [
    pytest.param(
        "firstname",
        400,
        marks=pytest.mark.xfail(
            strict=True,
            reason="当前接口缺少 firstname 时返回 500，应返回 400。",
        ),
        id="missing-firstname",
    ),
    pytest.param(
        "lastname",
        400,
        marks=pytest.mark.xfail(
            strict=True,
            reason="当前接口缺少 lastname 时返回 500，应返回 400。",
        ),
        id="missing-lastname",
    ),
    pytest.param(
        "totalprice",
        400,
        marks=pytest.mark.xfail(
            strict=True,
            reason="当前接口缺少 totalprice 时返回 500，应返回 400。",
        ),
        id="missing-totalprice",
    ),
    pytest.param(
        "depositpaid",
        400,
        marks=pytest.mark.xfail(
            strict=True,
            reason="当前接口缺少 depositpaid 时返回 500，应返回 400。",
        ),
        id="missing-depositpaid",
    ),
    pytest.param(
        "bookingdates",
        400,
        marks=pytest.mark.xfail(
            strict=True,
            reason="当前接口缺少 bookingdates 时返回 500，应返回 400。",
        ),
        id="missing-bookingdates",
    ),
    pytest.param(
        "bookingdates.checkin",
        400,
        marks=pytest.mark.xfail(
            strict=True,
            reason="当前接口缺少 checkin 时返回 500，应返回 400。",
        ),
        id="missing-bookingdates-checkin",
    ),
    pytest.param(
        "bookingdates.checkout",
        400,
        marks=pytest.mark.xfail(
            strict=True,
            reason="当前接口缺少 checkout 时返回 500，应返回 400。",
        ),
        id="missing-bookingdates-checkout",
    ),
]


def _get_token(api_client, auth_credentials):
    """获取清理意外资源所需的 Token，不打印 Token 内容。"""
    response = api_client.post("/auth", json=auth_credentials)

    assert response.status_code == 200

    data = response.json()
    token = data.get("token")
    assert isinstance(token, str)
    assert token.strip()

    return token


def _remove_field(payload, field_path):
    """按点号路径从独立 payload 中删除一个字段。"""
    target = payload
    path_parts = field_path.split(".")

    for key in path_parts[:-1]:
        target = target[key]

    del target[path_parts[-1]]


def _extract_booking_id(response):
    """尽量从成功响应提取 ID，供断言失败后的清理使用。"""
    try:
        data = response.json()
    except ValueError:
        return None

    if not isinstance(data, dict):
        return None

    booking_id = data.get("bookingid")
    return booking_id if isinstance(booking_id, int) else None


def _cleanup_booking(booking_client, booking_id, token):
    """清理接口错误接受缺失字段请求时创建的 booking。"""
    if booking_id is None:
        return

    current_response = booking_client.get_booking(booking_id)

    if current_response.status_code == 404:
        return

    assert current_response.status_code == 200

    delete_response = booking_client.delete_booking(booking_id, token)
    assert delete_response.status_code in (201, 404)


@pytest.mark.parametrize(
    ("missing_field", "expected_status"),
    MISSING_REQUIRED_FIELD_CASES,
)
def test_create_booking_rejects_missing_required_field(
    booking_client,
    api_client,
    auth_credentials,
    missing_field,
    expected_status,
):
    """逐个删除必填字段，验证错误请求被安全拒绝。"""
    token = _get_token(api_client, auth_credentials)
    payload = deepcopy(build_booking_payload())
    _remove_field(payload, missing_field)
    booking_id = None

    try:
        response = booking_client.create_booking(payload)
        booking_id = _extract_booking_id(response)
        response_body = " ".join(response.text.split())[:200]

        # 业务预期不能因当前接口返回 500 而改成 500。
        assert response.status_code == expected_status, (
            f"缺失字段 {missing_field!r}："
            f"expected_status={expected_status}, "
            f"actual_status={response.status_code}, "
            f"response={response_body!r}"
        )

        # 拒绝请求时不应返回可用资源 ID。
        assert booking_id is None
    finally:
        # 即使接口错误地返回 200，断言失败前提取的 ID 也必须被清理。
        _cleanup_booking(booking_client, booking_id, token)
