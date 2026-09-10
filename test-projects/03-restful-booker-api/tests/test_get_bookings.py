"""验证 GET /booking 集合响应契约。"""

from factories import build_booking_payload


def _extract_booking_id(response):
    """尽可能从创建响应中提取 booking ID。"""
    try:
        data = response.json()
    except ValueError:
        return None

    if not isinstance(data, dict):
        return None

    booking_id = data.get("bookingid")
    return booking_id if isinstance(booking_id, int) else None


def _cleanup_booking(booking_client, booking_id, token):
    """删除本测试创建的 booking，并确认资源已经不存在。"""
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
        f"Booking still exists after cleanup: booking_id={booking_id}; "
        f"status={deleted_response.status_code}"
    )


def test_get_bookings(
    booking_client,
    api_client,
    auth_credentials,
):
    # 先获取 token，供 finally 中清理本测试创建的资源。
    auth_response = api_client.post(
        "/auth",
        json=auth_credentials,
    )
    assert auth_response.status_code == 200

    auth_data = auth_response.json()
    token = auth_data.get("token")
    assert isinstance(token, str)
    assert token.strip()

    # 两次独立调用工厂，确保两个资源拥有独立且唯一的测试数据。
    first_payload = build_booking_payload()
    second_payload = build_booking_payload()

    # 在 try 之前初始化，保证后续失败时 finally 仍可访问两个变量。
    booking_id_1 = None
    booking_id_2 = None

    try:
        first_response = booking_client.create_booking(first_payload)

        # 创建成功后先登记 ID，再执行状态码和类型断言。
        booking_id_1 = _extract_booking_id(first_response)

        assert first_response.status_code == 200
        assert isinstance(booking_id_1, int)

        second_response = booking_client.create_booking(second_payload)

        # 第二个资源也必须在后续断言前立即登记 ID。
        booking_id_2 = _extract_booking_id(second_response)

        assert second_response.status_code == 200
        assert isinstance(booking_id_2, int)

        # 无过滤查询应返回当前已经存在的两个 booking。
        response = booking_client.get_bookings()

        # HTTP 状态码和 JSON 结构属于接口契约的两个独立验证层次。
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

        # 先确认集合响应是 JSON 数组，再检查数组中的每一项。
        data = response.json()

        assert isinstance(data, list), (
            f"Expected response body to be a list, got {type(data).__name__}"
        )

        returned_ids = {
            item["bookingid"] for item in data if isinstance(item, dict) and "bookingid" in item
        }

        assert booking_id_1 in returned_ids
        assert booking_id_2 in returned_ids

        # 遍历所有集合元素，不能只检查第一个元素后就认为集合正确。
        for index, booking in enumerate(data):
            # 每个集合元素都应是对象，并且包含后续详情查询需要的 bookingid。
            assert isinstance(booking, dict), (
                f"Expected item {index} to be an object, got {type(booking).__name__}"
            )

            assert "bookingid" in booking, f"Item {index} is missing 'bookingid': {booking}"

    finally:
        # 分别尝试清理两个资源，避免第一个清理失败阻止第二个资源清理。
        cleanup_errors = []

        for booking_id in (booking_id_1, booking_id_2):
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
