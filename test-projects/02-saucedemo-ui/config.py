import os
from urllib.parse import urlparse


DEFAULT_BASE_URL = "https://www.saucedemo.com/"


def resolve_base_url(cli_value: str | None = None) -> str:
    """按命令行、环境变量、默认值的优先级解析并校验目标地址。"""
    candidate = (
        cli_value
        or os.getenv("SAUCEDEMO_URL")
        or DEFAULT_BASE_URL
    )

    parsed = urlparse(candidate)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError(
            "base_url 必须是完整的 http(s) URL，"
            f"当前值为：{candidate!r}"
        )

    return candidate.rstrip("/") + "/"