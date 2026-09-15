"""验证省略可选 additionalneeds 的 booking 创建和持久化行为。"""

import sys

import requests
from factories import build_booking_payload


def _json_object(response):
    """安全读取 JSON 对象，避免解析失败遮蔽后续清理线索。"""
    try:
        data = response.json()
    except ValueError:
        return None

    return data if isinstance(data, dict) else None


def _assert_submitted_fields(booking, payload):
    """只核对客户端实际提交的字段。"""
    for field in (
        "firstname",
        "lastname",
        "totalprice",
        "depositpaid",
        "bookingdates",
    ):
        assert booking.get(field) == payload[field]


def _assert_no_invented_additionalneeds(booking):
    """省略字段可以缺失或为空，但不能凭空出现实际需求值。"""
    if "additionalneeds" in booking:
        assert booking["additionalneeds"] in (None, "")


def _cleanup_booking(booking_client, booking_id, token):
    """尽力删除本测试资源，并把清理失败作为主异常的附加诊断。"""
    if not isinstance(booking_id, int):
        return

    # finally 调用本函数时，sys.exc_info() 保留主测试异常；无主异常时为 None。
    primary_error = sys.exc_info()[1]

    try:
        current_response = booking_client.get_booking(booking_id)

        if current_response.status_code == 404:
            return

        if current_response.status_code != 200:
            raise AssertionError(
                "Booking cleanup lookup failed: "
                f"booking_id={booking_id}, "
                f"get_status={current_response.status_code}, "
                f"response={current_response.text!r}"
            )

        delete_response = booking_client.delete_booking(booking_id, token)

        if delete_response.status_code not in (201, 404):
            raise AssertionError(
                "Booking cleanup delete failed: "
                f"booking_id={booking_id}, "
                f"delete_status={delete_response.status_code}, "
                f"response={delete_response.text!r}"
            )

        if delete_response.status_code == 201:
            deleted_response = booking_client.get_booking(booking_id)

            if deleted_response.status_code != 404:
                raise AssertionError(
                    "Booking cleanup verification failed: "
                    f"booking_id={booking_id}, "
                    f"get_status={deleted_response.status_code}, "
                    f"response={deleted_response.text!r}"
                )
    except (AssertionError, requests.exceptions.RequestException) as cleanup_error:
        if primary_error is None:
            raise

        primary_error.add_note(
            "Cleanup also failed while preserving the primary test failure: "
            f"{cleanup_error.__class__.__name__}: {cleanup_error}"
        )


def test_create_booking_without_optional_additionalneeds(
    booking_client,
    auth_token,
):
    """省略可选字段时创建成功，且读取结果不产生未提交的需求值。"""
    payload = build_booking_payload()
    payload.pop("additionalneeds")
    booking_id = None

    try:
        post_response = booking_client.create_booking(payload)
        post_data = _json_object(post_response)

        # 先登记 ID，再执行可能失败的业务断言。
        if isinstance(post_data, dict):
            candidate_id = post_data.get("bookingid")
            if isinstance(candidate_id, int):
                booking_id = candidate_id

        assert post_response.status_code == 200
        assert isinstance(post_data, dict)
        assert isinstance(booking_id, int)

        created_booking = post_data.get("booking")
        assert isinstance(created_booking, dict)
        _assert_submitted_fields(created_booking, payload)
        _assert_no_invented_additionalneeds(created_booking)

        get_response = booking_client.get_booking(booking_id)
        assert get_response.status_code == 200

        persisted_booking = _json_object(get_response)
        assert isinstance(persisted_booking, dict)
        _assert_submitted_fields(persisted_booking, payload)
        _assert_no_invented_additionalneeds(persisted_booking)
    finally:
        _cleanup_booking(booking_client, booking_id, auth_token)
