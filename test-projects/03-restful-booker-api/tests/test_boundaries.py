"""验证 booking 核心字段边界及当前接口的校验风险。"""

import pytest

from factories import build_booking_payload


# 每组参数都包含输入、预期状态码和成功时需要核对的字段。
# xfail 用于保留业务预期：如果接口修复了校验，strict=True 会提醒我们移除该标记。
BOUNDARY_CASES = [
    pytest.param(
        {"totalprice": 0},
        200,
        {("totalprice",): 0},
        id="price-zero-accepted",
    ),
    pytest.param(
        {"totalprice": 1},
        200,
        {("totalprice",): 1},
        id="price-minimum-positive-accepted",
    ),
    pytest.param(
        {"totalprice": 999999},
        200,
        {("totalprice",): 999999},
        id="price-large-accepted",
    ),
    pytest.param(
        {"firstname": "A"},
        200,
        {("firstname",): "A"},
        id="firstname-one-character-accepted",
    ),
    pytest.param(
        {"firstname": "张三"},
        200,
        {("firstname",): "张三"},
        id="firstname-unicode-accepted",
    ),
    pytest.param(
        {
            "bookingdates": {
                "checkin": "2026-09-01",
                "checkout": "2026-09-01",
            }
        },
        200,
        {
            ("bookingdates", "checkin"): "2026-09-01",
            ("bookingdates", "checkout"): "2026-09-01",
        },
        id="bookingdates-same-day-accepted",
    ),
    pytest.param(
        {"totalprice": -1},
        400,
        {},
        marks=pytest.mark.xfail(
            strict=True,
            reason="当前接口接受负数价格，缺少 totalprice >= 0 业务校验。",
        ),
        id="price-negative-should-reject",
    ),
    pytest.param(
        {"totalprice": "100"},
        400,
        {},
        marks=pytest.mark.xfail(
            strict=True,
            reason="当前接口把字符串价格转换成数字，未执行严格类型校验。",
        ),
        id="price-string-should-reject",
    ),
    pytest.param(
        {"firstname": ""},
        400,
        {},
        marks=pytest.mark.xfail(
            strict=True,
            reason="当前接口接受空 firstname，缺少必填非空校验。",
        ),
        id="firstname-empty-should-reject",
    ),
    pytest.param(
        {"firstname": " "},
        400,
        {},
        marks=pytest.mark.xfail(
            strict=True,
            reason="当前接口接受纯空格 firstname，缺少空白输入校验。",
        ),
        id="firstname-whitespace-should-reject",
    ),
    pytest.param(
        {
            "bookingdates": {
                "checkin": "2026-09-10",
                "checkout": "2026-09-01",
            }
        },
        400,
        {},
        marks=pytest.mark.xfail(
            strict=True,
            reason="当前接口接受 checkout 早于 checkin，缺少日期顺序校验。",
        ),
        id="bookingdates-reversed-should-reject",
    ),
    pytest.param(
        {
            "bookingdates": {
                "checkin": "2026-02-30",
                "checkout": "2026-03-01",
            }
        },
        400,
        {},
        marks=pytest.mark.xfail(
            strict=True,
            reason="当前接口接受非法日期并进行日期转换，缺少严格日期校验。",
        ),
        id="bookingdates-invalid-date-should-reject",
    ),
]


def _get_token(api_client, auth_credentials):
    """获取边界测试清理资源所需的 Token，不打印 Token 内容。"""
    response = api_client.post("/auth", json=auth_credentials)

    assert response.status_code == 200

    data = response.json()
    token = data.get("token")
    assert isinstance(token, str)
    assert token.strip()

    return token


def _read_path(data, path):
    """读取响应中的顶层或嵌套字段。"""
    for key in path:
        data = data[key]
    return data


def _cleanup_booking(booking_client, booking_id, token):
    """删除当前测试创建的 booking，避免边界用例污染环境。"""
    if not isinstance(booking_id, int):
        return

    current_response = booking_client.get_booking(booking_id)

    if current_response.status_code == 404:
        return

    assert current_response.status_code == 200

    delete_response = booking_client.delete_booking(booking_id, token)
    assert delete_response.status_code in (201, 404)


@pytest.mark.parametrize(
    ("overrides", "expected_status", "expected_fields"),
    BOUNDARY_CASES,
)
def test_create_booking_boundary_cases(
    booking_client,
    api_client,
    auth_credentials,
    overrides,
    expected_status,
    expected_fields,
):
    """用同一套创建、回查和清理流程验证多组字段边界。"""
    token = _get_token(api_client, auth_credentials)
    payload = build_booking_payload(**overrides)
    booking_id = None

    try:
        create_response = booking_client.create_booking(payload)

        # 先尽量提取 ID，哪怕后续状态码断言失败也要清理已创建资源。
        try:
            create_data = create_response.json()
        except ValueError:
            create_data = {}

        if isinstance(create_data, dict):
            booking_id = create_data.get("bookingid")

        # 状态码是接口处理结果；业务预期由每组参数明确给出。
        assert create_response.status_code == expected_status

        if expected_status != 200:
            return

        assert isinstance(booking_id, int)
        assert isinstance(create_data.get("booking"), dict)

        created_booking = create_data["booking"]
        for path, expected_value in expected_fields.items():
            assert _read_path(created_booking, path) == expected_value

        # 成功创建后用同一个动态 ID 回查，证明边界值确实持久化。
        get_response = booking_client.get_booking(booking_id)
        assert get_response.status_code == 200

        persisted_booking = get_response.json()
        for path, expected_value in expected_fields.items():
            assert _read_path(persisted_booking, path) == expected_value
    finally:
        _cleanup_booking(booking_client, booking_id, token)
