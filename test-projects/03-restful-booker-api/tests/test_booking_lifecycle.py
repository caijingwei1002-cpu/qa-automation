"""验证 booking 从创建到删除的完整资源生命周期。"""

from datetime import date, timedelta

import pytest
from factories import build_booking_payload
from schema_helpers import assert_schema_valid


def _get_token(api_client, auth_credentials):
    """获取更新和删除资源所需的 Token，不打印凭据或 Token。"""
    response = api_client.post(
        "/auth",
        json=auth_credentials,
    )

    assert response.status_code == 200

    data = response.json()
    token = data.get("token")
    assert isinstance(token, str)
    assert token.strip()

    return token


def _json_object(response):
    """尽量读取 JSON 对象，便于断言失败前提取资源 ID。"""
    try:
        data = response.json()
    except ValueError:
        return {}

    return data if isinstance(data, dict) else {}


def _cleanup_booking(booking_client, booking_id, token):
    """只清理本测试创建的资源，并兼容已删除的情况。"""
    if not isinstance(booking_id, int):
        return

    current_response = booking_client.get_booking(booking_id)

    if current_response.status_code == 404:
        return

    assert current_response.status_code == 200, (
        f"Unexpected cleanup lookup status: {current_response.status_code}; booking_id={booking_id}"
    )

    assert isinstance(token, str) and token.strip(), (
        f"A valid cleanup token is required for booking_id={booking_id}"
    )

    cleanup_response = booking_client.delete_booking(
        booking_id,
        token,
    )

    # 此处已经确认资源仍存在，因此清理 DELETE 必须真正返回 201。
    assert cleanup_response.status_code == 201, (
        f"Unexpected cleanup delete status: "
        f"{cleanup_response.status_code}; booking_id={booking_id}; "
        f"response={cleanup_response.text!r}"
    )

    cleanup_get_response = booking_client.get_booking(booking_id)
    assert cleanup_get_response.status_code == 404, (
        f"Booking still exists after cleanup: "
        f"booking_id={booking_id}; "
        f"status={cleanup_get_response.status_code}"
    )


def test_booking_full_lifecycle(
    booking_client,
    api_client,
    auth_credentials,
):
    """验证同一动态 booking 的创建、查询、更新和删除链路。"""
    # 使用工厂生成唯一 firstname 和动态日期，避免依赖固定环境数据。
    create_payload = build_booking_payload(
        lastname="Create",
        totalprice=111,
        depositpaid=True,
        additionalneeds="Breakfast",
    )

    update_checkin = date.today() + timedelta(days=28)
    update_payload = {
        **create_payload,
        "lastname": "Updated",
        "totalprice": 222,
        "depositpaid": False,
        "bookingdates": {
            "checkin": update_checkin.isoformat(),
            "checkout": (update_checkin + timedelta(days=7)).isoformat(),
        },
        "additionalneeds": "Late checkout",
    }

    # 先获取 Token，确保 POST 成功后从生命周期第一步就具备清理能力。
    token = _get_token(api_client, auth_credentials)
    booking_id = None

    try:
        # 1. POST 创建
        create_response = booking_client.create_booking(create_payload)
        create_data = _json_object(create_response)

        # 在其他断言之前提取 ID，避免响应字段不一致时丢失清理线索。
        booking_id = create_data.get("bookingid")

        assert create_response.status_code == 200, (
            f"Expected POST /booking status 200, "
            f"got {create_response.status_code}; "
            f"response={create_response.text!r}"
        )
        assert isinstance(booking_id, int)
        assert create_data.get("booking") == create_payload
        assert_schema_valid(
            create_data,
            context="POST /booking lifecycle response",
            schema_key="createBookingResponse",
        )

        # 2. GET 查询创建结果
        get_response = booking_client.get_booking(booking_id)

        assert get_response.status_code == 200
        get_data = get_response.json()
        assert_schema_valid(
            get_data,
            context="GET /booking/{bookingid} lifecycle response",
            schema_key="getBookingResponse",
        )
        assert get_data == create_payload

        # 3. PUT 完整更新
        update_response = booking_client.update_booking(
            booking_id,
            update_payload,
            token,
        )

        assert update_response.status_code == 200
        assert update_response.json() == update_payload

        # 4. GET 回查更新结果，证明更新已经持久化。
        updated_get_response = booking_client.get_booking(booking_id)

        assert updated_get_response.status_code == 200
        updated_get_data = updated_get_response.json()
        assert_schema_valid(
            updated_get_data,
            context="GET /booking/{bookingid} after PUT response",
            schema_key="getBookingResponse",
        )
        assert updated_get_data == update_payload

        # 5. DELETE 删除
        delete_response = booking_client.delete_booking(
            booking_id,
            token,
        )

        assert delete_response.status_code == 201

        # 6. GET 验证资源已经不存在
        deleted_get_response = booking_client.get_booking(booking_id)
        assert deleted_get_response.status_code == 404
    finally:
        # 正常流程已删除时查询得到 404；中途失败时仍会删除残留资源。
        _cleanup_booking(booking_client, booking_id, token)


def test_booking_cleanup_after_update_assertion_failure(
    booking_client,
    api_client,
    auth_credentials,
):
    """更新阶段断言失败后，仍应清理创建的 booking。"""

    create_payload = build_booking_payload(
        lastname="Create",
        totalprice=111,
        depositpaid=True,
        additionalneeds="Breakfast",
    )

    update_payload = {
        **create_payload,
        "lastname": "Updated",
        "totalprice": 222,
    }

    wrong_expected_payload = {
        **update_payload,
        "lastname": "__wrong_expected_name__",
    }

    token = _get_token(api_client, auth_credentials)
    booking_id = None

    try:
        create_response = booking_client.create_booking(create_payload)
        create_data = _json_object(create_response)

        # 这里必须放在其他创建断言之前
        booking_id = create_data.get("bookingid")

        assert create_response.status_code == 200
        assert isinstance(booking_id, int)
        assert create_data.get("booking") == create_payload

        update_response = booking_client.update_booking(
            booking_id,
            update_payload,
            token,
        )

        assert update_response.status_code == 200

        with pytest.raises(AssertionError):
            assert update_response.json() == wrong_expected_payload
    finally:
        _cleanup_booking(booking_client, booking_id, token)

    deleted_response = booking_client.get_booking(booking_id)

    assert deleted_response.status_code == 404
