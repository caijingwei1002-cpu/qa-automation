"""提供 API 错误响应的统一断言。"""

import re


def _response_summary(response, limit=300):
    text = response.text or ""

    summary = re.sub(r"\s+", " ", text).strip()

    if not summary:
        return "<empty response body>"

    return summary[:limit]


def assert_error_response(
    response,
    expected_status,
    *,
    expected_text=None,
):
    if not 400 <= expected_status <= 599:
        raise ValueError(
            f"expected_status must be between 400 and 599, "
            f"but got {expected_status}"
        )

    summary = _response_summary(response)

    assert response.status_code == expected_status, (
        f"Expected HTTP {expected_status}, "
        f"but got HTTP {response.status_code}. "
        f"Response body: {summary!r}"
    )

    assert response.text.strip(), (
        f"Expected HTTP {expected_status} error response body to be non-empty, "
        f"but got HTTP {response.status_code}. "
        f"Response body: {summary!r}"
    )

    if expected_text is not None:
        assert expected_text in response.text, (
            f"Expected HTTP {expected_status} response body to contain "
            f"{expected_text!r}, "
            f"but got HTTP {response.status_code}. "
            f"Response body: {summary!r}"
        )
