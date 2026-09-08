import pytest
from src.settings import (
    DEFAULT_RESTFUL_BOOKER_TIMEOUT_SECONDS,
    DEFAULT_RESTFUL_BOOKER_URL,
    SettingsError,
    get_settings,
)


def test_uses_default_url_when_environment_variable_is_not_set(monkeypatch):
    monkeypatch.delenv("RESTFUL_BOOKER_URL", raising=False)

    settings = get_settings()

    assert settings.restful_booker_url == DEFAULT_RESTFUL_BOOKER_URL


def test_environment_variable_overrides_default_url(monkeypatch):
    monkeypatch.setenv(
        "RESTFUL_BOOKER_URL",
        "http://127.0.0.1:3002/",
    )

    settings = get_settings()

    assert settings.restful_booker_url == "http://127.0.0.1:3002"


def test_url_is_stripped_and_trailing_slash_is_removed(monkeypatch):
    monkeypatch.setenv(
        "RESTFUL_BOOKER_URL",
        "  http://127.0.0.1:3002/  ",
    )

    settings = get_settings()

    assert settings.restful_booker_url == "http://127.0.0.1:3002"


@pytest.mark.parametrize(
    "value",
    [
        "",
        "   ",
    ],
)
def test_empty_url_raises_settings_error(monkeypatch, value):
    monkeypatch.setenv("RESTFUL_BOOKER_URL", value)

    with pytest.raises(
        SettingsError,
        match="RESTFUL_BOOKER_URL must not be empty",
    ):
        get_settings()


def test_unsupported_protocol_raises_settings_error(monkeypatch):
    monkeypatch.setenv(
        "RESTFUL_BOOKER_URL",
        "ftp://127.0.0.1:3002",
    )

    with pytest.raises(
        SettingsError,
        match="RESTFUL_BOOKER_URL must use http or https",
    ):
        get_settings()


def test_invalid_url_raises_settings_error(monkeypatch):
    monkeypatch.setenv(
        "RESTFUL_BOOKER_URL",
        "not-a-url",
    )

    with pytest.raises(
        SettingsError,
        match="RESTFUL_BOOKER_URL must be a valid URL",
    ):
        get_settings()


@pytest.mark.parametrize(
    "value",
    [
        "http://:3002",
        "http://127.0.0.1:abc",
        "http://[::1",
    ],
)
def test_malformed_host_or_port_raises_settings_error(monkeypatch, value):
    monkeypatch.setenv("RESTFUL_BOOKER_URL", value)

    # 覆盖 hostname 缺失、端口非数字和 urlparse 解析失败三类输入。
    with pytest.raises(
        SettingsError,
        match="RESTFUL_BOOKER_URL must be a valid URL",
    ):
        get_settings()


def test_settings_reads_environment_when_called(monkeypatch):
    # 两次调用读取不同值，证明配置不是在 import 时固定的。
    monkeypatch.setenv(
        "RESTFUL_BOOKER_URL",
        "http://127.0.0.1:3001",
    )

    first_settings = get_settings()

    monkeypatch.setenv(
        "RESTFUL_BOOKER_URL",
        "http://127.0.0.1:3002",
    )

    second_settings = get_settings()

    assert first_settings.restful_booker_url == "http://127.0.0.1:3001"
    assert second_settings.restful_booker_url == "http://127.0.0.1:3002"


def test_api_client_uses_settings_url(monkeypatch, request):
    monkeypatch.setenv(
        "RESTFUL_BOOKER_URL",
        "http://127.0.0.1:3002/",
    )

    # 先设置环境变量，再按需创建真实 fixture，避免依赖测试服务或网络请求。
    api_client = request.getfixturevalue("api_client")

    assert api_client.base_url == "http://127.0.0.1:3002"


# ----------------------------
# Timeout configuration tests
# ----------------------------


def test_uses_default_timeout_when_environment_variable_is_not_set(monkeypatch):
    monkeypatch.delenv(
        "RESTFUL_BOOKER_TIMEOUT_SECONDS",
        raising=False,
    )

    settings = get_settings()

    assert settings.request_timeout_seconds == DEFAULT_RESTFUL_BOOKER_TIMEOUT_SECONDS
    assert isinstance(settings.request_timeout_seconds, float)


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("5", 5.0),
        ("2.5", 2.5),
        ("0.1", 0.1),
        ("  4.5  ", 4.5),
    ],
)
def test_valid_timeout_is_parsed_as_float(monkeypatch, value, expected):
    monkeypatch.setenv(
        "RESTFUL_BOOKER_TIMEOUT_SECONDS",
        value,
    )

    settings = get_settings()

    assert settings.request_timeout_seconds == expected
    assert isinstance(settings.request_timeout_seconds, float)


@pytest.mark.parametrize(
    "value",
    [
        "",
        "   ",
    ],
)
def test_empty_timeout_raises_settings_error(monkeypatch, value):
    monkeypatch.setenv(
        "RESTFUL_BOOKER_TIMEOUT_SECONDS",
        value,
    )

    with pytest.raises(
        SettingsError,
        match="RESTFUL_BOOKER_TIMEOUT_SECONDS must not be empty",
    ):
        get_settings()


@pytest.mark.parametrize(
    "value",
    [
        "abc",
        "3s",
    ],
)
def test_non_numeric_timeout_raises_settings_error(monkeypatch, value):
    monkeypatch.setenv(
        "RESTFUL_BOOKER_TIMEOUT_SECONDS",
        value,
    )

    with pytest.raises(
        SettingsError,
        match="RESTFUL_BOOKER_TIMEOUT_SECONDS must be a positive number",
    ):
        get_settings()


@pytest.mark.parametrize(
    "value",
    [
        "0",
        "0.0",
        "-1",
        "-0.5",
    ],
)
def test_non_positive_timeout_raises_settings_error(monkeypatch, value):
    monkeypatch.setenv(
        "RESTFUL_BOOKER_TIMEOUT_SECONDS",
        value,
    )

    with pytest.raises(
        SettingsError,
        match="RESTFUL_BOOKER_TIMEOUT_SECONDS must be a positive number",
    ):
        get_settings()


@pytest.mark.parametrize(
    "value",
    [
        "nan",
        "inf",
        "-inf",
        "Infinity",
    ],
)
def test_non_finite_timeout_raises_settings_error(monkeypatch, value):
    monkeypatch.setenv(
        "RESTFUL_BOOKER_TIMEOUT_SECONDS",
        value,
    )

    # float() 可以解析这些值，因此需要配置层额外限制必须是有限正数。
    with pytest.raises(
        SettingsError,
        match="RESTFUL_BOOKER_TIMEOUT_SECONDS must be a positive number",
    ):
        get_settings()


def test_request_timeout_fixture_uses_settings_value(monkeypatch, request):
    monkeypatch.setenv(
        "RESTFUL_BOOKER_TIMEOUT_SECONDS",
        "6.25",
    )

    # fixture 只消费 Settings，不应重新读取或解析环境变量。
    request_timeout_seconds = request.getfixturevalue("request_timeout_seconds")

    assert request_timeout_seconds == 6.25
    assert isinstance(request_timeout_seconds, float)


def test_api_client_uses_settings_timeout(monkeypatch, request):
    monkeypatch.setenv(
        "RESTFUL_BOOKER_TIMEOUT_SECONDS",
        "6.25",
    )

    # 这里只构造 Client 并检查配置传递，不调用任何 HTTP 方法。
    api_client = request.getfixturevalue("api_client")

    assert api_client.timeout == 6.25


@pytest.fixture(autouse=True)
def isolate_settings_environment(monkeypatch):
    monkeypatch.delenv("RESTFUL_BOOKER_URL", raising=False)
    monkeypatch.delenv(
        "RESTFUL_BOOKER_TIMEOUT_SECONDS",
        raising=False,
    )


def test_timeout_reads_environment_when_called(monkeypatch):
    monkeypatch.setenv(
        "RESTFUL_BOOKER_TIMEOUT_SECONDS",
        "2",
    )

    first_settings = get_settings()

    monkeypatch.setenv(
        "RESTFUL_BOOKER_TIMEOUT_SECONDS",
        "7",
    )

    second_settings = get_settings()

    assert first_settings.request_timeout_seconds == 2.0
    assert second_settings.request_timeout_seconds == 7.0
