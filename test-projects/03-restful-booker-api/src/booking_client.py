from collections.abc import Mapping
from typing import Any

import requests

from src.api_client import RestfulBookerClient


class BookingClient:
    """在通用 HTTP Client 之上提供 booking 领域动作。"""

    def __init__(self, http_client: RestfulBookerClient):
        self.http_client = http_client

    def create_booking(self, payload: Mapping[str, Any]) -> requests.Response:
        # 领域方法负责 booking endpoint，HTTP Client 负责传输细节。
        return self.http_client.post(
            "/booking",
            json=payload,
        )

    def get_bookings(
        self,
        params: Mapping[str, Any] | None = None,
    ) -> requests.Response:
        # 返回原始响应，让测试自行断言状态码和响应结构。
        return self.http_client.get(
            "/booking",
            params=params,
        )

    def get_booking(self, booking_id: int) -> requests.Response:
        # booking ID 是领域参数，具体 URL 拼接仍由领域 Client 负责。
        return self.http_client.get(
            f"/booking/{booking_id}",
        )

    def update_booking(
        self,
        booking_id: int,
        payload: Mapping[str, Any],
        token: str | None,
    ) -> requests.Response:
        # 传递鉴权信息，但授权结果的预期仍由测试负责。
        return self.http_client.put(
            f"/booking/{booking_id}",
            json=payload,
            token=token,
        )

    def partial_update_booking(
        self,
        booking_id: int,
        payload: Mapping[str, Any],
        token: str | None,
    ) -> requests.Response:
        # 暴露 PATCH 部分更新语义，但不替测试决定预期结果。
        return self.http_client.patch(
            f"/booking/{booking_id}",
            json=payload,
            token=token,
        )

    def delete_booking(
        self,
        booking_id: int,
        token: str | None,
    ) -> requests.Response:
        # 删除返回原始响应，既支持成功断言，也支持负向场景断言。
        return self.http_client.delete(
            f"/booking/{booking_id}",
            token=token,
        )
