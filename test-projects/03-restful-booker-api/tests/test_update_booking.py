"""验证 PUT 整体替换和 PATCH 部分更新行为。"""

from factories import build_booking_payload

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


def create_booking(booking_client, payload):
    # 创建资源的场景数据保留在测试附近，HTTP 细节交给 Client 处理。
    response = booking_client.create_booking(payload)

    assert response.status_code == 200

    data = response.json()
    assert "bookingid" in data
    assert isinstance(data["bookingid"], int)

    return data["bookingid"]


def get_auth_token(
    api_client,
    auth_credentials,
):
    # Token 返回给测试用于鉴权，但绝不打印 Token 内容。
    response = api_client.post(
        "/auth",
        json=auth_credentials,
    )

    assert response.status_code == 200

    data = response.json()
    assert "token" in data
    assert isinstance(data["token"], str)
    assert data["token"].strip()

    # 不打印、不记录真实 Token。
    return data["token"]


def test_update_booking_with_put(
    booking_client,
    api_client,
    auth_credentials,
):
    # 1. 创建 booking，并使用本次响应中的动态 bookingid。
    create_payload = build_booking_payload()
    booking_id = create_booking(
        booking_client,
        create_payload,
    )

    # 2. 获取鉴权 Token。
    token = get_auth_token(
        api_client,
        auth_credentials,
    )

    # 3. PUT 发送完整 booking 数据。
    # PUT 测试整体替换语义，因此发送完整资源表示。
    update_response = booking_client.update_booking(
        booking_id,
        UPDATE_PAYLOAD,
        token,
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

    assert response.status_code == 403


def test_patch_booking_partial_update(
    booking_client,
    api_client,
    auth_credentials,
):
    create_payload = build_booking_payload()
    booking_id = create_booking(booking_client, create_payload)

    token = get_auth_token(
        api_client,
        auth_credentials,
    )

    # PATCH 只发送本次需要修改的字段。
    patch_response = booking_client.partial_update_booking(
        booking_id,
        PATCH_PAYLOAD,
        token,
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
