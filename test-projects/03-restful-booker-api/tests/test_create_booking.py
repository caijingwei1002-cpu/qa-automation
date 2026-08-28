"""验证 POST /booking 创建响应契约。"""

from factories import build_booking_payload


def test_create_booking(booking_client):
    # 工厂提供合法基线；本场景只需要验证默认 booking 创建契约。
    payload = build_booking_payload()

    # Client 负责发送 JSON，并应用统一的 URL 和 timeout 配置。
    response = booking_client.create_booking(payload)

    # HTTP 成功状态是必要条件，但还必须继续验证响应结构。
    assert response.status_code == 200

    data = response.json()

    assert "bookingid" in data
    assert isinstance(data["bookingid"], int)

    assert "booking" in data
    assert isinstance(data["booking"], dict)
    created_booking = data["booking"]

    # 逐字段比较请求数据和响应数据，证明创建资源与请求一致。
    for field, expected in payload.items():
        assert created_booking.get(field) == expected, (
            f"Field {field!r} mismatch: "
            f"expected {expected!r}, got {created_booking.get(field)!r}"
        )
