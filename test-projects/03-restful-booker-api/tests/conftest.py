import os
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
# 项目目录包含 src/，但当前没有安装为 Python 包。
# 只在这里加入一次路径，保证所有测试能够统一导入共享 Client。
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from factories import build_booking_payload  # noqa: E402
from src.api_client import RestfulBookerClient  # noqa: E402
from src.booking_client import BookingClient  # noqa: E402
from src.settings import get_settings  # noqa: E402


@pytest.fixture
def settings():
    # 每次创建 fixture 时读取，支持同一进程中的环境切换并统一校验入口。
    return get_settings()


@pytest.fixture
def api_base_url(settings):
    # fixture 只消费规范化结果，不重复读取或解析环境变量。
    return settings.restful_booker_url


@pytest.fixture
def request_timeout_seconds(settings):
    # fixture 只消费已经解析并校验过的配置，不重复读取环境变量。
    return settings.request_timeout_seconds


@pytest.fixture
def auth_credentials():
    # 有环境变量时使用外部凭据；测试中不得打印凭据。
    return {
        "username": os.getenv("RESTFUL_BOOKER_USERNAME", "admin"),
        "password": os.getenv("RESTFUL_BOOKER_PASSWORD", "password123"),
    }


@pytest.fixture
def api_client(api_base_url, request_timeout_seconds):
    # Client 只接收配置结果，URL 选择与校验不属于传输层职责。
    return RestfulBookerClient(
        base_url=api_base_url,
        timeout=request_timeout_seconds,
    )


@pytest.fixture
def booking_client(api_client):
    return BookingClient(api_client)


@pytest.fixture
def auth_token(api_client, auth_credentials):
    """获取认证 token，供需要鉴权的测试和资源 fixture 使用。"""
    response = api_client.post(
        "/auth",
        json=auth_credentials,
    )

    assert response.status_code == 200

    data = response.json()
    token = data.get("token")

    assert isinstance(token, str)
    assert token.strip()

    return token


def _extract_booking_id(response):
    """从创建响应中尽早提取 booking ID。"""
    try:
        data = response.json()
    except ValueError:
        return None

    if not isinstance(data, dict):
        return None

    booking_id = data.get("bookingid")

    if isinstance(booking_id, int):
        return booking_id

    return None


def _cleanup_booking(booking_client, booking_id, token):
    """删除 booking，并验证资源最终不存在。"""
    if booking_id is None:
        return

    current_response = booking_client.get_booking(booking_id)

    # 测试主体可能已经删除资源，视为清理完成。
    if current_response.status_code == 404:
        return

    assert current_response.status_code == 200, (
        f"Unexpected cleanup status: {current_response.status_code}; booking_id={booking_id}"
    )

    delete_response = booking_client.delete_booking(
        booking_id,
        token,
    )

    assert delete_response.status_code == 201, (
        f"Unexpected delete status: {delete_response.status_code}; booking_id={booking_id}"
    )

    deleted_response = booking_client.get_booking(booking_id)

    assert deleted_response.status_code == 404, (
        f"Booking still exists after cleanup: "
        f"booking_id={booking_id}; "
        f"status={deleted_response.status_code}"
    )


@pytest.fixture
def created_booking(booking_client, auth_token):
    # 资源数据属于 booking fixture，认证能力由 auth_token fixture 提供。
    payload = build_booking_payload(
        lastname="Booking",
        totalprice=999,
        additionalneeds="Fixture data",
    )

    # 必须在 try 之前初始化，保证异常路径可以访问。
    booking_id = None

    try:
        create_response = booking_client.create_booking(payload)

        # 先登记 ID，再执行状态码和响应内容断言。
        booking_id = _extract_booking_id(create_response)

        assert create_response.status_code == 200, (
            f"Expected status code 200, got {create_response.status_code}"
        )
        assert isinstance(booking_id, int), f"Expected integer booking_id, got {booking_id!r}"

        # 只返回 booking 自身相关的信息，不暴露 token。
        yield {
            "booking_id": booking_id,
            "payload": payload,
        }

    finally:
        # 测试通过或失败后，都尝试清理资源。
        _cleanup_booking(
            booking_client,
            booking_id,
            auth_token,
        )
