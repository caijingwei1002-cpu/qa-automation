from __future__ import annotations

from collections.abc import Callable
from typing import TypeVar

import requests

T = TypeVar("T")

_RETRYABLE_EXCEPTIONS = (requests.Timeout, requests.ConnectionError)
_RETRY_DELAY_SECONDS = 1.0


def retry_request(
    request_action: Callable[[], T],
    method: str,
    max_attempts: int,
    sleep_func: Callable[[float], None],
) -> T:
    """Execute one request action with the Day 63 retry policy."""
    if max_attempts < 1:
        raise ValueError("max_attempts must be at least 1")

    normalized_method = method.upper()
    allowed_attempts = max_attempts if normalized_method == "GET" else 1

    for attempt in range(1, allowed_attempts + 1):
        try:
            return request_action()
        except _RETRYABLE_EXCEPTIONS:
            if attempt == allowed_attempts:
                raise
            sleep_func(_RETRY_DELAY_SECONDS)

    raise RuntimeError("retry policy reached an unreachable state")
