from unittest.mock import Mock, patch

import pytest
import requests
from src.api_client import ApiRequestError, RestfulBookerClient


def _build_response(
    status_code: int,
    body: str,
    headers: dict[str, str] | None = None,
) -> requests.Response:
    response = requests.Response()
    response.status_code = status_code
    response._content = body.encode("utf-8")
    response.encoding = "utf-8"
    response.headers.update(headers or {})
    return response


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


@patch("src.api_client.requests.request")
def test_put_returns_403_response_and_explicit_summary(mock_request):
    response = _build_response(
        403,
        '{"error": "Forbidden", "detail": "permission denied"}',
        {"Content-Type": "application/json"},
    )
    mock_request.return_value = response

    client = RestfulBookerClient(
        base_url="http://example.test",
        timeout=6.25,
    )

    result = client.put(
        "/booking/123",
        json={"firstname": "Alice"},
        token="request-token",
    )

    assert result is response

    mock_request.assert_called_once_with(
        method="PUT",
        url="http://example.test/booking/123",
        params=None,
        json={"firstname": "Alice"},
        headers={
            "Accept": "application/json",
            "Cookie": "token=request-token",
        },
        timeout=6.25,
    )

    summary = client._response_summary(result)

    assert "status=403" in summary
    assert "Forbidden" in summary
    assert "permission denied" in summary


@pytest.mark.parametrize(
    ("body", "sensitive_value", "sensitive_fragments"),
    [
        (
            '{"ToKeN": "secret token 123", "detail": "permission denied"}',
            "secret token 123",
            ("token 123",),
        ),
        (
            '{"pAsSwOrD": "my password 123", "detail": "permission denied"}',
            "my password 123",
            ("password 123",),
        ),
        (
            '{"AUTHORIZATION": "Bearer abc def 456", "detail": "permission denied"}',
            "Bearer abc def 456",
            ("abc def 456",),
        ),
        (
            ('{"cOoKiE": "token=abc 123; session=xyz 456", "detail": "permission denied"}'),
            "token=abc 123; session=xyz 456",
            ("abc 123", "xyz 456"),
        ),
    ],
    ids=["token", "password", "authorization", "cookie"],
)
def test_response_summary_redacts_sensitive_fields_but_keeps_diagnostics(
    body,
    sensitive_value,
    sensitive_fragments,
):
    client = RestfulBookerClient(
        base_url="http://example.test",
        timeout=6.25,
    )
    response = _build_response(
        403,
        body,
        {"Content-Type": "application/json"},
    )

    summary = client._response_summary(response)

    # 可诊断性：脱敏后仍保留状态码和非敏感正文。
    assert "status=403" in summary
    assert "permission denied" in summary

    # 旧断言保留：完整敏感值不得出现。
    assert sensitive_value not in summary
    assert "<redacted>" in summary

    # 加强断言：即使只脱掉 Bearer、token= 等前缀，
    # 敏感值主体也不能残留在摘要中。
    for sensitive_fragment in sensitive_fragments:
        assert sensitive_fragment not in summary


def test_request_exception_with_response_uses_safe_response_summary():
    client = RestfulBookerClient(
        base_url="http://example.test",
        timeout=6.25,
    )
    response = _build_response(
        403,
        ('{"AUTHORIZATION": "Bearer abc def 456", "detail": "permission denied"}'),
        {"Content-Type": "application/json"},
    )
    error = requests.RequestException(
        "request failed",
        response=response,
    )

    with patch(
        "src.api_client.requests.request",
        side_effect=error,
    ):
        with pytest.raises(ApiRequestError) as exc_info:
            client.put(
                "/booking/123",
                json={"firstname": "Alice"},
                token="request-token",
            )

    message = str(exc_info.value)

    assert "method=PUT" in message
    assert "url=http://example.test/booking/123" in message
    assert "timeout=6.25s" in message
    assert "error=RequestException" in message
    assert "status=403" in message
    assert "permission denied" in message
    assert "<redacted>" in message
    assert "Bearer abc def 456" not in message
    assert "abc def 456" not in message
    assert exc_info.value.__cause__ is error


@pytest.mark.parametrize(
    ("body_length", "expect_truncated"),
    [
        (200, False),
        (201, True),
    ],
    ids=["200_chars", "201_chars"],
)
def test_response_summary_body_length_boundary(body_length, expect_truncated):
    client = RestfulBookerClient(
        base_url="http://example.test",
        timeout=6.25,
    )
    body = "A" * body_length
    response = _build_response(
        403,
        body,
        {"Content-Type": "text/plain"},
    )

    summary = client._response_summary(response)

    assert "status=403" in summary

    if expect_truncated:
        assert ("A" * 200) + "..." in summary
        assert "A" * 201 not in summary
    else:
        assert "A" * 200 in summary
        assert ("A" * 200) + "..." not in summary


def test_response_summary_truncates_long_body_without_leaking_sensitive_value():
    client = RestfulBookerClient(
        base_url="http://example.test",
        timeout=6.25,
    )
    sensitive_value = "Bearer abc def 456"
    body = (
        '{"AUTHORIZATION": "Bearer abc def 456", '
        '"detail": "permission denied", '
        '"padding": "' + ("A" * 260) + '"}'
    )
    response = _build_response(
        403,
        body,
        {"Content-Type": "application/json"},
    )

    summary = client._response_summary(response)

    assert "status=403" in summary
    assert "permission denied" in summary
    assert sensitive_value not in summary
    assert "abc def 456" not in summary
    assert "..." in summary


def test_response_summary_marks_missing_response():
    client = RestfulBookerClient(
        base_url="http://example.test",
        timeout=6.25,
    )

    summary = client._response_summary(None)

    assert summary == "status=<no response>, response=<no response>"


def test_response_summary_does_not_mutate_original_response():
    client = RestfulBookerClient(
        base_url="http://example.test",
        timeout=6.25,
    )
    response = _build_response(
        403,
        ('{"Authorization": "Bearer original secret value", "detail": "permission denied"}'),
        {
            "Content-Type": "application/json",
            "X-Request-ID": "req-123",
        },
    )

    original_text = response.text
    original_content = response.content
    original_headers = dict(response.headers)

    summary = client._response_summary(response)

    assert "Bearer original secret value" not in summary
    assert "permission denied" in summary

    assert response.text == original_text
    assert response.content == original_content
    assert dict(response.headers) == original_headers


def test_request_error_redacts_sensitive_params_without_mutating_caller_data():
    client = RestfulBookerClient(
        base_url="http://example.test",
        timeout=6.25,
    )

    params = {
        "authorization": "Bearer alpha beta gamma",
        "firstname": "Alice",
    }
    original_params = dict(params)

    error = requests.ConnectionError("connection refused")

    with patch(
        "src.api_client.requests.request",
        side_effect=error,
    ):
        with pytest.raises(ApiRequestError) as exc_info:
            client.get(
                "/booking",
                params=params,
            )

    message = str(exc_info.value)

    assert "method=GET" in message
    assert "url=http://example.test/booking" in message
    assert "timeout=6.25s" in message
    assert "firstname" in message
    assert "Alice" in message

    assert "<redacted>" in message
    assert "Bearer alpha beta gamma" not in message
    assert "alpha beta gamma" not in message

    assert exc_info.value.__cause__ is error
    assert params == original_params
