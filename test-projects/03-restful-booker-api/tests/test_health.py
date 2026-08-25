import time

import requests
import os

BASE_URL = os.getenv(
    "RESTFUL_BOOKER_URL",
    "http://127.0.0.1:3001",
).rstrip("/")

HEALTH_URL = f"{BASE_URL}/ping"


EXPECTED_STATUS_CODE = 201
EXPECTED_RESPONSE_BODY = "Created"

REQUEST_TIMEOUT_SECONDS = 3.0
MAX_RESPONSE_TIME_SECONDS = 1.0


def test_health_check():
    start_time = time.perf_counter()

    response = requests.get(
        HEALTH_URL,
        timeout=REQUEST_TIMEOUT_SECONDS,
    )

    elapsed_time = time.perf_counter() - start_time

    assert response.status_code == EXPECTED_STATUS_CODE
    assert response.text.strip() == EXPECTED_RESPONSE_BODY
    assert elapsed_time <= MAX_RESPONSE_TIME_SECONDS
