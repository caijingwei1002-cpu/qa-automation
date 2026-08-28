"""验证 POST /auth 对有效和无效凭据的处理行为。"""

import pytest


@pytest.mark.parametrize(
    "credential_type",
    ["valid", "invalid"],
    ids=["valid_credentials", "invalid_credentials"],
)
def test_authentication(
    api_client,
    auth_credentials,
    credential_type,
):
    # 参数化复用请求流程，同时明确每种凭据场景的预期结果。
    if credential_type == "valid":
        payload = auth_credentials.copy()
    else:
        payload = {
            "username": auth_credentials["username"],
            "password": "wrong-password",
        }

    response = api_client.post(
        "/auth",
        json=payload,
    )

    # 两种凭据场景都返回 HTTP 200，真正的认证结果体现在响应字段中。
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, dict)

    if credential_type == "valid":
        # 非空 Token 证明认证成功，但 Token 值绝不写入日志。
        token = data.get("token")
        assert isinstance(token, str)
        assert token.strip()
        assert "reason" not in data
    else:
        # 无效凭据必须返回失败原因，且不能返回可用 Token。
        assert data.get("reason") == "Bad credentials"
        assert "token" not in data
