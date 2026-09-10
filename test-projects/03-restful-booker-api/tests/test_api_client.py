from unittest.mock import Mock, patch

import pytest
import requests
from src.api_client import ApiRequestError, RestfulBookerClient


@patch("src.api_client.requests.request")
def test_request_passes_timeout_and_builds_url(mock_request):
    fake_response = Mock()
    mock_request.return_value = fake_response

    client = RestfulBookerClient(
        base_url="http://example.test/api/",
        timeout=6.25,
    )

    result = client.get(
        "/booking",
        params={"firstname": "Alice"},
    )

    assert result is fake_response

    mock_request.assert_called_once_with(
        method="GET",
        url="http://example.test/api/booking",
        params={"firstname": "Alice"},
        json=None,
        headers={"Accept": "application/json"},
        timeout=6.25,
    )


@pytest.mark.parametrize(
    "error",
    [
        requests.Timeout("request timed out"),
        requests.ConnectionError("connection refused"),
    ],
)
def test_request_wraps_network_error(error):
    client = RestfulBookerClient(
        base_url="http://example.test",
        timeout=6.25,
    )

    with patch(
        "src.api_client.requests.request",
        side_effect=error,
    ):
        with pytest.raises(ApiRequestError) as exc_info:
            client.get(
                "/booking",
                token="secret-token",
            )

    message = str(exc_info.value)

    assert "method=GET" in message
    assert "url=http://example.test/booking" in message
    assert "timeout=6.25s" in message
    assert error.__class__.__name__ in message
    assert "secret-token" not in message
    assert exc_info.value.__cause__ is error


@patch("src.api_client.requests.request")
def test_request_headers_do_not_leak_between_requests(mock_request):
    mock_request.side_effect = [Mock(), Mock()]

    client = RestfulBookerClient(
        base_url="http://example.test",
        timeout=3.0,
    )

    client.get(
        "/first",
        headers={"X-Trace": "first"},
        token="token-123",
    )
    client.get("/second")

    first_headers = mock_request.call_args_list[0].kwargs["headers"]
    second_headers = mock_request.call_args_list[1].kwargs["headers"]

    assert first_headers == {
        "Accept": "application/json",
        "X-Trace": "first",
        "Cookie": "token=token-123",
    }
    assert second_headers == {
        "Accept": "application/json",
    }
    assert client.default_headers == {
        "Accept": "application/json",
    }


@patch("src.api_client.requests.request")
def test_request_does_not_mutate_caller_headers(mock_request):
    mock_request.return_value = Mock()

    custom_headers = {
        "X-Trace": "first",
    }

    client = RestfulBookerClient(
        base_url="http://example.test",
        timeout=3.0,
    )

    client.get(
        "/booking",
        headers=custom_headers,
        token="token-123",
    )

    assert custom_headers == {
        "X-Trace": "first",
    }

    sent_headers = mock_request.call_args.kwargs["headers"]

    assert sent_headers == {
        "Accept": "application/json",
        "X-Trace": "first",
        "Cookie": "token=token-123",
    }
