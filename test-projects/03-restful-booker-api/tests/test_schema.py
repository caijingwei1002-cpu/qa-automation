import pytest

from factories import build_booking_payload
from schema_helpers import assert_schema_valid


def valid_create_response():
    return {
        "bookingid": 1,
        "booking": build_booking_payload(),
    }


def test_schema_accepts_valid_create_response():
    assert_schema_valid(
        valid_create_response(),
        context="valid create response",
        schema_key="createBookingResponse",
    )


@pytest.mark.parametrize(
    "mutation",
    [
        pytest.param(
            "remove-lastname",
            id="missing-lastname",
        ),
        pytest.param(
            "change-totalprice-to-string",
            id="totalprice-string",
        ),
    ],
)
def test_schema_rejects_invalid_create_response(mutation):
    response_body = valid_create_response()

    if mutation == "remove-lastname":
        del response_body["booking"]["lastname"]
    elif mutation == "change-totalprice-to-string":
        response_body["booking"]["totalprice"] = "200"

    with pytest.raises(AssertionError):
        assert_schema_valid(
            response_body,
            context=f"mutated response: {mutation}",
            schema_key="createBookingResponse",
        )
