"""验证 PUT 整体替换和 PATCH 部分更新行为。"""

from assertions import assert_error_response

UPDATE_PAYLOAD = {
    "firstname": "James",
    "lastname": "Green",
    "totalprice": 222,
    "depositpaid": False,
    "bookingdates": {
        "checkin": "2026-09-01",
        "checkout": "2026-09-05",
    },
    "additionalneeds": "Late checkout",
}

PATCH_PAYLOAD = {
    "totalprice": 300,
    "additionalneeds": "Dinner",
}


def test_update_booking_with_put(
    created_booking,
    booking_client,
    auth_token,
):
    booking_id = created_booking["booking_id"]

    update_response = booking_client.update_booking(
        booking_id,
        UPDATE_PAYLOAD,
        auth_token,
    )

    # 4. HTTP 成功后继续验证 PUT 响应体。
    assert update_response.status_code == 200

    updated_booking = update_response.json()
    assert updated_booking == UPDATE_PAYLOAD

    # 5. 再次 GET 同一个动态 bookingid，验证持久化结果。
    get_response = booking_client.get_booking(booking_id)

    assert get_response.status_code == 200

    persisted_booking = get_response.json()
    assert persisted_booking == UPDATE_PAYLOAD


def test_update_booking_without_token_returns_403(
    created_booking,
    booking_client,
):
    # Day 42 可选挑战：无 Token 时不能执行完整更新。
    booking_id = created_booking["booking_id"]

    response = booking_client.update_booking(
        booking_id,
        UPDATE_PAYLOAD,
        token=None,
    )

    assert_error_response(
        response,
        expected_status=403,
        expected_text="Forbidden",
    )


def test_patch_booking_partial_update(
    created_booking,
    booking_client,
    auth_token,
):
    booking_id = created_booking["booking_id"]
    create_payload = created_booking["payload"]

    patch_response = booking_client.partial_update_booking(
        booking_id,
        PATCH_PAYLOAD,
        auth_token,
    )

    assert patch_response.status_code == 200

    expected_booking = {
        # 合并只用于构造预期结果，实际 PATCH 请求仍然保持部分 payload。
        **create_payload,
        **PATCH_PAYLOAD,
    }

    patched_booking = patch_response.json()
    assert patched_booking == expected_booking

    get_response = booking_client.get_booking(booking_id)

    assert get_response.status_code == 200
    assert get_response.json() == expected_booking
