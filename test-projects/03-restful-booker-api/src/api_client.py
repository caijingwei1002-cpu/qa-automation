from __future__ import annotations

from collections.abc import Mapping
import re
from typing import Any

import requests


class ApiRequestError(RuntimeError):
    """当网络层无法完成 HTTP 请求时抛出。"""


class RestfulBookerClient:
    """集中处理 HTTP 传输细节，将业务断言保留在测试中。"""

    def __init__(self, base_url: str, timeout: float) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.default_headers = {"Accept": "application/json"}

    def _build_url(self, path: str) -> str:
        # 调用方只传入相对 API 路径，环境 base URL 只由 Client 统一管理。
        return f"{self.base_url}/{path.lstrip('/')}"

    def _build_headers(
        self,
        headers: Mapping[str, str] | None = None,
        token: str | None = None,
    ) -> dict[str, str]:
        # 复制默认 headers，避免单次请求的覆盖值污染后续请求。
        merged_headers = dict(self.default_headers)

        if headers:
            merged_headers.update(headers)

        if token:
            # 将鉴权传输细节集中在 Client 中，避免散落到各个测试用例。
            merged_headers["Cookie"] = f"token={token}"

        return merged_headers

    @staticmethod
    def _redact_sensitive(value: str) -> str:
        return re.sub(
            r'''(?i)(["']?(?:token|password|authorization|cookie)["']?\s*[:=]\s*["']?)([^"'\s,}]+)''',
            r"\1<redacted>",
            value,
        )

    @classmethod
    def _response_summary(cls, response: requests.Response | None) -> str:
        if response is None:
            return "status=<no response>, response=<no response>"

        # 保留有用的失败诊断信息，同时防止凭据进入日志。
        body = cls._redact_sensitive(" ".join(response.text.split()))
        if len(body) > 200:
            body = f"{body[:200]}..."

        return f"status={response.status_code}, response={body!r}"

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: Mapping[str, Any] | None = None,
        json: Any = None,
        headers: Mapping[str, str] | None = None,
        token: str | None = None,
    ) -> requests.Response:
        url = self._build_url(path)
        request_headers = self._build_headers(headers=headers, token=token)

        try:
            # 返回原始响应，让每个测试自行断言对应的业务状态码。
            return requests.request(
                method=method,
                url=url,
                params=params,
                json=json,
                headers=request_headers,
                timeout=self.timeout,
            )
        except requests.RequestException as exc:
            raise ApiRequestError(
                "HTTP request failed: "
                f"method={method.upper()}, "
                f"url={url}, "
                f"params={self._redact_sensitive(repr(dict(params or {})))}, "
                f"timeout={self.timeout}s, "
                f"{self._response_summary(exc.response)}, "
                f"error={exc.__class__.__name__}"
            ) from exc

    def get(
        self,
        path: str,
        *,
        params: Mapping[str, Any] | None = None,
        headers: Mapping[str, str] | None = None,
        token: str | None = None,
    ) -> requests.Response:
        return self._request(
            "GET",
            path,
            params=params,
            headers=headers,
            token=token,
        )

    def post(
        self,
        path: str,
        *,
        json: Any = None,
        headers: Mapping[str, str] | None = None,
        token: str | None = None,
    ) -> requests.Response:
        return self._request(
            "POST",
            path,
            json=json,
            headers=headers,
            token=token,
        )

    def put(
        self,
        path: str,
        *,
        json: Any = None,
        headers: Mapping[str, str] | None = None,
        token: str | None = None,
    ) -> requests.Response:
        return self._request(
            "PUT",
            path,
            json=json,
            headers=headers,
            token=token,
        )

    def patch(
        self,
        path: str,
        *,
        json: Any = None,
        headers: Mapping[str, str] | None = None,
        token: str | None = None,
    ) -> requests.Response:
        return self._request(
            "PATCH",
            path,
            json=json,
            headers=headers,
            token=token,
        )

    def delete(
        self,
        path: str,
        *,
        headers: Mapping[str, str] | None = None,
        token: str | None = None,
    ) -> requests.Response:
        return self._request(
            "DELETE",
            path,
            headers=headers,
            token=token,
        )
