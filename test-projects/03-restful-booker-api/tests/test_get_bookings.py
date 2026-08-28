"""验证 GET /booking 集合响应契约。"""


def test_get_bookings(booking_client):
    # 目标 URL 和传输配置由 Client 统一管理。
    response = booking_client.get_bookings()

    # HTTP 状态码和 JSON 结构属于接口契约的两个独立验证层次。
    assert response.status_code == 200, (
        f"Expected status code 200, got {response.status_code}"
    )

    # 先确认集合响应是 JSON 数组，再检查数组中的每一项。
    data = response.json()

    assert isinstance(data, list), (
        f"Expected response body to be a list, "
        f"got {type(data).__name__}"
    )

    # 遍历所有集合元素，不能只检查第一个元素后就认为集合正确。
    for index, booking in enumerate(data):
        # 每个集合元素都应是对象，并且包含后续详情查询需要的 bookingid。
        assert isinstance(booking, dict), (
            f"Expected item {index} to be an object, "
            f"got {type(booking).__name__}"
        )

        assert "bookingid" in booking, (
            f"Item {index} is missing 'bookingid': {booking}"
        )
