"""验证 booking 数据工厂的唯一性、覆盖能力和数据隔离。"""

from factories import build_booking_payload


def test_booking_payload_is_unique_and_independent():
    first_payload = build_booking_payload()
    second_payload = build_booking_payload()

    # 唯一字段用于隔离不同测试数据。
    assert first_payload["firstname"] != second_payload["firstname"]

    # 修改一次调用返回的嵌套对象，不应污染另一次调用。
    first_payload["bookingdates"]["checkin"] = "changed"
    assert second_payload["bookingdates"]["checkin"] != "changed"


def test_booking_payload_supports_overrides_and_keeps_defaults():
    payload = build_booking_payload(
        totalprice=999,
        bookingdates={"checkin": "2026-09-01"},
    )

    # 指定字段被覆盖，未指定的默认字段仍然保留。
    assert payload["totalprice"] == 999
    assert payload["bookingdates"]["checkin"] == "2026-09-01"
    assert payload["bookingdates"]["checkout"]
    assert payload["lastname"] == "User"
    assert payload["depositpaid"] is True
