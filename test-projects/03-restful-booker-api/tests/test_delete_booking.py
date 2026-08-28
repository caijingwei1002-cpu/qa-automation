"""验证删除、删除后资源不存在以及重复删除行为。"""


def test_delete_booking(
    created_booking,
    booking_client,
):
    # Fixture 已完成创建并提供本次测试专属的动态 ID 和 Token。
    booking_id = created_booking["booking_id"]
    token = created_booking["token"]

    # 测试主动删除资源，Fixture teardown 随后会识别 404，避免重复删除。
    delete_response = booking_client.delete_booking(booking_id, token)

    # DELETE 201 是本地 API 的即时成功契约。
    assert delete_response.status_code == 201

    # 4. 使用同一个动态 bookingid 再次查询，
    #    证明资源确实已经不可读取。
    get_response = booking_client.get_booking(booking_id)

    # 后续 GET 证明资源确实不存在，而不只是 DELETE 返回了 201。
    assert get_response.status_code == 404


def test_delete_booking_twice_returns_405(
    created_booking,
    booking_client,
):
    # 可选挑战：重复删除同一资源。
    booking_id = created_booking["booking_id"]
    token = created_booking["token"]

    first_delete_response = booking_client.delete_booking(booking_id, token)

    assert first_delete_response.status_code == 201

    second_delete_response = booking_client.delete_booking(booking_id, token)

    # 第二次 DELETE 验证本地接口对已删除资源的处理契约。
    assert second_delete_response.status_code == 405
