import pytest
import requests


FILTER_CASES = [
    pytest.param(
        {"firstname": "Jim"},
        ("firstname",),
        "Jim",
        "equals",
        id="firstname",
    ),
    pytest.param(
        {"lastname": "Brown"},
        ("lastname",),
        "Brown",
        "equals",
        id="lastname",
    ),
    pytest.param(
        {"checkin": "2015-01-01"},
        ("bookingdates", "checkin"),
        "2015-01-01",
        "after",
        id="checkin-after",
    ),
]


def read_nested_value(data, path):
    for key in path:
        data = data[key]
    return data


@pytest.mark.parametrize(
    ("params", "detail_path", "expected_value", "comparison"),
    FILTER_CASES,
)
def test_filter_bookings(
    params,
    detail_path,
    expected_value,
    comparison,
    booking_url,
    request_timeout_seconds,
):
    response = requests.get(
        booking_url,
        params=params,
        timeout=request_timeout_seconds,
    )

    assert response.status_code == 200, (
        f"Expected status code 200, got {response.status_code}; "
        f"request_url={response.request.url}"
    )

    data = response.json()

    assert isinstance(data, list), (
        f"Expected response body to be a list, got {type(data).__name__}; "
        f"request_url={response.request.url}"
    )

    assert data, (
        f"Expected at least one booking for params={params!r}; "
        f"request_url={response.request.url}"
    )

    for index, booking_summary in enumerate(data):
        assert isinstance(booking_summary, dict), (
            f"Expected item {index} to be an object, "
            f"got {type(booking_summary).__name__}; "
            f"request_url={response.request.url}"
        )

        assert "bookingid" in booking_summary, (
            f"Item {index} is missing 'bookingid': {booking_summary}; "
            f"request_url={response.request.url}"
        )

        booking_id = booking_summary["bookingid"]

        detail_response = requests.get(
            f"{booking_url}/{booking_id}",
            timeout=request_timeout_seconds,
        )

        assert detail_response.status_code == 200

        booking_detail = detail_response.json()
        assert isinstance(booking_detail, dict), (
            f"Expected booking detail to be an object, "
            f"got {type(booking_detail).__name__}; "
            f"bookingid={booking_id}"
        )

        actual_value = read_nested_value(booking_detail, detail_path)
        if comparison == "equals":
            matches = actual_value == expected_value
        elif comparison == "after":
            matches = actual_value > expected_value
        else:
            raise AssertionError(f"Unsupported comparison: {comparison!r}")

        assert matches, (
            f"Filter mismatch for bookingid={booking_id}: "
            f"expected {comparison} path {detail_path!r} "
            f"against {expected_value!r}, "
            f"got {actual_value!r}; "
            f"filter_url={response.request.url}"
        )
