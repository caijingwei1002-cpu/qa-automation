"""验证新创建的 booking 可以通过响应中的 ID 再次查询。"""

from factories import build_booking_payload


def test_create_booking_can_be_retrieved(booking_client):
    payload = build_booking_payload()

    # 1. POST 创建 booking
    create_response = booking_client.create_booking(payload)

    # POST 状态码证明创建请求被接受，返回的 ID 用于关联下一次查询。
    assert create_response.status_code == 200

    create_data = create_response.json()

    # 2. 读取本次 POST 返回的动态 bookingid
    assert "bookingid" in create_data
    booking_id = create_data["bookingid"]

    assert isinstance(booking_id, int)

    # 3. GET 查询刚创建的 booking
    get_response = booking_client.get_booking(booking_id)

    # GET 状态码和字段比较共同证明创建结果可读且数据一致。
    assert get_response.status_code == 200

    booking = get_response.json()

    # 4. 比较查询结果与原始 payload
    assert isinstance(booking, dict)
    assert booking["firstname"] == payload["firstname"]
    assert booking["lastname"] == payload["lastname"]
    assert booking["totalprice"] == payload["totalprice"]
    assert booking["depositpaid"] == payload["depositpaid"]


    assert (
        booking["bookingdates"]["checkin"]
        == payload["bookingdates"]["checkin"]
    )
    assert (
        booking["bookingdates"]["checkout"]
        == payload["bookingdates"]["checkout"]
    )

    assert booking["additionalneeds"] == payload["additionalneeds"]
