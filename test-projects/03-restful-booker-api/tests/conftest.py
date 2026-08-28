import os
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
# 项目目录包含 src/，但当前没有安装为 Python 包。
# 只在这里加入一次路径，保证所有测试能够统一导入共享 Client。
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.api_client import RestfulBookerClient
from src.booking_client import BookingClient
from factories import build_booking_payload


@pytest.fixture
def api_base_url():
    # 支持本地、测试和明确授权环境之间切换目标地址。
    return os.getenv(
        "RESTFUL_BOOKER_URL",
        "http://127.0.0.1:3001",
    ).rstrip("/")


@pytest.fixture
def request_timeout_seconds():
    # 这是传输层超时；业务性能阈值应由具体测试定义。
    return float(os.getenv("RESTFUL_BOOKER_TIMEOUT_SECONDS", "3"))


@pytest.fixture
def auth_credentials():
    # 有环境变量时使用外部凭据；测试中不得打印凭据。
    return {
        "username": os.getenv("RESTFUL_BOOKER_USERNAME", "admin"),
        "password": os.getenv("RESTFUL_BOOKER_PASSWORD", "password123"),
    }


@pytest.fixture
def api_client(api_base_url, request_timeout_seconds):
    # 测试接收统一配置好的 Client，不再自行重复组装 HTTP 细节。
    return RestfulBookerClient(
        base_url=api_base_url,
        timeout=request_timeout_seconds,
    )


@pytest.fixture
def booking_client(api_client):
    return BookingClient(api_client)


@pytest.fixture
def created_booking(booking_client, api_client, auth_credentials):
    # 先获取 Token，避免创建成功后鉴权失败导致资源无法清理。
    auth_response = api_client.post(
        "/auth",
        json=auth_credentials,
    )
    assert auth_response.status_code == 200

    auth_data = auth_response.json()
    assert isinstance(auth_data.get("token"), str)
    assert auth_data["token"].strip()
    token = auth_data["token"]

    payload = build_booking_payload(
        lastname="Booking",
        totalprice=999,
        additionalneeds="Fixture data",
    )

    create_response = booking_client.create_booking(payload)
    assert create_response.status_code == 200

    create_data = create_response.json()
    assert isinstance(create_data.get("bookingid"), int)
    booking_id = create_data["bookingid"]

    try:
        yield {
            "booking_id": booking_id,
            "token": token,
            "payload": payload,
        }
    finally:
        current_response = booking_client.get_booking(booking_id)

        if current_response.status_code == 200:
            delete_response = booking_client.delete_booking(
                booking_id,
                token,
            )
            assert delete_response.status_code in (201, 404)
        elif current_response.status_code == 404:
            # 测试本身已经删除，视为清理完成
            pass
        else:
            raise AssertionError(
                f"Unexpected cleanup status: "
                f"{current_response.status_code}"
            )
