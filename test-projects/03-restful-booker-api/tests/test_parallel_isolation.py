import pytest


@pytest.mark.parametrize(
    "case_label",
    ["case_a", "case_b"],
    ids=["case_a", "case_b"],
)
def test_filter_booking_is_isolated_between_parallel_tests(
    case_label,
    booking_client,
    created_booking,
):
    own_booking_id = created_booking["booking_id"]
    own_firstname = created_booking["payload"]["firstname"]

    response = booking_client.get_bookings(
        params={"firstname": own_firstname},
    )

    assert response.status_code == 200, (
        f"{case_label}: expected filter status 200, got {response.status_code}"
    )

    results = response.json()

    assert isinstance(results, list), (
        f"{case_label}: expected filter response to be a list, got {type(results).__name__}"
    )

    returned_ids = set()

    for index, item in enumerate(results):
        assert isinstance(item, dict), (
            f"{case_label}: expected result item {index} to be a dict, got {type(item).__name__}"
        )

        booking_id = item.get("bookingid")

        assert isinstance(booking_id, int), (
            f"{case_label}: expected result item {index} to contain "
            f"integer bookingid, got {booking_id!r}"
        )

        returned_ids.add(booking_id)

    assert own_booking_id in returned_ids, (
        f"{case_label}: expected own booking_id={own_booking_id} "
        f"for firstname={own_firstname!r}, "
        f"returned_ids={sorted(returned_ids)}"
    )

    for booking_id in returned_ids:
        detail_response = booking_client.get_booking(booking_id)

        assert detail_response.status_code == 200, (
            f"{case_label}: expected detail status 200 for "
            f"booking_id={booking_id}, "
            f"got {detail_response.status_code}"
        )

        detail = detail_response.json()

        assert isinstance(detail, dict), (
            f"{case_label}: expected booking detail to be a dict for "
            f"booking_id={booking_id}, "
            f"got {type(detail).__name__}"
        )

        actual_firstname = detail.get("firstname")

        assert actual_firstname == own_firstname, (
            f"{case_label}: filter isolation failed for booking_id={booking_id}; "
            f"expected firstname={own_firstname!r}, "
            f"got {actual_firstname!r}"
        )


@pytest.mark.parametrize(
    "case_label",
    ["case_a", "case_b"],
    ids=["case_a", "case_b"],
)
def test_update_booking_is_isolated_between_parallel_tests(
    case_label,
    booking_client,
    created_booking,
    auth_token,
):
    own_booking_id = created_booking["booking_id"]
    original_payload = created_booking["payload"]

    updated_payload = {
        **original_payload,
        "firstname": f"{case_label}_updated_{own_booking_id}",
    }

    update_response = booking_client.update_booking(
        own_booking_id,
        updated_payload,
        auth_token,
    )

    assert update_response.status_code == 200
    assert update_response.json() == updated_payload

    detail_response = booking_client.get_booking(own_booking_id)

    assert detail_response.status_code == 200

    detail = detail_response.json()

    assert detail["firstname"] == updated_payload["firstname"]
