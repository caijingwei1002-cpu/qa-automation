import os

import requests

BASE_URL = os.getenv(
    "RESTFUL_BOOKER_URL",
    "http://127.0.0.1:3001",
).rstrip("/")

BOOKING_URL = f"{BASE_URL}/booking"
REQUEST_TIMEOUT_SECONDS = 3.0


def test_create_booking():
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

    response = requests.post(
        BOOKING_URL,
        json=payload,
        timeout=REQUEST_TIMEOUT_SECONDS,
    )

    assert response.status_code == 200

    data = response.json()

    assert "bookingid" in data
    assert isinstance(data["bookingid"], int)

    assert "booking" in data
    assert isinstance(data["booking"], dict)
    created_booking = data["booking"]

    for field, expected in payload.items():
        assert created_booking.get(field) == expected, (
            f"Field {field!r} mismatch: "
            f"expected {expected!r}, got {created_booking.get(field)!r}"
        )
