import time

# 目标 URL 和请求超时由共享 api_client Fixture 提供。
# RESTFUL_BOOKER_URL 仍可通过该 Fixture 覆盖默认本地目标。

# Restful Booker 的 /ping 契约是 GET 返回 201 Created。
EXPECTED_STATUS_CODE = 201
EXPECTED_RESPONSE_BODY = "Created"

# 请求超时由 api_client fixture 统一管理；性能阈值是本项目定义的端到端门槛，二者职责不同。
MAX_RESPONSE_TIME_SECONDS = 1.0


def test_health_check(api_client):
    """验证 /ping 契约和项目定义的响应时间阈值。"""
    start_time = time.perf_counter()

    # URL 拼接、Accept header 和传输超时由 Client 统一处理。
    response = api_client.get("/ping")

    elapsed_time = time.perf_counter() - start_time

    assert response.status_code == EXPECTED_STATUS_CODE
    assert response.text.strip() == EXPECTED_RESPONSE_BODY
    assert elapsed_time <= MAX_RESPONSE_TIME_SECONDS
