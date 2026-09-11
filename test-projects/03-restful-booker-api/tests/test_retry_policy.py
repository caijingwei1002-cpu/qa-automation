from unittest.mock import Mock

import pytest
import requests
from src.retry_policy import retry_request


def test_get_retries_after_timeout_then_returns_success():
    expected_result = object()
    request_action = Mock(
        side_effect=[
            requests.Timeout("temporary timeout"),
            expected_result,
        ]
    )
    sleep_func = Mock()

    result = retry_request(
        request_action=request_action,
        method="GET",
        max_attempts=3,
        sleep_func=sleep_func,
    )

    assert result is expected_result
    assert request_action.call_count == 2
    assert sleep_func.call_count == 1


def test_get_stops_after_max_attempts_and_reraises_last_exception():
    first_error = requests.Timeout("first timeout")
    second_error = requests.ConnectionError("temporary connection error")
    last_error = requests.Timeout("last timeout")
    request_action = Mock(
        side_effect=[
            first_error,
            second_error,
            last_error,
        ]
    )
    sleep_func = Mock()

    with pytest.raises(requests.Timeout) as exc_info:
        retry_request(
            request_action=request_action,
            method="GET",
            max_attempts=3,
            sleep_func=sleep_func,
        )

    assert exc_info.value is last_error
    assert request_action.call_count == 3
    assert sleep_func.call_count == 2


def test_post_does_not_retry_after_timeout():
    error = requests.Timeout("post timeout")
    request_action = Mock(side_effect=error)
    sleep_func = Mock()

    with pytest.raises(requests.Timeout) as exc_info:
        retry_request(
            request_action=request_action,
            method="POST",
            max_attempts=3,
            sleep_func=sleep_func,
        )

    assert exc_info.value is error
    assert request_action.call_count == 1
    assert sleep_func.call_count == 0


def test_post_does_not_retry_after_connection_error():
    error = requests.ConnectionError("post connection error")
    request_action = Mock(side_effect=error)
    sleep_func = Mock()

    with pytest.raises(requests.ConnectionError) as exc_info:
        retry_request(
            request_action=request_action,
            method="POST",
            max_attempts=3,
            sleep_func=sleep_func,
        )

    assert exc_info.value is error
    assert request_action.call_count == 1
    assert sleep_func.call_count == 0


@pytest.mark.parametrize("invalid_max_attempts", [0, -1])
def test_rejects_non_positive_max_attempts(invalid_max_attempts):
    request_action = Mock()
    sleep_func = Mock()

    with pytest.raises(ValueError, match="max_attempts must be at least 1"):
        retry_request(
            request_action=request_action,
            method="GET",
            max_attempts=invalid_max_attempts,
            sleep_func=sleep_func,
        )

    assert request_action.call_count == 0
    assert sleep_func.call_count == 0
