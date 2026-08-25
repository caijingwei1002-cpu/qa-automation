import os

import requests


BASE_URL = os.getenv(
    "RESTFUL_BOOKER_URL",
    "http://127.0.0.1:3001",
).rstrip("/")
REQUEST_TIMEOUT_SECONDS = 3.0
BOOKING_URL = f"{BASE_URL}/booking"


def test_create_booking_can_be_retrieved():
    payload = {
        "firstname": "Jim",
        "lastname": "Brown",
        "totalprice": 111,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2026-08-25",
            "checkout": "2026-08-30",
        },
        "additionalneeds": "Breakfast",
    }

    # 1. POST 创建 booking
    create_response = requests.post(
        BOOKING_URL,
        json=payload,
        timeout=REQUEST_TIMEOUT_SECONDS,
    )

    assert create_response.status_code == 200

    create_data = create_response.json()

    # 2. 读取本次 POST 返回的动态 bookingid
    assert "bookingid" in create_data
    booking_id = create_data["bookingid"]

    assert isinstance(booking_id, int)

    # 3. GET 查询刚创建的 booking
    get_response = requests.get(
        f"{BOOKING_URL}/{booking_id}",
        timeout=REQUEST_TIMEOUT_SECONDS,
    )

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