import os

import pytest


@pytest.fixture
def booking_url():
    base_url = os.getenv(
        "RESTFUL_BOOKER_URL",
        "http://127.0.0.1:3001",
    ).rstrip("/")
    return f"{base_url}/booking"


@pytest.fixture
def request_timeout_seconds():
    return 3.0