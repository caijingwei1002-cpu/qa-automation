import math
import os
from dataclasses import dataclass
from urllib.parse import urlparse

# 未提供环境变量时使用本地默认目标，保证开发环境开箱可运行。
DEFAULT_RESTFUL_BOOKER_URL = "http://127.0.0.1:3001"
DEFAULT_RESTFUL_BOOKER_TIMEOUT_SECONDS = 3.0


class SettingsError(ValueError):
    """Raised when application configuration is invalid."""


@dataclass(frozen=True)
class Settings:
    # 配置对象不可变，避免 Client 创建后被测试意外改写。
    restful_booker_url: str
    request_timeout_seconds: float


def _parse_restful_booker_url(raw_value: str) -> str:
    # 清洗集中在配置层，调用方只接收可以直接使用的规范化 URL。
    value = raw_value.strip()

    if not value:
        raise SettingsError("RESTFUL_BOOKER_URL must not be empty")

    try:
        parsed = urlparse(value)
    except ValueError as exc:
        # 某些非法 IPv6 等输入会在解析阶段直接抛出 ValueError。
        raise SettingsError("RESTFUL_BOOKER_URL must be a valid URL") from exc

    if not parsed.scheme or not parsed.netloc:
        raise SettingsError("RESTFUL_BOOKER_URL must be a valid URL")

    if parsed.scheme not in {"http", "https"}:
        raise SettingsError("RESTFUL_BOOKER_URL must use http or https")

    try:
        hostname = parsed.hostname
        # urlparse 会延迟校验端口，访问该属性才能发现非数字或越界端口。
        parsed.port
    except ValueError as exc:
        raise SettingsError("RESTFUL_BOOKER_URL must be a valid URL") from exc

    if not hostname or any(character.isspace() for character in hostname):
        raise SettingsError("RESTFUL_BOOKER_URL must be a valid URL")

    return value.rstrip("/")


def _parse_request_timeout_seconds(raw_value: str) -> float:
    # timeout 的清洗和类型转换统一留在配置层，调用方只消费 float。
    value = raw_value.strip()

    if not value:
        raise SettingsError("RESTFUL_BOOKER_TIMEOUT_SECONDS must not be empty")

    try:
        timeout_seconds = float(value)
    except ValueError as exc:
        raise SettingsError("RESTFUL_BOOKER_TIMEOUT_SECONDS must be a positive number") from exc

    # float() 会接受 nan/inf，因此除了 > 0 还需要显式检查有限值。
    if not math.isfinite(timeout_seconds) or timeout_seconds <= 0:
        raise SettingsError("RESTFUL_BOOKER_TIMEOUT_SECONDS must be a positive number")

    return timeout_seconds


def get_settings() -> Settings:
    # 在调用时读取环境变量，避免模块导入时缓存旧配置。
    raw_url = os.getenv("RESTFUL_BOOKER_URL")
    raw_timeout = os.getenv("RESTFUL_BOOKER_TIMEOUT_SECONDS")

    if raw_url is None:
        raw_url = DEFAULT_RESTFUL_BOOKER_URL

    if raw_timeout is None:
        timeout_seconds = DEFAULT_RESTFUL_BOOKER_TIMEOUT_SECONDS
    else:
        timeout_seconds = _parse_request_timeout_seconds(raw_timeout)

    return Settings(
        restful_booker_url=_parse_restful_booker_url(raw_url),
        request_timeout_seconds=timeout_seconds,
    )
