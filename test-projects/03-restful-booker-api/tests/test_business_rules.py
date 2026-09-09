"""验证 booking 的跨字段关系和业务数值边界。"""

from datetime import date, timedelta

import pytest
from assertions import assert_error_response
from factories import build_booking_payload

# 沿用项目已有的边界约定：checkout 不得早于 checkin，totalprice=0 表示免费订单并且合法。
# 当前服务对两个非法边界仍会返回 200，因此用 strict xfail 保留已确认的缺陷证据。


def _get_token(api_client, auth_credentials):
    """获取清理测试资源所需的 Token，不打印凭据或 Token。"""
    response = api_client.post("/auth", json=auth_credentials)

    assert response.status_code == 200

    data = response.json()
    token = data.get("token")
    assert isinstance(token, str)
    assert token.strip()

    return token


def _extract_booking_id(response):
    """尽量从响应中提取 bookingid，保证断言失败后仍可清理。"""
    try:
        data = response.json()
    except ValueError:
        return None

    if not isinstance(data, dict):
        return None

    booking_id = data.get("bookingid")
    return booking_id if isinstance(booking_id, int) else None


def _cleanup_booking(booking_client, booking_id, token):
    """删除本测试创建的 booking，避免业务边界用例污染环境。"""
    if booking_id is None:
        return

    current_response = booking_client.get_booking(booking_id)

    if current_response.status_code == 404:
        return

    assert current_response.status_code == 200

    delete_response = booking_client.delete_booking(booking_id, token)
    assert delete_response.status_code in (201, 404)


def _assert_created_booking(
    booking_client,
    response,
    payload,
    booking_id,
):
    """验证合法业务边界被创建并能通过 GET 回查。"""
    assert response.status_code == 200, (
        f"Expected HTTP 200, but got HTTP {response.status_code}. Response body: {response.text!r}"
    )

    body = response.json()

    assert isinstance(body.get("bookingid"), int)
    assert body["bookingid"] == booking_id
    assert body.get("booking") == payload

    get_response = booking_client.get_booking(booking_id)

    assert get_response.status_code == 200
    assert get_response.json() == payload


def _date_payload(checkin, checkout):
    return build_booking_payload(
        bookingdates={
            "checkin": checkin.isoformat(),
            "checkout": checkout.isoformat(),
        }
    )


def test_checkout_after_checkin_is_accepted_and_persisted(
    booking_client,
    api_client,
    auth_credentials,
):
    """checkout 晚于 checkin 时应创建成功，并保持日期关系。"""
    checkin = date.today() + timedelta(days=7)
    checkout = checkin + timedelta(days=3)
    payload = _date_payload(checkin, checkout)
    token = _get_token(api_client, auth_credentials)
    booking_id = None

    try:
        response = booking_client.create_booking(payload)

        booking_id = _extract_booking_id(response)

        _assert_created_booking(
            booking_client,
            response,
            payload,
            booking_id,
        )

        dates = response.json()["booking"]["bookingdates"]
        assert dates["checkin"] < dates["checkout"]
    finally:
        _cleanup_booking(booking_client, booking_id, token)


def test_same_day_checkout_is_allowed(
    booking_client,
    api_client,
    auth_credentials,
):
    """按照当前项目契约，同日入住和退房属于允许的边界。"""
    checkin = date.today() + timedelta(days=7)
    payload = _date_payload(checkin, checkin)
    token = _get_token(api_client, auth_credentials)
    booking_id = None

    try:
        response = booking_client.create_booking(payload)

        booking_id = _extract_booking_id(response)

        _assert_created_booking(
            booking_client,
            response,
            payload,
            booking_id,
        )

        dates = response.json()["booking"]["bookingdates"]
        assert dates["checkin"] == dates["checkout"]
    finally:
        _cleanup_booking(booking_client, booking_id, token)


@pytest.mark.xfail(
    strict=True,
    reason="已确认当前接口接受 checkout 早于 checkin，缺少日期顺序校验。",
)
def test_checkout_before_checkin_is_rejected(
    booking_client,
    api_client,
    auth_credentials,
):
    """checkout 早于 checkin 时应按业务规则拒绝请求。"""
    checkin = date.today() + timedelta(days=7)
    checkout = checkin - timedelta(days=1)
    payload = _date_payload(checkin, checkout)
    token = _get_token(api_client, auth_credentials)
    booking_id = None

    try:
        response = booking_client.create_booking(payload)

        booking_id = _extract_booking_id(response)

        assert_error_response(response, expected_status=400)
        assert booking_id is None
    finally:
        _cleanup_booking(booking_client, booking_id, token)


def test_zero_totalprice_is_allowed(
    booking_client,
    api_client,
    auth_credentials,
):
    """免费订单的 totalprice=0 应被接受并持久化。"""
    payload = build_booking_payload(totalprice=0)
    token = _get_token(api_client, auth_credentials)
    booking_id = None

    try:
        response = booking_client.create_booking(payload)

        booking_id = _extract_booking_id(response)

        _assert_created_booking(
            booking_client,
            response,
            payload,
            booking_id,
        )

        assert response.json()["booking"]["totalprice"] == 0
    finally:
        _cleanup_booking(booking_client, booking_id, token)


@pytest.mark.xfail(
    strict=True,
    reason="已确认当前接口接受负数 totalprice，缺少 totalprice >= 0 校验。",
)
def test_negative_totalprice_is_rejected(
    booking_client,
    api_client,
    auth_credentials,
):
    """负数价格不应被接受。"""
    payload = build_booking_payload(totalprice=-1)
    token = _get_token(api_client, auth_credentials)
    booking_id = None

    try:
        response = booking_client.create_booking(payload)

        booking_id = _extract_booking_id(response)

        assert_error_response(response, expected_status=400)
        assert booking_id is None
    finally:
        _cleanup_booking(booking_client, booking_id, token)


def test_created_booking_is_cleaned_up_when_business_assertion_fails(
    booking_client,
    api_client,
    auth_credentials,
):
    """业务断言失败后，finally 仍应删除已经创建的 booking。"""
    payload = build_booking_payload()
    token = _get_token(api_client, auth_credentials)
    booking_id = None

    try:
        response = booking_client.create_booking(payload)

        booking_id = _extract_booking_id(response)

        wrong_expected_payload = {
            **payload,
            "firstname": "__controlled_wrong_firstname__",
        }

        with pytest.raises(AssertionError):
            _assert_created_booking(
                booking_client,
                response,
                wrong_expected_payload,
                booking_id,
            )
    finally:
        _cleanup_booking(booking_client, booking_id, token)

    assert booking_id is not None

    get_response = booking_client.get_booking(booking_id)

    assert get_response.status_code == 404, (
        f"Expected booking {booking_id} to be deleted after "
        f"the controlled assertion failure, "
        f"but got HTTP {get_response.status_code}. "
        f"Response body: {get_response.text!r}"
    )
