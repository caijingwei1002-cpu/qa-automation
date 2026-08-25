import os
import requests


BASE_URL = os.getenv(
    "RESTFUL_BOOKER_URL",
    "http://127.0.0.1:3001",
).rstrip("/")

BOOKINGS_URL = f"{BASE_URL}/booking"
REQUEST_TIMEOUT_SECONDS = 3.0

def test_get_bookings():
    response = requests.get(
        BOOKINGS_URL,
        timeout=REQUEST_TIMEOUT_SECONDS,
    )

    assert response.status_code == 200, (
        f"Expected status code 200, got {response.status_code}"
    )

    data = response.json()

    assert isinstance(data, list), (
        f"Expected response body to be a list, "
        f"got {type(data).__name__}"
    )

    for index, booking in enumerate(data):
        assert isinstance(booking, dict), (
            f"Expected item {index} to be an object, "
            f"got {type(booking).__name__}"
        )

        assert "bookingid" in booking, (
            f"Item {index} is missing 'bookingid': {booking}"
        )
